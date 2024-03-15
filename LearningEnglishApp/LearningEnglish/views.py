from rest_framework import viewsets, permissions, generics,status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .forms import UserRegisterForm, AdminRegisterForm, UserUpdateForm
from .models import *
from rest_framework.decorators import action
from .serializers import *
from django.shortcuts import get_object_or_404
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import HttpResponse
from oauth2_provider.views.base import TokenView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model, get_application_model
from oauth2_provider.signals import app_authorized
import json

class CustomTokenView(TokenView):
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            body = json.loads(body)
            access_token = body.get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(
                    token=access_token)
                app_authorized.send(
                    sender=self, request=request,
                    token=token)
                body['user'] = {
                    'id': token.user.id,
                    'username': token.user.username,
                    'email': token.user.email,
                    'avatar': token.user.avatar.name
                }
                body = json.dumps(body)
        response = HttpResponse(content=body, status=status)
        for k, v in headers.items():
            response[k] = v
        return response

class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://127.0.0.1:3000/"
    client_class = OAuth2Client

class CourseViewSet(viewsets.ViewSet,
                  generics.RetrieveAPIView,
                    generics.ListAPIView):
    queryset = Course.objects.filter(is_active = True)
    serializer_class = CourseSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = {
                'error': None,
                'message': 'Success',
                'statusCode': status.HTTP_200_OK,
                'results': serializer.data,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            response_data = {
                'error': 'Không tìm thấy khóa học.',
                'message': 'Not found',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'results': None,
            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True,
            url_path="hide-course",
            url_name="hide-course")
    def hide_course(self, request, pk):
        try:
            c = Course.objects.get(pk=pk)
            c.is_active = False
            c.save()
        except Course.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=CourseSerializer(c, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False,
            url_path="search-by-tag",
            url_name="search-by-tag")
    def search_by_tag(self, request):
        try:
            tags = request.data.get('tags', [])
            courses = Course.objects.filter(tag__name__in=tags).distinct()
            serializer = CourseSerializer(courses, many=True, context={'request': request})

            # Tạo đối tượng kết quả mới
            response_data = {
                'error': None,
                'message': 'Success',
                'statusCode': status.HTTP_200_OK,
                'results': serializer.data,
            }

            return Response(data=response_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Trường hợp có lỗi
            response_data = {
                'error': str(e),
                'message': 'Error',
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'results': None,
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

class LessonViewSet(viewsets.ViewSet,
                  generics.RetrieveAPIView,
                    generics.ListAPIView,):
    queryset = Lesson.objects.filter(is_active=True)
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'search_by_course_id':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(methods=['get'], detail=False,
            url_path="search-by-course/(?P<course_id>[^/.]+)",
            url_name="search-by-course")
    def search_by_course_id(self, request, course_id=None):
        try:
            course = get_object_or_404(Course, id=course_id)
            queryset = Lesson.objects.filter(fk_courses=course)
            serializer = LessonSerializer(queryset, many=True, context={'request': request})

            response_data = {
                'error': None,
                'message': 'Success',
                'statusCode': status.HTTP_200_OK,
                'results': serializer.data,
            }

            return Response(data=response_data, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            response_data = {
                'error': 'Không tìm thấy khóa học.',
                'message': 'Not found',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'results': None,
            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            response_data = {
                'error': str(e),
                'message': 'Lỗi ' + str(e),
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'results': None,
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True,
            url_path="hide-lesson",
            url_name="hide-lesson")
    def hide_lesson(self, request, pk):
        try:
            l = Lesson.objects.get(pk=pk)
            l.is_active = False
            l.save()
        except Lesson.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=LessonSerializer(l, context={'request':request}).data, status=status.HTTP_200_OK)

class UserPagination(PageNumberPagination):
    page_size = 5

class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = UserPagination

    def get_permissions(self):
        if self.action == 'list' or self.action == 'hide_user':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={"request": request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=False, url_path='update-user')
    def update_user(self, request):
        user_id = request.data.get('id')
        if not id:
            return Response({'message': 'Không có ID user.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        form = UserUpdateForm(instance=user, data=request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'Sửa thành công.'}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='register')
    def register_user(self, request):
        if request.user.is_superuser:
            form = AdminRegisterForm(data=request.POST)
        else:
            form = UserRegisterForm(data=request.POST)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                errors = dict(form.errors)
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], detail=False, url_path='change-password')
    def change_password(self, request):
        user = request.user
        data = request.data

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not user.check_password(old_password):
            return Response({'message': 'Mật khẩu cũ không đúng'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Mật khẩu đã được thay đổi'}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True,
            url_path="hide-user",
            url_name="hide-user")
    def hide_user(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
            u.is_active = not u.is_active
            u.save()
        except User.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=UserSerializer(u, context={'request': request}).data, status=status.HTTP_200_OK)


class QuestionListeningViewSet(viewsets.ModelViewSet):
    queryset = QuestionListening.objects.filter(is_active=True)
    serializer_class = QuestionListeningSerializer

    # def get_permissions(self):
    #     if self.action == 'list' or self.action == 'retrieve':
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-question-listening",
            url_name="hide-question-listening")
    def hide_question(self, request, pk):
        try:
            q = QuestionListening.objects.get(pk=pk)
            q.is_active = False
            q.save()
        except QuestionListening.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=QuestionListeningSerializer(q, context={'request': request}).data, status=status.HTTP_200_OK)

class QuestionGrammarViewSet(viewsets.ModelViewSet):
    queryset = QuestionGrammar.objects.filter(is_active=True)
    serializer_class = QuestionGrammarSerializer

    # def get_permissions(self):
    #     if self.action == 'list' or self.action == 'retrieve':
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-question-grammar",
            url_name="hide-question-grammar")
    def hide_question(self, request, pk):
        try:
            q = QuestionGrammar.objects.get(pk=pk)
            q.is_active = False
            q.save()
        except QuestionGrammar.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=QuestionGrammarSerializer(q, context={'request': request}).data, status=status.HTTP_200_OK)

class QuestionReadingViewSet(viewsets.ModelViewSet):
    queryset = QuestionReading.objects.filter(is_active=True)
    serializer_class = QuestionReadingSerializer

    # def get_permissions(self):
    #     if self.action == 'list' or self.action == 'retrieve':
    #         return [permissions.AllowAny()]
    #     return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-question-reading",
            url_name="hide-question-reading")
    def hide_question(self, request, pk):
        try:
            q = QuestionReading.objects.get(pk=pk)
            q.is_active = False
            q.save()
        except QuestionReading.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=QuestionReadingSerializer(q, context={'request': request}).data, status=status.HTTP_200_OK)

class GrammarViewSet(viewsets.ModelViewSet):
    queryset = Grammar.objects.filter(is_active=True)
    serializer_class = GrammarSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-grammar",
            url_name="hide-grammar")
    def hide_grammar(self, request, pk):
        try:
            g = Grammar.objects.get(pk=pk)
            g.is_active = False
            g.save()
        except Grammar.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=GrammarSerializer(g, context={'request': request}).data, status=status.HTTP_200_OK)


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.filter(is_active=True)
    serializer_class = WordSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-word",
            url_name="hide-word")
    def hide_word(self, request, pk):
        try:
            w = Word.objects.get(pk=pk)
            w.is_active = False
            w.save()
        except Word.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=WordSerializer(w, context={'request': request}).data, status=status.HTTP_200_OK)

class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.filter(is_active=True)
    serializer_class = ReadingSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-reading",
            url_name="hide-reading")
    def hide_reading(self, request, pk):
        try:
            r = Reading.objects.get(pk=pk)
            r.is_active = False
            r.save()
        except Reading.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=ReadingSerializer(r, context={'request': request}).data, status=status.HTTP_200_OK)

class ListeningViewSet(viewsets.ModelViewSet):
    queryset = Listening.objects.filter(is_active=True)
    serializer_class = ListeningSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-listening",
            url_name="hide-listening")
    def hide_listening(self, request, pk):
        try:
            l = Listening.objects.get(pk=pk)
            l.is_active = False
            l.save()
        except Listening.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=ListeningSerializer(l, context={'request': request}).data, status=status.HTTP_200_OK)

class TitleGrammarViewSet(viewsets.ModelViewSet):
    queryset = TitleGrammar.objects.filter(is_active=True)
    serializer_class = TitleGrammarSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-titlegrammar",
            url_name="hide-titlegrammar")
    def hide_titlegrammar(self, request, pk):
        try:
            tg = TitleGrammar.objects.get(pk=pk)
            tg.is_active = False
            tg.save()
        except TitleGrammar.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=TitleGrammarSerializer(tg, context={'request': request}).data, status=status.HTTP_200_OK)


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.filter(is_active=True)
    serializer_class = ProcessSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif(self.action == 'put' or self.action == 'patch'):
            return [permissions.IsAuthenticated]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-process",
            url_name="hide-process")
    def hide_process(self, request, pk):
        try:
            p = Process.objects.get(pk=pk)
            p.is_active = False
            p.save()
        except Process.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=ProcessSerializer(p, context={'request': request}).data, status=status.HTTP_200_OK)

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.filter(is_active=True)
    serializer_class = ScoreSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif(self.action == 'put' or self.action == 'patch'):
            return [permissions.IsAuthenticated]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-score",
            url_name="hide-score")
    def hide_score(self, request, pk):
        try:
            s = Score.objects.get(pk=pk)
            s.is_active = False
            s.save()
        except Score.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=ScoreSerializer(s, context={'request': request}).data, status=status.HTTP_200_OK)

class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friends.objects.filter(is_active=True)
    serializer_class = FriendSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif(self.action == 'put' or self.action == 'patch'):
            return [permissions.IsAuthenticated]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-friend",
            url_name="hide-friend")
    def hide_friend(self, request, pk):
        try:
            f = Friends.objects.get(pk=pk)
            f.is_active = False
            f.save()
        except Friends.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=FriendSerializer(f, context={'request': request}).data, status=status.HTTP_200_OK)

class RankingViewSet(viewsets.ModelViewSet):
    queryset = Ranking.objects.filter(is_active=True)
    serializer_class = RankingSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif(self.action == 'put' or self.action == 'patch'):
            return [permissions.IsAuthenticated]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-ranking",
            url_name="hide-ranking")
    def hide_ranking(self, request, pk):
        try:
            r = Ranking.objects.get(pk=pk)
            r.is_active = False
            r.save()
        except Ranking.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=RankingSerializer(r, context={'request': request}).data, status=status.HTTP_200_OK)
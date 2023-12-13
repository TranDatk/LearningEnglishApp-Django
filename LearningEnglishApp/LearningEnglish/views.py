from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets, permissions, generics,status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import *
from rest_framework.decorators import action
from .serializers import *
from django.http import JsonResponse


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_active = True)
    serializer_class = CourseSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

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


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(is_active=True)
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

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

class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'hide_user':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
        return Response(self.serializer_class(request.user).data)

    @action(methods=['patch'], detail=False, url_path='update-user')
    def update_user(self, request):
        user = request.user
        if user is not None:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='register')
    def register_user(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        except Question.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=UserSerializer(u, context={'request': request}).data, status=status.HTTP_200_OK)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_active=True)
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-question",
            url_name="hide-question")
    def hide_question(self, request, pk):
        try:
            q = Question.objects.get(pk=pk)
            q.is_active = False
            q.save()
        except Question.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=QuestionSerializer(q, context={'request': request}).data, status=status.HTTP_200_OK)

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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-category",
            url_name="hide-category")
    def hide_category(self, request, pk):
        try:
            c = Category.objects.get(pk=pk)
            c.is_active = False
            c.save()
        except Category.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=CategorySerializer(c, context={'request': request}).data, status=status.HTTP_200_OK)

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
    queryset = Listen.objects.filter(is_active=True)
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
            l = Listen.objects.get(pk=pk)
            l.is_active = False
            l.save()
        except Listen.DoesNotExits:
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

class Lesson_Category_WLRGViewSet(viewsets.ModelViewSet):
    queryset = Lesson_Category_WLRG.objects.filter(is_active=True)
    serializer_class = Lesson_Category_WLRGSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @action(methods=['post'], detail=True,
            url_path="hide-wlrg",
            url_name="hide-wlrg")
    def hide_lesson_category_wlrg(self, request, pk):
        try:
            wlrg = Lesson_Category_WLRG.objects.get(pk=pk)
            wlrg.is_active = False
            wlrg.save()
        except Lesson_Category_WLRG.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=Lesson_Category_WLRGSerializer(wlrg, context={'request': request}).data, status=status.HTTP_200_OK)

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
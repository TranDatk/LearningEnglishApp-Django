from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Course, Lesson
from rest_framework.decorators import action
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_active = True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list' \
                or self.action == 'create'\
                or self.action == 'update'\
                or self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(is_active=True)
    serializer_class = LessonSerializer

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

def index(request):
    return render(request,template_name='index.html', context={'name':'Dat'})

def welcome(request, year):
    return HttpResponse("Hello " + str(year))

def welcome2(request, year):
    return HttpResponse("Hello " + str(year))

class TestView(View):
    def get(self, request):
        return HttpResponse("Hello testview")
    def post(self, request):
        pass
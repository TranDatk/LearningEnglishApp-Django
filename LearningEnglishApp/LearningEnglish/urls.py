from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register('course', views.CourseViewSet)
router.register('lesson', views.LessonViewSet)
router.register('users', views.UserViewSet)
router.register('users', views.UserViewSet)
router.register('process', views.ProcessViewSet)
router.register('questions', views.QuestionViewSet)
router.register('grammars', views.GrammarViewSet)
router.register('categories', views.CategoryViewSet)
router.register('words', views.WordViewSet)
router.register('readings', views.ReadingViewSet)
router.register('listenings', views.ListeningViewSet)
router.register('titlegrammars', views.TitleGrammarViewSet)
router.register('wlrgs', views.Lesson_Category_WLRGViewSet)
router.register('processes', views.ProcessViewSet)
router.register('scores', views.ScoreViewSet)
router.register('friends', views.FriendViewSet)
router.register('ranking', views.RankingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
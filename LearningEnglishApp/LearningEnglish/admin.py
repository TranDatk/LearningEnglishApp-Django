from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from django.urls import path
from .models import Course, Lesson, Tag, Reading, Grammar, Process, Ranking, Friends, Score, User, \
    Listening, QuestionReading, QuestionListening
from django.contrib.auth.models import Permission, Group


class ReadingForm(forms.ModelForm):
    paragraph = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Reading
        fields = '__all__'

class GrammarForm(forms.ModelForm):
    recipe = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Grammar
        fields = '__all__'

class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active","description", "image"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]
    readonly_fields = ["display"]

    def display(self, course):
        if course:
            return mark_safe(
                '<img src="/static/{url}/" width="120" />' \
                    .format(url=course.image.name)
            )

class LessonAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active", "index", "description","fk_courses"]
    search_fields = ["id", "name", "created_date", "updated_date", "fk_courses__name"]
    list_filter = ["fk_courses__name", "name", "created_date", "updated_date"]

class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class WordAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class ReadingAdmin(admin.ModelAdmin):
    form = ReadingForm
    list_display = ["id", "name", "created_date", "updated_date", "is_active", "fk_lesson"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class GrammarAdmin(admin.ModelAdmin):
    form = GrammarForm
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class ListeningAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active", "fk_lesson"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class ListeningAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active", "fk_lesson"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class TitleGrammarAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active", "fk_lesson"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class QuestionGrammarAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class QuestionListeningAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class QuestionReadingAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class ProcessAdmin(admin.ModelAdmin):
    list_display = ["id", "progress", "fk_user", "fk_course", "created_date", "updated_date", "is_active"]
    search_fields = ["id","fk_user", "created_date", "updated_date", "fk_course"]
    list_filter = ["id","fk_user", "created_date", "updated_date", "fk_course"]

class ScoreAdmin(admin.ModelAdmin):
    list_display = ["id", "score", "fk_user", "created_date", "updated_date", "is_active"]
    search_fields = ["id","fk_user", "created_date", "updated_date"]
    list_filter = ["id","fk_user", "created_date", "updated_date"]

class FriendsAdmin(admin.ModelAdmin):
    list_display = ["id", "fk_friend_id", "fk_user", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "created_date", "updated_date"]
    list_filter = ["id","fk_friend_id","fk_user", "created_date", "updated_date"]

class RankingAdmin(admin.ModelAdmin):
    list_display = ["id", "score", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id","id_user","name", "created_date", "updated_date"]
    list_filter = ["id","id_user","name", "created_date", "updated_date"]

class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "first_name", "last_name", "is_active"]
    search_fields = ["id","username", "first_name", "last_name"]
    list_filter = ["id","username", "first_name", "last_name"]
    readonly_fields = ["display"]

    def display(self, user):
        if user:
            return mark_safe(
                '<img src="/static/{url}/" width="120" />' \
                    .format(url=user.avatar.name)
            )

class LearningEnglishAppAdminSite(admin.AdminSite):
    site_header = 'LearningEnglishApp'
    index_title = 'Hệ thống quản lý khóa học tiếng Anh'

    def get_urls(self):
        return [
            path('learningenglish-stats/', self.LearningEnglish_stats)
        ] + super().get_urls()

    def LearningEnglish_stats(self, request):
        course_count = Course.objects.count()
        stats = Course.objects.annotate(lesson_count=Count('lessons')).values("id", "name", "lesson_count")

        return TemplateResponse(request, 'admin/learningenglish-stats.html',{
            'course_count' : course_count,
            'stats' : stats
        })

admin_site = LearningEnglishAppAdminSite('LearningEnglish')

admin_site.register(User, UserAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(Reading, ReadingAdmin)
admin_site.register(Grammar, GrammarAdmin)
admin_site.register(Listening, ListeningAdmin)
admin_site.register(Process, ProcessAdmin)
admin_site.register(Score, ScoreAdmin)
admin_site.register(Ranking, RankingAdmin)
admin_site.register(Friends, FriendsAdmin)
admin_site.register(QuestionReading, QuestionReadingAdmin)
admin_site.register(QuestionListening, QuestionListeningAdmin)

admin_site.register(Permission)
admin_site.register(Group)







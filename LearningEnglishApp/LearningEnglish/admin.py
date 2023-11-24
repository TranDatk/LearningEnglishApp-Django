from django.contrib import admin
from .models import Category, Course, Lesson, Tag, Word, Reading, Question, Grammar, Listen, Lesson_Category_WLRG, TitleGrammar

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active","description", "image"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

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
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "content", "created_date", "updated_date"]
    list_filter = ["content", "created_date", "updated_date"]

class GrammarAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class ListenAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

class Lesson_Category_WLRGAdmin(admin.ModelAdmin):
    list_display = ["id", "id_WLRG", "fk_Lesson", "fk_Category"]
    search_fields = ["id", "id_WLRG", "fk_Lesson", "fk_Category"]

class TitleGrammarAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "is_active"]
    search_fields = ["id", "name", "created_date", "updated_date"]
    list_filter = ["name", "created_date", "updated_date"]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Grammar, GrammarAdmin)
admin.site.register(Listen, ListenAdmin)
admin.site.register(Lesson_Category_WLRG, Lesson_Category_WLRGAdmin)
admin.site.register(TitleGrammar, TitleGrammarAdmin)
# Register your models here.

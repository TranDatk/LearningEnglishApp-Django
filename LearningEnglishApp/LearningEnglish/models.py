from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

class ItemBase(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255, null=False, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Tag(ItemBase):
    class Meta:
        db_table = 'tag'
        ordering = ["created_date"]

    def __str__(self):
        return self.name

class Question(models.Model):
    class Meta:
        db_table = 'question'
    content = models.TextField(null=False, blank=True)
    ft_answer = models.CharField(max_length=255,null=True)
    sd_answer = models.CharField(max_length=255,null=True)
    td_answer = models.CharField(max_length=255, null=True)
    fh_answer = models.CharField(max_length=255,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    correct_answer = models.IntegerField(null=True)
    fk_lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, related_name="questions")

    def __str__(self):
        return self.content

class Category(ItemBase):
    class Meta:
        db_table = 'category'
        ordering = ["created_date"]

class Course(ItemBase):
    class Meta:
        db_table = 'course'
        ordering = ["created_date"]
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    description = models.TextField(null=True, blank=True)
    tag = models.ManyToManyField(Tag, related_name="tags",null=True, blank=True)

class Lesson(ItemBase):
    class Meta:
        unique_together = ('name','fk_courses')
        db_table = 'lesson'
        ordering = ["created_date"]
    index = models.IntegerField(null = False)
    description = models.TextField(null=True, blank=True)
    fk_courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")


class Word(ItemBase):
    class Meta:
        db_table = 'word'
    means = models.CharField(max_length=255, null=True, blank=True, unique=True)
    spelling = models.CharField(max_length=255, null=True, blank=True, unique=True)
    sound = models.FileField(default=None, blank=True, null=True, upload_to='words_sound/%Y/%m')
    example = models.TextField(null=True, blank=True)


class Grammar(ItemBase):
    class Meta:
        db_table = 'grammar'
    recipe = models.CharField(max_length=255,null=True, blank=True)
    example = models.TextField(null=True, blank=True)
    fk_title_grammar = models.ForeignKey('TitleGrammar', on_delete=models.SET_NULL, null=True, related_name="grammars")

class Listen(ItemBase):
    class Meta:
        db_table = 'listen'
    sound = models.FileField(default=None, blank=True, null=True, upload_to='listening_file/%Y/%m')

class Reading(ItemBase):
    class Meta:
        db_table = 'reading'
    paragraph = models.TextField(null=True, blank=True)

class TitleGrammar(ItemBase):
    class Meta:
        db_table = 'titlegrammar'

class Lesson_Category_WLRG(models.Model):
    class Meta:
        unique_together = ('id_WLRG','fk_Lesson','fk_Category')
        db_table = 'lesson_category_wlrg'
    id_WLRG = models.IntegerField(null=False)
    fk_Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_category_wlrg")
    fk_Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="lesson_category_wlrg")

    def __str__(self):
        return "Id: " + str(self.id_WLRG) + " - Lesson: " + str(self.fk_Lesson) \
               + " - Category: " + str(self.fk_Category)
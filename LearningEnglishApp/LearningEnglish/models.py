from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
from PIL import Image

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    email = models.CharField(max_length=255, null=False, unique=True)

    # def save(self, *args, **kwargs):
    #     super(User, self).save(*args, **kwargs)
    #
    #     avatar = Image.open(self.avatar.path)
    #
    #     if avatar.height > 300 or avatar.width > 300:
    #         output_size = (300, 300)
    #         avatar.thumbnail(output_size)
    #         avatar.save(self.avatar.path)

class ItemBase(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255, null=False, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Process(models.Model):
    class Meta:
        db_table = 'process'

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    progress = models.IntegerField(default=0)
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="process_user")
    fk_course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, related_name="process_course")

    def __str__(self):
        return str(self.id) + " : " + str(self.progress)

class Score(models.Model):
    class Meta:
        db_table = 'score'

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="score_user")

    def __str__(self):
        return str(self.id) + " : " + str(self.score)

class Friends(models.Model):
    class Meta:
        db_table = 'friends'

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="users")
    fk_friend_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_friend")

    def __str__(self):
        return str(self.id) + " : " + str(self.fk_friend_id)

class Ranking(models.Model):
    class Meta:
        db_table = 'ranking'

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    id_user = models.IntegerField(default=None)
    name = models.CharField(max_length=255)


class Tag(ItemBase):
    class Meta:
        db_table = 'tag'
        ordering = ["created_date"]

    def __str__(self):
        return self.name

class Question(models.Model):
    class Meta:
        db_table = 'question'
    content = RichTextField(null=False, blank=True)
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
    recipe = RichTextField(null=True, blank=True)
    example = models.TextField(null=True, blank=True)
    fk_title_grammar = models.ForeignKey('TitleGrammar', on_delete=models.SET_NULL, null=True, related_name="grammars")

class Listen(ItemBase):
    class Meta:
        db_table = 'listen'
    sound = models.FileField(default=None, blank=True, null=True, upload_to='listening_file/%Y/%m')

class Reading(ItemBase):
    class Meta:
        db_table = 'reading'
    paragraph = RichTextField(null=True, blank=True)

class TitleGrammar(ItemBase):
    class Meta:
        db_table = 'titlegrammar'

class Lesson_Category_WLRG(models.Model):
    class Meta:
        unique_together = ('id_WLRG','fk_lesson','fk_category')
        db_table = 'lesson_category_wlrg'
    id_WLRG = models.IntegerField(null=False)
    fk_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_category_wlrg")
    fk_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="lesson_category_wlrg")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Id: " + str(self.id_WLRG) + " - Lesson: " + str(self.fk_lesson) \
               + " - Category: " + str(self.fk_category)
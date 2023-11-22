from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

class ItemBase(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, null=False, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Topic(ItemBase):
    class Meta:
        db_table = 'topic'
        ordering = ["created_date"]

    def __str__(self):
        return self.name

class Course(ItemBase):
    class Meta:
        db_table = 'course'
        ordering = ["created_date"]
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    description = models.TextField(null=True, blank=True)
    topic = models.ManyToManyField(Topic, related_name="topics",null=True, blank=True)

class Lesson(ItemBase):
    class Meta:
        unique_together = ('name','fk_courses')
        db_table = 'lesson'
        ordering = ["created_date"]
    index = models.IntegerField(null = False)
    description = models.TextField(null=True, blank=True)
    fk_courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

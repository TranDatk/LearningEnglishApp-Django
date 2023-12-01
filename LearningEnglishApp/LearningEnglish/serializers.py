from rest_framework.serializers import ModelSerializer
from .models import Course, Tag, Lesson



class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class CourseSerializer(ModelSerializer):
    tag = TagSerializer(many=True)
    class Meta:
        model = Course
        fields = ["id", "name", "image", "created_date", "is_active", "tag"]

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "name", "index", "description", "fk_courses","created_date", "updated_date","is_active"]
from rest_framework.serializers import ModelSerializer
from .models import Course, Tag, Lesson, User, Process


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password' : {'write_only':'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

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


class ProcessSerializer(ModelSerializer):
    class Meta:
        model = Process
        fields = ["id", "progress", "fk_user", "fk_course", "created_date", "updated_date", "is_active"]

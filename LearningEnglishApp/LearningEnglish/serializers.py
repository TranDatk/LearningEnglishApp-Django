from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class UserSerializer(ModelSerializer):
    avatar = serializers.SerializerMethodField(source='avatar')
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'username', 'password', 'avatar', 'is_active', 'is_superuser']
        extra_kwargs = {
            'password' : {'write_only':'true'}
        }

    def validate(self, data):
        if 'password' not in data or 'username' not in data or data['password'] == '' or data['username'] == '':
            raise serializers.ValidationError("Mật khẩu không được để trống")

        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email đã tồn tại trong hệ thống")

        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Tên người dùng đã tồn tại trong hệ thống")
        return data

    def get_avatar(self, user):
        if user.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % user.avatar.name)

            return '/static/%s' % user.avatar.name


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Xóa domain từ URL hình ảnh
        if 'image' in representation and representation['image']:
            representation['image'] = representation['image'].replace(self.context['request'].build_absolute_uri('/'),
                                                                      '')

        return representation


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "name", "index", "description", "fk_courses","created_date", "updated_date","is_active"]

class ProcessSerializer(ModelSerializer):
    class Meta:
        model = Process
        fields = ["id", "progress", "fk_user", "fk_course", "created_date", "updated_date", "is_active"]

class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = ["id","content", "created_date", "updated_date", "is_active", "correct_answer",
                  "ft_answer", "sd_answer","td_answer","fh_answer","fk_lesson"]

class GrammarSerializer(ModelSerializer):
    class Meta:
        model = Grammar
        fields = ["id", "name", "recipe","example","created_date", "updated_date", "is_active", "fk_title_grammar"]

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_date", "updated_date", "is_active"]

class WordSerializer(ModelSerializer):
    class Meta:
        model = Word
        fields = ["id", "name", "means", "spelling", "sound", "example" ,"created_date", "updated_date", "is_active"]

class ReadingSerializer(ModelSerializer):
    class Meta:
        model = Reading
        fields = ["id", "name", "created_date", "updated_date", "is_active", "paragraph"]

class ListeningSerializer(ModelSerializer):
    class Meta:
        model = Listen
        fields = ["id", "name", "created_date", "updated_date", "is_active", "sound"]

class TitleGrammarSerializer(ModelSerializer):
    class Meta:
        model = TitleGrammar
        fields = ["id", "name", "created_date", "updated_date", "is_active"]

class Lesson_Category_WLRGSerializer(ModelSerializer):
    class Meta:
        model = Lesson_Category_WLRG
        fields = ["id", "created_date", "updated_date", "is_active", "id_WLRG", "fk_lesson", "fk_category"]

class ProcessSerializer(ModelSerializer):
    class Meta:
        model = Process
        fields = ["id", "created_date", "updated_date", "is_active", "fk_user", "fk_course", "progress"]

class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = ["id", "created_date", "updated_date", "is_active", "fk_user", "score"]

class FriendSerializer(ModelSerializer):
    class Meta:
        model = Friends
        fields = ["id", "created_date", "updated_date", "is_active", "fk_user", "fk_friend_id"]

class RankingSerializer(ModelSerializer):
    class Meta:
        model = Ranking
        fields = ["id", "created_date", "updated_date", "is_active", "score", "id_user", "name"]
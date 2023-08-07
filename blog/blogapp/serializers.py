from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User,Blog,Comment

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name']

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'created_time', 'updated_time', 'author', 'image']
        read_only_fields = ['id', 'created_time', 'updated_time']



class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_time', 'updated_time', 'author', 'blog']
        read_only_fields = ['id', 'created_time', 'updated_time', 'author']

class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=True)
    is_superuser = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'password', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user



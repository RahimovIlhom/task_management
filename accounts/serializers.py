from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import CustomUser, Profile, ClassName
from task_app.models import Course


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ('username', 'password')

    def validate_username(self, username):
        if not username:
            raise serializers.ValidationError('The username is required')
        if not username.isalnum():
            raise serializers.ValidationError('The username should contain only letters and numbers')
        return username

    def validate_password(self, password):
        if not password:
            raise serializers.ValidationError('The password is required')
        return password

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('The username or password is wrong')  # {"error": "Password or username is wrong"}

        attrs['user'] = user
        return attrs  # {"username": "test", "password": "test1234", "user": UserObject}


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(max_length=255, required=True)
    password2 = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, attrs):
        password1 = attrs.pop('password1')
        password2 = attrs.pop('password2')
        username = attrs.get('username')
        email = attrs.get('email')
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        if password1 != password2:
            raise serializers.ValidationError('Passwords do not match!')
        attrs['password'] = password1
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class CustomTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError('Username yoki password xato')
        refresh = RefreshToken.for_user(user)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        return data


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user_id', 'user_type', 'user', 'course', 'fullname', 'age', 'image', 'information', 'class_name']

    def get_user(self, obj):
        return obj.user.username


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['user_type', 'user', 'course', 'fullname', 'age', 'image', 'information', 'class_name']

    def get_user(self, obj):
        return obj.user.username

    def update(self, instance, validated_data):
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.course = validated_data.get('course', instance.course)
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.age = validated_data.get('age', instance.age)
        instance.image = validated_data.get('image', instance.image)
        instance.information = validated_data.get('information', instance.information)
        instance.class_name = validated_data.get('class_name', instance.class_name)
        instance.save()
        return instance


class ClassNameSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = ClassName
        fields = ['id', 'name', 'course']

    def get_course(self, obj):
        return obj.course.name

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.course = validated_data.get('course', instance.course)
        if instance.course:
            print('Course not found')

        instance.save()
        return instance


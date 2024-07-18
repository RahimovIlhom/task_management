from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import CustomUser


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

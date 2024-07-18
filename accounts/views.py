from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework import status

from .serializers import LoginSerializer, UserRegisterSerializer, UserSerializer

user_model = get_user_model()


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            "username": user.username
        })


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = user_model.objects.create_user(username=username, email=email, password=password)
        user.save()
        data = UserSerializer(instance=user).data
        return Response({"message": "User created successfully", 'data': data}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            201: UserSerializer(many=False),
            400: 'Bad Request',
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


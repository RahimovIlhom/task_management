from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Profile, ClassName
from .serializers import LoginSerializer, UserRegisterSerializer, UserSerializer, CustomTokenObtainSerializer, \
    ProfileSerializer, ProfileUpdateSerializer, ClassNameSerializer

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


class LoginApiView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CustomTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data, status=status.HTTP_201_CREATED)


class RefreshTokenApiView(TokenRefreshView):
    permission_classes = [permissions.AllowAny, ]


class CreateProfileApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateProfileApiView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProfileUpdateSerializer


    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class GetProfileApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class DeleteProfileApiView(APIView):
    permission_classes = [permissions.IsAdminUser, ]

    def delete(self, request, pk):
        del_user = Profile.objects.get(pk=pk)
        del_user.delete()
        return Response({"message": "Foydalanuvchi muvaffaqiyatli tarzda ochirildi"}, status=status.HTTP_204_NO_CONTENT)


class ClassNameCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = ClassNameSerializer


class ClassNameUpdateApiView(generics.UpdateAPIView):
    queryset = ClassName.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ClassNameSerializer

    def patch(self, request, *args, **kwargs):
        class_name = self.get_object()
        user_type = Profile.objects.get(user=request.user).user_type
        if user_type == 'admin' or user_type == 'mentor':
            serializer = ClassNameSerializer(class_name, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)


class ClassNameListApiView(generics.ListAPIView):
    queryset = ClassName.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ClassNameSerializer



from django.urls import path

from .views import LoginView, RegisterView, LoginApiView, RefreshTokenApiView, CreateProfileApiView, \
    UpdateProfileApiView, GetProfileApiView, DeleteProfileApiView, ClassNameCreateApiView, ClassNameUpdateApiView, \
    ClassNameListApiView

urlpatterns = [
    path('token/', LoginApiView.as_view()),
    path('token/refresh/', RefreshTokenApiView.as_view()),
    # path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('create/profile/', CreateProfileApiView.as_view()),
    path('update/profile/', UpdateProfileApiView.as_view()),
    path('information/profile/', GetProfileApiView.as_view()),
    path('delete/profile/<int:pk>/', DeleteProfileApiView.as_view()),
    path('create/class/', ClassNameCreateApiView.as_view()),
    path('update/class/<int:pk>/', ClassNameUpdateApiView.as_view()),
    path('list/class/', ClassNameListApiView.as_view()),
]


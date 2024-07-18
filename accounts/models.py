from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


USER_STATUS = (
    ('admin', 'Admin'),
    ('mentor', 'Mentor'),
    ('student', 'Student'),
)

user_model = get_user_model()


class Profile(models.Model):
    user_type = models.CharField(max_length=10, choices=USER_STATUS, default='student')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    course = models.ForeignKey('task_app.Course', on_delete=models.SET_NULL, null=True, blank=True)
    fullname = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(5), MaxValueValidator(100),
    ])
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    information = models.TextField(null=True, blank=True)
    class_name = models.ForeignKey('ClassName', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname


class ClassName(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey('task_app.Course', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

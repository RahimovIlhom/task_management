from django.contrib import admin

from .models import CustomUser, Profile, ClassName


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'age', 'class_name')
    search_fields = ('user', 'fullname', 'age', 'class_name')
    list_filter = ('class_name', 'course')


@admin.register(ClassName)
class ClassNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    search_fields = ('name', 'course')

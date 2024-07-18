from django.contrib import admin

from .models import Course, Task, Assignment, TaskResult, TaskRank


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'information')
    search_fields = ('name', 'information')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'information', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')
    search_fields = ('title', 'information')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'ball')
    search_fields = ('title', 'ball')


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'file')
    search_fields = ('task', 'student')


@admin.register(TaskRank)
class TaskRankAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'rank')
    search_fields = ('task', 'student')
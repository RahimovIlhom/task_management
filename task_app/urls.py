from django.urls import path

from task_app.views import (
    CourseCreateApiView,
    CourseListApiView,
    CourseUpdateApiView,
    CourseDetailApiView,
    # CourseDeleteApiView,

    TaskCreateApiView,
    TaskListApiView,
    TaskUpdateApiView,
    TaskDetailApiView,
    TaskDeleteApiView,

    AssignmentCreateApiView,
    AssignmentListApiView,
    AssignmentUpdateApiView,
    AssignmentDeleteApiView,
    AssignmentDetailApiView,

    TaskResultCreateApiView, TaskResultListApiView, TastResultDetailApiView, StudentAssessmentCreateAPIView,
)

urlpatterns = [
    # Course urls
    path('create/course/', CourseCreateApiView.as_view()),
    path('list/course/', CourseListApiView.as_view()),
    path('update/course/<int:pk>/', CourseUpdateApiView.as_view()),
    path('detail/course/<int:pk>/', CourseDetailApiView.as_view()),
    # path('delete/course/<int:pk>/', CourseDeleteApiView.as_view()),

    # Task urls
    path('create/task/', TaskCreateApiView.as_view()),
    path('list/', TaskListApiView.as_view()),
    path('detail/<int:pk>/', TaskDetailApiView.as_view()),
    path('update/<int:pk>/', TaskUpdateApiView.as_view()),
    path('delete/<int:pk>/', TaskDeleteApiView.as_view()),

    # Assignment urls
    path('create/assignment/', AssignmentCreateApiView.as_view()),
    path('assignment/list/', AssignmentListApiView.as_view()),
    path('assignment/update/<int:pk>/', AssignmentUpdateApiView.as_view()),
    path('assignment/detail/<int:pk>/', AssignmentDetailApiView.as_view()),
    path('assignment/delete/<int:pk>/', AssignmentDeleteApiView.as_view()),

    # TaskResult urls
    path('student/result/create', TaskResultCreateApiView.as_view()),
    path('student/result/detail/<int:pk>/', TastResultDetailApiView.as_view()),
    path('student/result/list/', TaskResultListApiView.as_view()),

    # baholash
    path('task_result/assessment/', StudentAssessmentCreateAPIView.as_view()),
]

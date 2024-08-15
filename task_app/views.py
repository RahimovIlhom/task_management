from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from task_app.models import Course, Task, Assignment, TaskResult, AssignmentGrade
from task_app.serializers import CourseSerializer, TaskSerializer, AssignmentSerializer, TaskResultSerializer, \
    TaskResultRetrieveSerializer, StudentAssessmentSerializer


class CourseCreateApiView(generics.CreateAPIView):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CourseSerializer

    def post(self, request, *args, **kwargs):
        user_type = Profile.objects.get(user=request.user).user_type
        if user_type == 'admin' or user_type == 'mentor':
            serializer = CourseSerializer(data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)


class CourseListApiView(generics.ListAPIView):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CourseSerializer


class CourseUpdateApiView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CourseSerializer

    def patch(self, request, *args, **kwargs):
        course = self.get_object()
        user_type = Profile.objects.get(user=request.user).user_type
        if user_type == 'admin' or user_type == 'mentor':
            serializer = CourseSerializer(course, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)


class CourseDetailApiView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CourseSerializer


# class CourseDeleteApiView(generics.DestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated, ]
#     serializer_class = CourseSerializer
#
#     def delete(self, request, *args, **kwargs):
#         course = Course.objects.get(pk=kwargs['pk'])
#         user_type = Profile.objects.get(user=request.user).user_type
#         if user_type == 'mentor' or user_type == 'student':
#             raise ValidationError({
#                 "message": "Sizda bu sahifa uchun ruxsat yo'q",
#                 "status": f"{status.HTTP_403_FORBIDDEN}"
#             })
#         if user_type == 'admin':
#             course.delete()
#             return Response({"message": "Kurs muvaffaqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)
#         return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)


class TaskCreateApiView(generics.CreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(user=request.user)
        if user_profile.user_type == 'mentor':
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                task = serializer.save(mentor=user_profile)
                response_serializer = TaskSerializer(task)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)


class TaskUpdateApiView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TaskSerializer

    def patch(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(user=request.user)
        if user_profile.user_type == 'mentor':
            task = self.get_object()
            serializer = self.get_serializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)


class TaskListApiView(generics.ListAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        if request.data:
            course = request.data['course']
            tasks = Task.objects.filter(course=course)
            serializer = self.get_serializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            tasks = self.get_queryset()
            serializer = self.get_serializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TaskDetailApiView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TaskSerializer


class TaskDeleteApiView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    def delete(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(user=request.user)
        try:
            task = Task.objects.get(pk=kwargs['pk'])
            if user_profile.user_type == 'mentor' or user_profile.user_type == 'admin':

                task.delete()
                return Response({"message": "Mavzu muvaffaqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

        except Task.DoesNotExist:
            raise ValidationError({
                "status": "404",
                "message": "Bunday mavzu mavjud emas"
            })


class AssignmentCreateApiView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AssignmentSerializer

    def post(self, request, *args, **kwargs):
        user_type = Profile.objects.get(user=request.user).user_type
        if user_type == 'mentor':
            serializer = AssignmentSerializer(data=request.data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)


class AssignmentListApiView(generics.ListAPIView):
    queryset = Assignment.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AssignmentSerializer


class AssignmentUpdateApiView(generics.UpdateAPIView):
    queryset = Assignment.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AssignmentSerializer

    def patch(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(user=request.user)
        if user_profile.user_type == 'mentor':
            assignment = self.get_object()
            serializer = self.get_serializer(assignment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)


class AssignmentDeleteApiView(generics.DestroyAPIView):
    queryset = Assignment.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]

    def delete(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(user=request.user)
        try:
            assignment = Assignment.objects.get(pk=kwargs['pk'])
            if user_profile.user_type == 'mentor':
                assignment.delete()
                return Response({"message": "Topshiriq muvaffaqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

        except Assignment.DoesNotExist:
            raise ValidationError({
                "status": "404",
                "message": "Bunday topshiriq mavjud emas"
            })


class AssignmentDetailApiView(generics.RetrieveAPIView):
    queryset = Assignment.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = AssignmentSerializer

    def get(self, request, *args, **kwargs):
        try:
            assignment = Assignment.objects.get(pk=kwargs['pk'])
            serializer = self.get_serializer(assignment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Assignment.DoesNotExist:
            raise ValidationError({
                "status": "404",
                "message": "Bunday topshiriq mavjud emas"
            })


class TaskResultCreateApiView(generics.CreateAPIView):
    queryset = TaskResult.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TaskResultSerializer

    def post(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(user=request.user)
        if user_profile.user_type == 'student':
            serializer = TaskResultSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(student=user_profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)


class TastResultDetailApiView(generics.RetrieveAPIView):
    queryset = TaskResult.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TaskResultRetrieveSerializer

    def get(self, request, *args, **kwargs):
        try:
            task_result = TaskResult.objects.get(pk=kwargs['pk'])
            serializer = self.get_serializer(task_result)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except TaskResult.DoesNotExist:
            raise ValidationError({
                "status": "404",
                "message": "Bunday natija mavjud emas"
            })


class TaskResultListApiView(generics.ListAPIView):
    queryset = TaskResult.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = TaskResultSerializer

    def get(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(user=request.user)
        if user_profile.user_type == 'student':
            user_tasks = TaskResult.objects.filter(student=user_profile)
            serializer = self.get_serializer(user_tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user_profile.user_type == 'mentor':
            student_id = request.data.get('student')
            if student_id:
                user_tasks = TaskResult.objects.filter(student=student_id)
                serializer = self.get_serializer(user_tasks, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                user_tasks = self.get_queryset()
                serializer = self.get_serializer(user_tasks, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)


class StudentAssessmentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = StudentAssessmentSerializer

    @swagger_auto_schema(request_body=StudentAssessmentSerializer)
    def post(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(user=request.user)
        if user_profile.user_type == 'mentor':
            serializer = StudentAssessmentSerializer(data=request.data)
            if serializer.is_valid():
                assignments = serializer.validated_data.pop('assignment', [])
                assignments_result = []
                for assignment in assignments:
                    new_obj = AssignmentGrade.objects.create(assignment_id=assignment['assignment_id'],
                                                             grade=assignment['grade'])
                    new_obj.save()
                    assignments_result.append(new_obj)
                try:
                    task_result = TaskResult.objects.get(id=serializer.validated_data['task_result_id'])
                    task_result.assignments.set(assignments_result)
                    task_result.status = 'done'
                    task_result.save()
                    return Response({"message": "Student baholandi"}, status=status.HTTP_200_OK)
                except TaskResult.DoesNotExist:
                    raise ValidationError("Task result not found")
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Sizda bu sahifa uchun ruxsat yo'q"}, status=status.HTTP_403_FORBIDDEN)

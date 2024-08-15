from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from accounts.serializers import ProfileSerializer
from .models import Course, Task, Assignment, TaskResult, TaskRank, AssignmentGrade


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'ball']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.ball = validated_data.get('ball', instance.ball)
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    mentor = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    assignments = AssignmentSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'mentor', 'course', 'course_name', 'title', 'information',
                  'video', 'file', 'assignments', 'start_time', 'end_time']
        extra_kwargs = {'assignment_ids': {'write_only': True}}

    def get_mentor(self, obj):
        return obj.mentor.fullname if obj.mentor else None

    def get_course_name(self, obj):
        return obj.course.name if obj.course else None

    def create(self, validated_data):
        assignments = validated_data.pop('assignments', [])
        assignments_data = []
        if assignments:
            for assignment in assignments:
                new_obj = Assignment.objects.create(**assignment)
                # assignment = {'title': title, 'ball': ball}
                # create(title=title, ball=ball)
                assignments_data.append(new_obj)
        task = Task.objects.create(**validated_data)
        task.assignments.set(assignments_data)
        task.save()
        return task

    def update(self, instance, validated_data):
        assignments_data = validated_data.pop('assignment_ids', None)
        for attrs, value in validated_data.items():
            setattr(instance, attrs, value)

        if assignments_data is not None:
            instance.assignments.set(assignments_data)

        instance.save()
        return instance


class TaskResultSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    file = serializers.FileField(required=True, validators=[FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'pptx', 'py', 'js', 'html', 'css', 'jpg', 'jpeg', 'png'])
    ])

    class Meta:
        model = TaskResult
        fields = ['id', 'task', 'student', 'file']

    def get_student(self, obj):
        return obj.student.fullname

    def create(self, validated_data):
        task_result = TaskResult.objects.create(**validated_data, status='pending')
        task_result.save()
        return task_result


class TaskResultRetrieveSerializer(serializers.ModelSerializer):
    student = ProfileSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = TaskResult
        fields = ['id', 'task', 'student', 'file', 'status', 'created_at']


class AssignmentGradeSerializer(serializers.Serializer):
    assignment_id = serializers.IntegerField()
    grade = serializers.IntegerField()


class StudentAssessmentSerializer(serializers.Serializer):
    task_result_id = serializers.IntegerField(required=True)
    assignment = AssignmentGradeSerializer(many=True, required=True)

    class Meta:
        model = TaskResult
        fields = ['task_result_id', 'assignment']

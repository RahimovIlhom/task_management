from django.db import models
from django.core.validators import FileExtensionValidator


class Course(models.Model):
    name = models.CharField(max_length=255)
    information = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    mentor = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    information = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to='task_videos', null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    file = models.FileField(upload_to='task_files', null=True, blank=True,
                            validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'pptx'])])
    assignments = models.ManyToManyField('Assignment', blank=True, related_name='tasks')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mentor.fullname}-{self.title}"


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    ball = models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return self.title


TASK_RESULT_STATUS = (
    ('pending', 'Pending'),
    ('done', 'Done'),
)


class TaskResult(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_results', null=True, blank=True,
                            validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xlsx', 'pptx'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assignments = models.ManyToManyField('Assignment', blank=True, related_name='task_results')
    status = models.CharField(max_length=10, choices=TASK_RESULT_STATUS, default='pending')

    def __str__(self):
        return f"{self.task.title}-{self.student.fullname}"


RANKS_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class TaskRank(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(default=5, choices=RANKS_CHOICES, db_default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title}-{self.student.fullname}"

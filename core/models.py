from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

TEACHIN_DAYS = (
    ('1', 'Days'),
    ('2', 'Evening'),
    ('3', 'Weekend'),
)


POST_TYPE = (
    ('p', 'Publication'),
    ('b', 'Blog'),
    ('r', 'Resource'),
)

EVALUATION_TYPE = (
    ('a', 'Assignment'),
    ('c', 'CAT'),
    ('e', 'Exam'),
)

class University(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name    


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    # Comer sep ex: 6,7 or 1,4
    teaching_days = models.CharField(max_length=1, choices=TEACHIN_DAYS)
    start_hour = models.TimeField()
    duration = models.IntegerField()
    class_room = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.name
    
    def get_cats(self):
        cats = Evaluation.objects.filter(e_type='c', course=self, starts__lt=datetime.now(), ends__gt=datetime.now())
        return cats

    def get_assignments(self):
        assignments = Evaluation.objects.filter(e_type='a', course=self, starts__lt=datetime.now(), ends__gt=datetime.now())
        return assignments
    
    def get_exams(self):
        exams = Evaluation.objects.filter(e_type='e', course=self, starts__lt=datetime.now(), ends__gt=datetime.now())
        return exams
    
    
class Student(models.Model):
    student_id = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} - {self.university}"

class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.student} - {self.course}"

class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    presence = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.student} - {self.course} - {self.date} - Present : {self.presence}"


class Post(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField()
    year = models.DateField(auto_now_add=True)
    # Blog, Publication, Resouce
    p_type = models.CharField(max_length=1, choices=POST_TYPE)
    public = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.p_type} - Public : {self.public} "

    
class Evaluation(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True)
    description = models.TextField()
    maximum = models.IntegerField(default=100)
    # Assignment, CAT, Exam
    e_type = models.CharField(max_length=1, choices=EVALUATION_TYPE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    starts = models.DateTimeField(null=True, default=None, blank=True)
    ends = models.DateTimeField(null=True, default=None, blank=True)


class Score(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    points = models.FloatField()
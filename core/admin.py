from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Attendance)
admin.site.register(models.Course)
admin.site.register(models.Post)
admin.site.register(models.Evaluation)
admin.site.register(models.Student)
admin.site.register(models.Score)
admin.site.register(models.University)
admin.site.register(models.StudentCourse)

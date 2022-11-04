from django.db import models
from teacher import models as TMODEL
from student.models import Student
from teacher.models import Teacher
from froala_editor.fields import FroalaField
import datetime

class Course(models.Model):
    course_name = models.CharField(max_length=500)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    atempt = models.PositiveIntegerField(default=2)
    date = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

class Docs(models.Model):
    title = models.CharField(max_length=100,  default=True)
    content = FroalaField()
    slug = models.SlugField(max_length=200,  default=True)
    name = models.CharField(max_length=1000,  default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    def isnumeric(self):
        name = self.name
        if name.isnumeric() is True:
            return True
        else:
            return False
    def save(self, *args, **kwargs):
        super(Docs, self).save(*args, **kwargs)
class Comment(models.Model):
    post = models.ForeignKey(Docs,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


from django.db import models
from teacher import models as TMODEL
from student.models import Student
from teacher.models import Teacher
from ckeditor.fields import RichTextField
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   atempt = models.PositiveIntegerField(default=2)
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
    title = models.CharField(max_length=1000, null=True, blank=True)
    content = RichTextField()
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)
    video_iframe = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        super(Docs, self).save(*args, **kwargs)


class ScratchDocs(models.Model):
    docs_name = models.CharField(max_length=1000, null=True, blank=True)
    iframe = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self):
        return self.docs_name


    def save(self, *args, **kwargs):
        super(Docs, self).save(*args, **kwargs)
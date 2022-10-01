from django.db import models
from django.contrib.auth.models import User
from student.models import Student
class Parents(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=True)
    student_model = models.ManyToManyField(Student)
    def __str__(self):
        return self.user
from django.db import models
from django.contrib.auth.models import User
TAG = ((0, "Computer"), (1, "Gears for PC"), (2, "Tutorial"), (3, "Vehicle"))
CLASS = ((0, "6"), (1, "7"), (2, "8"), (3, "9"))

class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=True)
    salary=models.PositiveIntegerField(null=True)
    class_model=models.IntegerField(choices=TAG, default=3)
    grade=models.IntegerField(choices=CLASS, default=0)
    @property
    def get_name(self):
        self.user.name = self.user.first_name+" "+self.user.last_name + " " + self.grade
        return self.user.name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        self.user.name = self.user.first_name+" "+self.user.last_name + " " + str(self.grade)
        return self.user.name
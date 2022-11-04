from django.db import models
from django.contrib.auth.models import User
from quiz.models import SchoolClass
# TAG = ((0, "LSĐL"), (1, "Toán"), (2, "Văn"), (3, "Anh"))
CLASS = ((0, "6"), (1, "7"), (2, "8"), (3, "9"))
class Tag(models.Model):
    name = models.CharField(max_length=2000,null=False, default=True)
    def __str__(self):
        return self.name
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',default="image/teacher.png",null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    salary=models.PositiveIntegerField(null=True)
    class_model=models.ForeignKey(Tag,on_delete=models.CASCADE,default=True)
    grade=models.IntegerField(choices=CLASS, default=0)
    class_name = models.ForeignKey(SchoolClass,on_delete=models.CASCADE,default=True)

    @property
    def get_name(self):
        self.user.name = self.user.first_name+" "+self.user.last_name + " " + str(self.grade)
        return self.user.name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        self.user
        return self.user
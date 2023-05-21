from django import forms
from django.contrib.auth.models import User
from . import models

class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
        'password': forms.PasswordInput()
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model=models.Teacher
        fields=['address','mobile','profile_pic','class_model','grade']

class ClassroomCreateForm(forms.ModelForm):
    class Meta:
        model = models.Classroom

        fields = [
            "title",
            "subtitle",
            "class_slug",
            "content",
            "notes",
            "image",
            "author"
        ]

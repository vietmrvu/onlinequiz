from django import forms
from django.contrib.auth.models import User
from . import models

class parentsUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']
        widgets = {
        'password': forms.PasswordInput()
        }

class parentsForm(forms.ModelForm):
    class Meta:
        model=models.Parents
        fields=['address','mobile','profile_pic','student_model']


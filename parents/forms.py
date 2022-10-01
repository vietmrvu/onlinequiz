from django import forms
from django.contrib.auth.models import User
from . import models

class ParentsUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','student_model']
        widgets = {
        # 'student_model':forms.CheckboxSelectMultiple(),
        'password': forms.PasswordInput()
        }

class ParentsForm(forms.ModelForm):
    class Meta:
        model=models.Parents
        fields=['address','mobile','profile_pic']
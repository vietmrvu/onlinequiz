from django.shortcuts import render,redirect,reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from quiz import forms as QFORM


#for showing signup/login button for parents
def parentsclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'parents/parentsclick.html')

def parents_signup_view(request):
    userForm=forms.parentsUserForm()
    parentsForm=forms.parentsForm()
    mydict={'userForm':userForm,'parentsForm':parentsForm}
    if request.method=='POST':
        userForm=forms.parentsUserForm(request.POST)
        parentsForm=forms.parentsForm(request.POST,request.FILES)
        if userForm.is_valid() and parentsForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            parents=parentsForm.save(commit=False)
            parents.user=user
            parents.save()
            my_parents_group = Group.objects.get_or_create(name='parents')
            my_parents_group[0].user_set.add(user)
        return HttpResponseRedirect('parentslogin')
    return render(request,'parents/parentssignup.html',context=mydict)



def is_parents(user):
    return user.groups.filter(name='parents').exists()

@login_required(login_url='parentslogin')
@user_passes_test(is_parents)
def parents_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'parents/parents_dashboard.html',context=dict)

@login_required(login_url='parentslogin')
@user_passes_test(is_parents)
def parents_exam_view(request):
    return render(request,'parents/parents_exam.html')

# Create your views here.

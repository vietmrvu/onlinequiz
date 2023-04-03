from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from parents import models as PMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User


# Administrators
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'quiz/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def is_parents(user):
    return user.groups.filter(name='parents').exists()

def afterlogin_view(request):
    if is_student(request.user):   
        accountapproval=SMODEL.Student.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student/student-dashboard')
        else:
            return render(request,'student/student_wait_for_approval.html')   
    if is_parents(request.user):
        accountapproval=PMODEL.Parents.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('parents/parents-dashboard')
        else:
            return render(request,'parents/parents_wait_for_approval.html')
    if is_teacher(request.user):
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    'total_parents':PMODEL.Parents.objects.all().count(),
    'total_docs':models.Docs.objects.all().count(),
    }
    return render(request,'quiz/admin_dashboard.html',context=dict)
@login_required(login_url='adminlogin')
def admin_user(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().count(),
    'total_parents':PMODEL.Parents.objects.all().count(),
    }
    return render(request,'quiz/admin_users.html',context=dict)
# Teachers
@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'quiz/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_teacher.html',{'teachers':teachers})

@login_required(login_url='adminlogin')
def add_teacher_view(request):
    userForm=TFORM.TeacherUserForm()
    teacherForm=TFORM.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            print(my_teacher_group[0])
        return HttpResponseRedirect('teacherlogin')
    return render(request,'teacher/teachersignup.html',context=mydict)

@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'quiz/update_teacher.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')


@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'quiz/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    teacherSalary=forms.TeacherSalaryForm()
    if request.method=='POST':
        teacherSalary=forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            teacher=TMODEL.Teacher.objects.get(id=pk)
            teacher.salary=teacherSalary.cleaned_data['salary']
            teacher.status=True
            teacher.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    return render(request,'quiz/salary_form.html',{'teacherSalary':teacherSalary})

@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'quiz/admin_view_teacher_salary.html',{'teachers':teachers})



# Students
@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'courses':models.Course.objects.all()
    }
    return render(request,'quiz/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'quiz/admin_view_student.html',{'students':students})
    
@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm, "student":student}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'quiz/update_student.html',context=mydict)

@login_required(login_url='adminlogin')
def add_student_view(request):
    userForm=SFORM.StudentUserForm()
    studentForm=SFORM.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST)
        studentForm=SFORM.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student') 

@login_required(login_url='adminlogin')
def approve_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm, "student":student}
    if request.method=='POST':
        student= SMODEL.Student.objects.get(id=pk)
        student.status=True
        student.save()
        return HttpResponseRedirect('/admin-view-student')
    return render(request,'quiz/check_student.html', context=mydict)
# Parents
@login_required(login_url='adminlogin')
def admin_view_parents_view(request):
    parents= PMODEL.Parents.objects.all()
    return render(request,'quiz/admin_view_parents.html',{'parents':parents})

@login_required(login_url='adminlogin')
def update_parents_view(request,pk):
    parents=PMODEL.Parents.objects.get(id=pk)
    user=PMODEL.User.objects.get(id=parents.user_id)
    userForm=PFORM.ParentsUserForm(instance=user)
    parentsForm=PFORM.ParentsUserForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=PFORM.ParentsUserForm(request.POST,instance=user)
        parentsForm=PFORM.ParentsUserForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and parentsForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            parentsForm.save()
            return redirect('admin-view-parents')
    return render(request,'quiz/update_parents.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_parents_view(request,pk):
    parents=PMODEL.Parents.objects.get(id=pk)
    user=User.objects.get(id=parents.user_id)
    user.delete()
    parents.delete()
    return HttpResponseRedirect('/admin-view-parents')
# Courses
@login_required(login_url='adminlogin')
def admin_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'quiz/admin_course.html',{'courses':courses})


@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-course')
    return render(request,'quiz/admin_add_course.html',{'courseForm':courseForm})


@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-course')

# Questions

@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'quiz/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=models.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'quiz/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'quiz/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'quiz/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

# Marks
@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'quiz/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'quiz/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'quiz/admin_check_marks.html',{'results':results})
    
# Docs

@login_required(login_url='adminlogin')
def admin_docs_view(request):
    return render(request,'quiz/admin_docs.html')

@login_required(login_url='adminlogin')

def admin_add_docs_view(request):
    context = {'courseForm': forms.DocsForm}
    try:
        if request.method == 'POST':
            form = forms.DocsForm(request.POST)
            title = request.POST.get('title')
            name = request.POST.get('name')

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']

            blog_obj = models.Docs.objects.create(
                title=title, name=name,
                content=content
            )
            print(blog_obj)
            return redirect('/admin-view-docs')
    except Exception as e:
        print(e)

    return render(request, 'quiz/admin_add_docs.html', context)

@login_required(login_url='adminlogin')

def delete_docs_view(request,pk):
    course=models.Docs.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-docs')

@login_required(login_url='adminlogin')

def admin_view_docs_view(request):
    courses = models.Docs.objects.all().order_by('-created_at')
    return render(request,'quiz/admin_view_docs.html',{'courses':courses})


@login_required(login_url="adminlogin")
def updateDocs(request, pk):
	course = models.Docs.objects.get(id=pk)
	form = forms.DocsForm(instance=course)
	if request.method == 'POST':
		form = forms.DocsForm(request.POST, request.FILES, instance=course)
		if form.is_valid():
			form.save()
		return redirect('/admin-view-docs')

	context = {'courseForm': form}
	return render(request, 'quiz/admin_update_docs.html', context)

@login_required(login_url='adminlogin')
def admin_view_docs_view_detail(request, pk):
    docs = models.Docs.objects.get(id=pk)
    comments = docs.comments.all()
    new_comment = None
    if request.method == 'POST':
        form = forms.DocsForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            body = comment_form.cleaned_data['body']
            name = comment_form.cleaned_data['name']
            email = comment_form.cleaned_data['email']
            # Create Comment object but don't save to database yet
            # Assign the current post to the comment
            # Save the comment to the database
        comment_object = models.Comment.objects.create(
            email=email, name=name,
            body=body, post_id=pk
        )
    else:
        comment_form = forms.CommentForm()

    context = {'docs':docs,
                'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form}
    return render(request, 'quiz/admin_view_docs_detail.html', context) 

# Footer


def aboutus_view(request):
    return render(request,'quiz/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'quiz/contactussuccess.html')
    return render(request, 'quiz/contactus.html', {'form':sub})



from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from student import models as SMODEL
from parents import models as PMODEL
from quiz import forms as QFORM
#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
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



def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    dict={
    'pending_parents':PMODEL.Parents.objects.all().filter(status=False).count(),
    'pending_student':SMODEL.Student.objects.all().filter(status=False).count(),
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count(),
    }

    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all().order_by('-created_at')
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='teacherlogin')
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request,'teacher/teacher_add_question.html',{'questionForm':questionForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    courses= QMODEL.Course.objects.all().order_by('-created_at')
    return render(request,'teacher/teacher_view_question.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().order_by('-created_at').filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')

# approve parents
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_pending_parents_view(request):
    parents= PMODEL.Parents.objects.all().filter(status=False)
    return render(request,'teacher/teacher_pending_parents.html',{'parents':parents})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def approve_parents_view(request,pk):
    if request.method=='POST':
        parents= PMODEL.Parents.objects.get(id=pk)
        parents.status=True
        parents.save()
        return HttpResponseRedirect('/teacher/teacher-view-pending-parents')
    return render(request,'teacher/check_parents.html')

@login_required(login_url='teacherlogin')
def reject_parents_view(request,pk):
    parents= PMODEL.Parents.objects.get(id=pk)
    user=User.objects.get(id=parents.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/teacher/teacher-view-pending-parents')
# approve student
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_pending_student_view(request):
    student= SMODEL.Student.objects.all().filter(status=False)
    return render(request,'teacher/teacher_pending_student.html',{'student':student})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def approve_student_view(request,pk):
    if request.method=='POST':
        student= SMODEL.Student.objects.get(id=pk)
        student.status=True
        student.save()
        return HttpResponseRedirect('/teacher/teacher-view-pending-student')
    return render(request,'teacher/check_student.html')

@login_required(login_url='teacherlogin')
def reject_student_view(request,pk):
    student= SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/teacher/teacher-view-pending-student')
# Docs
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_docs_view(request):
    return render(request,'teacher/teacher_docs.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_docs_view(request):
    context = {'courseForm': QFORM.DocsForm}
    try:
        if request.method == 'POST':
            form = QFORM.DocsForm(request.POST)
            title = request.POST.get('title')
            name = request.POST.get('name')

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']

            blog_obj = QMODEL.Docs.objects.create(
                title=title, name=name,
                content=content
            )
            print(blog_obj)
            return redirect('/teacher/teacher-view-docs')
    except Exception as e:
        print(e)

    return render(request, 'teacher/teacher_add_docs.html', context)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_docs_view(request,pk):
    course=QMODEL.Docs.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-docs')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_docs_view(request):
    docs = QMODEL.Docs.objects.all().order_by('-created_at')
    return render(request,'teacher/teacher_view_docs.html',{'docs':docs})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_docs_view_detail(request, pk):
    docs = QMODEL.Docs.objects.get(id=pk)
    comments = docs.comments.all()
    new_comment = None
    if request.method == 'POST':
        form = QFORM.DocsForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment_form = QFORM.CommentForm(data=request.POST)
        if comment_form.is_valid():
            body = comment_form.cleaned_data['body']
            name = comment_form.cleaned_data['name']
            email = comment_form.cleaned_data['email']
            # Create Comment object but don't save to database yet
            # Assign the current post to the comment
            # Save the comment to the database
        comment_object = QMODEL.Comment.objects.create(
            email=email, name=name,
            body=body, post_id=pk
        )
    else:
        comment_form = QFORM.CommentForm()

    context = {'docs':docs,
                'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form}
    return render(request, 'teacher/teacher_view_docs_view.html', context)
# Marks
@login_required(login_url='teacherlogin')
def teacher_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'teacher/teacher_view_student_marks.html',{'students':students})

@login_required(login_url='teacherlogin')
def teacher_view_marks_view(request,pk):
    courses = QMODEL.Course.objects.all().order_by('-created_at')
    response =  render(request,'teacher/teacher_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='teacherlogin')
def teacher_check_marks_view(request,pk):
    course = QMODEL.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'teacher/teacher_check_marks.html',{'results':results, 'course':course})


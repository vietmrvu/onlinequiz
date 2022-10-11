from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('teacherclick', views.teacherclick_view),
path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teachersignup', views.teacher_signup_view,name='teachersignup'),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-docs', views.teacher_docs_view,name='teacher-docs'),
path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),
path('teacher-view-docs-detail/<slug:slug>/', views.teacher_view_docs_view_detail, name="teacher-view-docs-detail"),
path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),
path('teacher-add-docs', views.teacher_add_docs_view,name='teacher-add-docs'),
path('teacher-view-docs', views.teacher_view_docs_view,name='teacher-view-docs'),
path('teacher-view-pending-parents', views.teacher_view_pending_parents_view,name='teacher-view-pending-parents'),
path('approve-parents/<int:pk>', views.approve_parents_view,name='approve-parents'),
path('reject-parents/<int:pk>', views.reject_parents_view,name='reject-parents'),
path('teacher-view-pending-student', views.teacher_view_pending_student_view,name='teacher-view-pending-student'),
path('approve-student/<int:pk>', views.approve_student_view,name='approve-student'),
path('reject-student/<int:pk>', views.reject_student_view,name='reject-student'),

]
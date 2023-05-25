from django.urls import path
from parents import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('parentsclick', views.parentsclick_view, name='parentsclick'),
path('parentslogin', LoginView.as_view(template_name='parents/parentslogin.html'),name='parentslogin'),
path('parentssignup', views.parents_signup_view,name='parentssignup'),
path('parents-dashboard', views.parents_dashboard_view,name='parents-dashboard'),
path('parents-exam', views.parents_exam_view,name='parents-exam'),
path('parents-view-student-marks', views.parents_view_student_marks_view,name='parents-view-student-marks'),
path('parents-view-marks/<int:pk>', views.parents_view_marks_view,name='parents-view-marks'),
path('parents-check-marks/<int:pk>', views.parents_check_marks_view,name='parents-check-marks'),
path('parents-view-course-detail/<int:pk>', views.parents_course_view_detail,name='parents-view-course-detail'),

    path('parents-add-docs', views.parents_add_docs_view,name='parents-add-docs'),
    path('parents-view-docs', views.parents_view_docs_view,name='parents-view-docs'),
    path('delete-docs/<int:pk>', views.delete_docs_view,name='delete-docs'),
    path('parents-view-docs-detail/<int:pk>/', views.parents_view_docs_view_detail, name="parents-view-docs-detail"),
    path('update-docs/<int:pk>', views.updateDocs,name='update-docs'),
]
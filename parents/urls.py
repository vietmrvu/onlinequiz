from django.urls import path
from parents import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('parentsclick', views.parentsclick_view, name='parentsclick'),
path('parentslogin', LoginView.as_view(template_name='parents/parentslogin.html'),name='parentslogin'),
path('parentssignup', views.parents_signup_view,name='parentssignup'),
path('parents-dashboard', views.parents_dashboard_view,name='parents-dashboard'),
path('parents-exam', views.parents_exam_view,name='parents-exam'),
]
from django.contrib import admin
from django.urls import path
from app_1 import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.welcome, name='home'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="logout.html"), name='logout'),
    path('register/', views.register, name='register'),
    path('subjects/', views.getSubjects, name='subjects'),
    path('profsubjects/', views.profesorSubjects, name='profesorsubjects'),
    path('subject/<int:subjectid>/', views.editSubject, name='editsubject'),
    path('addsubject/', views.addSubject, name='addsubject'),
    path('deletesubject/<int:subjectid>/', views.deleteSubject, name='deletesubject'),
    path('editprofesor/<int:subjectid>/', views.editNositelj, name='editprofesor'),
    path('students/', views.students, name='students'),
    path('profesors/', views.profesors, name='profesors'),
    path('edituser/<int:userid>/', views.editUser, name='edituser'),
    path('usersonsubject/<int:subjectid>', views.usersOnSubject, name='usersonsubject'),
    path('changestatus/<int:userid>/<int:subjectid>/<str:status>/', views.changeStatus, name='changestatus'),
    path('enrollmentform/<int:userid>', views.enrollmentForm, name='enrollmentform'),
    path('enroll/<int:userid>/<int:subjectid>/', views.enroll, name='enroll'),
    path('disenroll/<int:userid>/<int:subjectid>/', views.disenroll, name='disenroll'),
]

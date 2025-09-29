"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('dindex/', views.dindex, name='dindex'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('gallery/', views.gallery, name='gallery'),
    path('team/', views.team, name='team'),
    path('appointment/', views.appointment, name='appointment'),
    path('blog/', views.blog, name='blog'),
    path('blog_details/', views.blog_details, name='blog_details'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('fpass/', views.fpass, name='fpass'),
    path('changepass/', views.changepass, name='changepass'),
    path('history/', views.history, name='history'),
    path('otp/', views.otp, name='otp'),
    path('newpass/', views.newpass, name='newpass'),
    path('profile/', views.profile, name='profile'),
    path('d_profile/', views.d_profile, name='d_profile'),
    path('d_dash/', views.d_dash, name='d_dash'),
    path("appointment/<int:pk>/<str:action>/", views.update_appointment, name="update_appointment"),
    path("appointment/delete/<int:pk>/", views.delete_appointment, name="delete_appointment"),
    path("upload_record/<int:patient_id>/", views.upload_record, name="upload_record"),
    path("my_records/", views.my_records, name="my_records"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("delete_doctor/<int:pk>/", views.delete_doctor, name="delete_doctor"),
    path("adelete_appointment/<int:pk>/", views.adelete_appointment, name="adelete_appointment"),
    path("apatientsdelete/<int:pk>/", views.apatientsdelete, name="apatientsdelete"),
    path('alogout/', views.alogout, name='alogout'),
    
]
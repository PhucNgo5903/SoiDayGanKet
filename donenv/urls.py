"""donvol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("gallery/", views.gallery, name="gallery"),
    path("login-admin/", views.login_admin, name="login_admin"),
    path("login-donor/", views.login_donor.as_view(), name="login_donor"),
    path("login-beneficiary/", views.login_beneficiary.as_view(), name="login_beneficiary"),
    path("login-volunteer/", views.login_volunteer.as_view(), name="login_volunteer"),
    path("signup-donor/", views.signup_donor.as_view(), name="signup_donor"),
    path("signup-volunteer/", views.signup_volunteer.as_view(), name="signup_volunteer"),
    path("signup-beneficiary/", views.signup_beneficiary.as_view(), name="signup_beneficiary"),

    path("index-donor/", views.index_donor, name="index_donor"),
    path("index-volunteer/", views.index_volunteer, name="index_volunteer"),
    path("index-beneficiary/", views.index_beneficiary, name="index_beneficiary"),
    
]

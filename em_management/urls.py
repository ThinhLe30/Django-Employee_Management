"""em_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import include, path
from admins.admin import admin_site
from . import views
from django.contrib.auth.views import (LoginView, LogoutView)


urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='login.html',redirect_authenticated_user=True),name='login'),
    path('logout/',LogoutView.as_view(next_page='/login/'),name="logout"),
    path('home/', include('home.urls', namespace="home")),
    path('employees/', include('employees.urls', namespace="employees")),
    path('departments/', include('departments.urls', namespace="departments")),
    path('admins/', include('admins.urls', namespace="admins")),
    path('salaries/', include('salaries.urls', namespace="salaries")),
    path('', include("django.contrib.auth.urls")), 
    path('permission_error/', views.permission_error, name='permission_error'),
    path('', lambda request: redirect('/login/'), name='index'),
]

handler404="handle_error.views.handle_404"
handler500="handle_error.views.handle_500"
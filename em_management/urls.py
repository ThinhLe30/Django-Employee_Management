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
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('home:home'), name='index'),
    path('admin/', admin.site.urls),
    path('home/', include('home.urls', namespace="home")),
    path('employees/', include('employees.urls', namespace="employees")),
    path('departments/', include('departments.urls', namespace="departments")),
    # path('salaries/', include('salaries.urls', namespace="salaries")),
    path('admins/', include('admins.urls', namespace="admins")),
    path('salaries/', include('salaries.urls', namespace="salaries")),
    # path('admins/', include('admin.urls', namespace="admin"))
]
handler404="handle_error.views.handle_404"
handler500="handle_error.views.handle_500"
from django.urls import path, include
from . import views
app_name = 'employees'
urlpatterns = [
    path('list/', views.showEmployeesList, name='list'),
]

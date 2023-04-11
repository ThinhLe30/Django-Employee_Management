from django.urls import path, include
from . import views
app_name = 'departments'
urlpatterns = [
    path('list/', views.showDepartmentsList, name='list'),
]
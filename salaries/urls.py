from django.urls import path, include
from . import views
app_name = 'employees'
urlpatterns = [
    path('list/', views.showLevel_SalariesList, name='list'),
    path('detail/<int:id>/', views.getDetailOfLevel_Salary, name='detail'),
    path('add/',views.showLevel_SalaryForm, name ='add'),
    path('edit/<int:id>/', views.showLevel_SalaryForm, name='edit'),
    path('delete/<int:id>/', views.deleteLevel_Salary, name='delete'),
    path('save/',views.saveLevel_Salary, name ='save'),
]

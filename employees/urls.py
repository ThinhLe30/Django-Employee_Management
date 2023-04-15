from django.urls import path, include
from . import views
app_name = 'employees'
urlpatterns = [
    path('list/', views.showEmployeesList, name='list'),
    path('detail/<int:id>/', views.getDetailOfEmployee, name='detail'),
    path('add/',views.showEmployeeForm, name ='add'),
    path('edit/<int:id>/', views.showEmployeeForm, name='edit'),
    path('delete/<int:id>/', views.deleteEmployee, name='delete'),
    path('save/',views.saveEmployee, name ='save'),
    path('checkDuplicate/',views.checkDuplicateEmailAndPhone, name ='checkDuplicate')
]

from django.urls import path
from . import views
app_name = 'departments'

urlpatterns = [
    path('list/', views.showDepartmentsList, name='list'),
    path('add/', views.showDepartmentForm, name='add'),
    path('edit/<int:id>/', views.showDepartmentForm, name='update'),
    path('save/',views.saveDepartment, name ='save'),
    path('delete/<int:id>/', views.deleteDepartment, name='delete'),
]
from django.urls import path, include
from . import views
app_name = 'admins'
urlpatterns = [
    path('list/', views.showAdminsList, name='list'),
    path('detail/<int:id>/', views.getDetailOfAdmin, name='detail'),
    path('add/', views.showAdminForm, name='add'),
    path('edit/<int:id>/', views.showAdminForm, name='edit'),
    path('delete/<int:id>/', views.deleteAdmin, name='delete'),
    path('save/', views.saveAdmin, name='save'),
    path('checkDuplicate/', views.checkDuplicateUsernameAndPhone,
         name='checkDuplicate')
]

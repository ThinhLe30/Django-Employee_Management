from django.contrib import admin
from . import models

class EmployeeAdminArea(admin.AdminSite):
    site_header = 'Employee Management'
    site_title = 'Employee Management'
    index_title = 'Employee Management'
    login_template = 'login.html'

admin_site = EmployeeAdminArea(name='admin')


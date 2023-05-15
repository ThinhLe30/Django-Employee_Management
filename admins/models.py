from django.db import models
from django.contrib.auth.models import AbstractUser
from employees.models import Employee

class AdminApp(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, default=1)
    class Meta:
        db_table = "admins"

    def get_full_name(self):
        return self.employee.firstName + " " + self.employee.lastName
    
    def get_type(self):
        return "Manager" if self.is_superuser else "Employee"

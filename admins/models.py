from django.db import models
from django.contrib.auth.models import AbstractUser
from employees.models import Employee

class AdminApp(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, default=1)
    class Meta:
        db_table = "admins"

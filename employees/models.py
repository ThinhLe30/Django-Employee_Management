from django.db import models
from salaries.models import Level_Salary
from departments.models import Department
class Employee(models.Model):
    firstName = models.CharField(max_length=45)
    lastName = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    birthday = models.DateField()
    address = models.CharField(max_length=500)
    gender = models.BooleanField()
    image = models.FileField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    salary = models.ForeignKey(Level_Salary, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = "employees"
    
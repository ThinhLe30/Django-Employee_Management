from django.shortcuts import render

from employees.models import Employee

# Create your views here.
def showEmployeesList(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees,
    }
    return render(request, "employees.html", context)
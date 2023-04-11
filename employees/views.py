from django.shortcuts import render

# Create your views here.
def showEmployeesList(request):
    return render(request, "employees.html")
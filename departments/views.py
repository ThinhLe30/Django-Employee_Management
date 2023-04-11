from django.shortcuts import render

# Create your views here.
def showDepartmentsList(request):
    return render(request, "departments.html")
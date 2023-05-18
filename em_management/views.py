from django.shortcuts import render

def permission_error(request):
    return render(request, "permission_error.html")
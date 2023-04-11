from django.shortcuts import render,redirect

# Create your views here.
def showHome(request):
    return render(request,"home.html")
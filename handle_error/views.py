from django.shortcuts import render

# Create your views here.
def handle_404(request, exception):
    return render(request, '404.html', status=404)
def handle_500(request):
    return render(request, '500.html', status=500)
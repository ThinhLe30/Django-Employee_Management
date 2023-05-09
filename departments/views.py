from django.shortcuts import render, redirect
from departments.models import Department
from django.db.models import Q
from django.contrib import messages
import math
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

@login_required
def showDepartmentsList(request): 
    per_page = 7  
    keyword = request.GET.get('keyword', "")
    sort = request.GET.get('sort', "asc")
    page_num = int(request.GET.get('page', 1))
    sort_field = request.GET.get('sort_field', "name")

    departments = Department.objects.all()

    if keyword:
        departments = departments.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword) | Q(address__icontains=keyword) | Q(phoneNumber__icontains=keyword))
    if sort == "asc":
        departments = departments.order_by(sort_field)
    else:
        departments = departments.order_by("-"+sort_field)

    total = departments.count()
    total_page = math.ceil(total/per_page)
    start = (page_num - 1) * per_page
    end = page_num * per_page

    if end > total : 
        end = total

    departments = departments[start:end]

    reverse_sort_field = "desc" if sort == "asc" else "asc"

    context = {
        'departments': departments,
        'total_page': total_page,
        'reverse_sort_field': reverse_sort_field,
        'range': range(1, total_page+1),
        'page_num': page_num,
        'keyword' : keyword,
        'sort' : sort,
        'sort_field': sort_field
    }
    return render(request, "departments.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def showDepartmentForm(request, id = 0):
    if id != 0:
        department = Department.objects.get(id=id)
        title = "Update"
    else:
        department = Department()
        title = "Add"

    context = {
            'department': department,
            'title': title,
            'id': id
        }
    return render(request, "department_form.html", context)

@login_required    
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def saveDepartment(request):
    id = int(request.POST.get('id', 0))
    name = request.POST.get('name', "")
    description = request.POST.get('description', "")
    address = request.POST.get('address', "")
    phoneNumber = request.POST.get('phoneNumber', "")
    if id == 0:
        department = Department(name=name, description=description, address=address, phoneNumber=phoneNumber)
        messages.success(request, "Department added successfully.")
    else:
        department = Department(id=id, name=name, description=description, address=address, phoneNumber=phoneNumber)
        messages.success(request, "Department updated successfully.")

    department.save()
    return redirect("/departments/list/?keyword="+name)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def deleteDepartment(request, id):
    department = Department.objects.get(id=id)
    department.delete()
    messages.success(request, "Department deleted successfully.")
    return redirect("/departments/list/")

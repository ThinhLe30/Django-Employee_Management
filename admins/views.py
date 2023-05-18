import math
from django.shortcuts import render
from django.http import JsonResponse
from admins.models import AdminApp
from employees.models import Employee
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def showAdminsList(request):
    per_page = 9
    keyword = request.GET.get('keyword')
    sort = request.GET.get('sort')
    page_num = int(request.GET.get('page', 1))
    sortField = request.GET.get('sortField')
    if not keyword:
        keyword = ""
    if not sort:
        sort = "asc"
    reverseSortField = "desc" if sort == "asc" else "asc"

    if sortField is None:
        sortField = "username"

    if sortField != "username":
        sortField = f"employee__{sortField}"

    admins = AdminApp.objects.all()
    if keyword:
        admins = admins.filter(Q(username__icontains=keyword) | Q(employee__firstName__icontains=keyword) | Q(
            employee__lastName__icontains=keyword) | Q(employee__phone__icontains=keyword))
    if sort == "asc" and sortField:
        admins = admins.order_by(sortField)
    if sort == "desc" and sortField:
        admins = admins.order_by('-'+sortField)
    total = admins.count()
    start = (page_num - 1) * per_page
    end = page_num * per_page
    if end > total:
        end = total
    totalPage = math.ceil(total / per_page)
    admins = admins[start: end]

    context = {
        'admins': admins,
        'total': total,
        'start': start,
        'end': end,
        'totalPage': totalPage,
        'range': range(1, totalPage+1),
        'keyword': keyword,
        'pageNum': page_num,
        'sort': sort,
        'sortField': sortField,
        "reverseSortField": reverseSortField
    }
    return render(request, "admins.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def getDetailOfAdmin(request, id):
    admin = AdminApp.objects.get(pk=id)
    employee = Employee.objects.get(pk=admin.employee_id)
    json = {
        'name': employee.firstName + ' ' + employee.lastName,
        'username': admin.username,
        'email': employee.email,
        'phone': employee.phone,
        'address': employee.address,
        'type': 'Manager' if admin.is_superuser else 'Employee',
    }
    return JsonResponse({'data': json}, safe=False)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def showAdminForm(request, id=0):
    if id == 0:
        admin = AdminApp()
        title = 'Add'
    else:
        admin = AdminApp.objects.get(pk=id)
        title = 'Update'
    
    employees = Employee.objects.all().order_by('firstName')

    context = {
        'admin': admin,
        'title': title,
        'id': id,
        'employees': employees
    }
    return render(request, "admin_form.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def saveAdmin(request):
    if request.method == "POST":
        id = int(request.POST.get('id'))
        username = request.POST.get('username')
        password = request.POST.get('password')

        employee_id = request.POST.get('employee_id')
        is_staff = int(request.POST.get('is_staff'))
        if id == 0:
            admin = AdminApp(username=username)
            admin.set_password(password)
            admin.employee_id = employee_id
            admin.is_staff = is_staff
            admin.is_superuser = 0 if is_staff == 1 else 1
            admin.save()
            messages.success(request, 'Admin account saved successfully.')
        else:
            admin = AdminApp.objects.get(pk=id)
            admin.employee_id = employee_id
            admin.is_staff = is_staff
            admin.is_superuser = 0 if is_staff == 1 else 1
            if(password != ''):
                admin.set_password(password)
            admin.save()
            messages.success(request, 'Admin account updated successfully.')

        # Truyền username vào biến keyword nếu username tồn tại, nếu không truyền chuỗi rỗng
        keyword = username if username else ''
        return redirect(f"/admins/list/?keyword={keyword}")

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def deleteAdmin(request, id):
    admin = AdminApp.objects.get(pk=id)
    admin.delete()
    messages.success(request, 'Admin account deleted successfully.')
    return redirect('/admins/list/')


@csrf_exempt
def checkDuplicateUsernameAndEmployee(request):
    if request.method == 'POST':
        payload = request.body.decode('utf-8')
        data = json.loads(payload)
        id = int(data['id'])
        employee_id = int(data['employee_id'])
        username = data.get('username', None)
        if id == 0:
            if AdminApp.objects.filter(username=username).exists() or AdminApp.objects.filter(employee_id=employee_id).exists():
                response = "Duplicated"
            else:
                response = "Ok"
        else:
            if AdminApp.objects.filter(username=username).exclude(id=id).exists() or AdminApp.objects.filter(employee_id=employee_id).exclude(id=id).exists():
                response = "Duplicated"
            else:
                response = "Ok"
        return JsonResponse(response, safe=False)
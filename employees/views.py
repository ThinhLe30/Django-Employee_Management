import math
from django.shortcuts import render
from django.http import JsonResponse
from salaries.models import Level_Salary
from employees.models import Employee
from departments.models import Department
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

@login_required
def showEmployeesList(request):
    per_page = 7
    keyword = request.GET.get('keyword')
    sort = request.GET.get('sort')
    page_num = int(request.GET.get('page', 1))
    sortField = request.GET.get('sortField')
    if not keyword:
        keyword = ""
    if not sort:
        sort = "asc"
    reverseSortField = "desc" if sort == "asc" else "asc"
    if not sortField:
        sortField = "lastName"
    employees = Employee.objects.all()
    if keyword:
        # | Q(lastName=keyword) | %like Q(phone=keyword) | Q(email=keyword) | Q(birthday=keyword) | Q(address=keyword) | Q(department=keyword) | Q(salary=keyword)
        employees = employees.filter(Q(firstName__icontains=keyword) | Q(lastName__icontains=keyword) | Q(phone__icontains=keyword) | Q(
            email__icontains=keyword) | Q(address__icontains=keyword) | Q(department__name__icontains=keyword))
    if sort == "asc" and sortField:
        employees = employees.order_by(sortField)
    if sort == "desc" and sortField:
        employees = employees.order_by('-'+sortField)
    total = employees.count()
    start = (page_num - 1) * per_page
    end = page_num * per_page
    if end > total:
        end = total
    totalPage = math.ceil(total / per_page)
    employees = employees[start: end]

    context = {
        'employees': employees,
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
    return render(request, "employees.html", context)

@login_required
def getDetailOfEmployee(request, id):
    employee = Employee.objects.get(pk=id)
    json = {
        'name': employee.firstName + ' ' + employee.lastName,
        'email': employee.email,
        'birthday': employee.birthday,
        'address': employee.address,
        'gender': employee.gender,
        'phone': employee.phone,
        'image': str(employee.image),
        'department': employee.department.name,
        'salary': employee.salary.basicSalary
    }
    return JsonResponse({'data': json}, safe=False)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def showEmployeeForm(request, id=0):
    if id == 0:
        employee = Employee()
        title = 'Add'
    else:
        employee = Employee.objects.get(pk=id)
        title = 'Update'
    departments = Department.objects.all().order_by('name')
    salaries = Level_Salary.objects.all().order_by('basicSalary')
    context = {
        'employee': employee,
        'departments': departments,
        'salaries': salaries,
        'title': title,
        'id': id
    }
    return render(request, "employee_form.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def saveEmployee(request):
    if request.method == "POST":
        id = int(request.POST.get('id'))
        firstName = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        birthday = request.POST.get('birthday')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        gender = True if gender == '1' else False
        phone = request.POST.get('phone')
        image_file = request.FILES.get('image')
        id_department = int(request.POST.get('id_department'))
        id_salary = int(request.POST.get('id_salary'))
        if image_file:
            with open(f"static/image/avatar/{image_file.name}", 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

        if id == 0:
            employee = Employee(firstName=firstName, lastName=lastname, email=email, birthday=birthday, address=address, gender=gender,
                                phone=phone, image=image_file.name if image_file else 'default.jpg', department_id=id_department, salary_id=id_salary)
            employee.save()
            messages.success(request, 'Employee saved successfully.')
        else:
            employee = Employee.objects.get(pk=id)
            employee.firstName = firstName
            employee.lastName = lastname
            employee.email = email
            employee.birthday = birthday
            employee.address = address
            employee.gender = gender
            employee.phone = phone
            employee.department_id = id_department
            employee.salary_id = id_salary
            employee.image = image_file.name if image_file else employee.image
            employee.save()
            messages.success(request, 'Employee edited successfully.')
        return redirect("/employees/list/?keyword="+email)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def deleteEmployee(request, id):
    employee = Employee.objects.get(pk=id)
    employee.delete()
    messages.success(request, 'Employee deleted successfully.')
    return redirect('/employees/list/')

@csrf_exempt
def checkDuplicateEmailAndPhone(request):
    if request.method == 'POST':
        payload = request.body.decode('utf-8')
        data = json.loads(payload)
        id = int(data['id'])
        email = data['email']
        phone = data['phone']
        if id == 0:
            if Employee.objects.filter(email=email).exists() | Employee.objects.filter(phone=phone).exists():
                response = "Duplicated"
            else:
                response = "Ok"
        else:
            if Employee.objects.filter(email=email).exclude(id=id).exists() | Employee.objects.filter(phone=phone).exclude(id=id).exists():
                response = "Duplicated"
            else:
                response = "Ok"
        return JsonResponse(response, safe=False)

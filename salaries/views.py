import math
from django.shortcuts import render
from django.http import JsonResponse
from salaries.models import Level_Salary
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

@login_required
def showLevel_SalariesList(request):
    per_page = 7
    keyword = request.GET.get('keyword')
    sort = request.GET.get('sort')
    page_num = int(request.GET.get('page',1))
    sortField = request.GET.get('sortField')
    if not keyword:
        keyword =""
    if not sort:
        sort = "asc"
    reverseSortField = "desc" if sort == "asc" else "asc" 
    if not sortField:
        sortField = "basicSalary"
    level_salaries = Level_Salary.objects.all()

    for level_salarie in level_salaries:
        level_salarie.basicSalary = str(int(level_salarie.basicSalary))
    if keyword:
        # | Q(lastName=keyword) | %like Q(phone=keyword) | Q(email=keyword) | Q(birthday=keyword) | Q(address=keyword) | Q(department=keyword) | Q(salary=keyword)
         level_salaries =  level_salaries.filter(Q( basicSalary__icontains=keyword.split('.')[0]) | Q(coefficientPay__icontains=keyword) | Q(coefficientAllowance__icontains=keyword) )
    if sort == "asc" and sortField:
        level_salaries = level_salaries.order_by(sortField)
    if sort == "desc" and sortField:
        level_salaries = level_salaries.order_by('-'+sortField)
    total = level_salaries.count()
    start = (page_num - 1) * per_page
    end = page_num * per_page
    if end > total : 
        end = total
    totalPage = math.ceil(total / per_page)
    level_salaries = level_salaries[start : end]

    context = {
        'level_salaries': level_salaries,
        'total' : total,
        'start' : start,
        'end' : end,
        'totalPage' : totalPage,
        'range' : range(1,totalPage+1),
        'keyword' : keyword,
        'pageNum' : page_num,
        'sort' : sort,
        'sortField' : sortField,
        "reverseSortField" : reverseSortField
    }
    return render(request, "salaries.html", context)


@login_required
def getDetailOfLevel_Salary(request, id):
    level_salary = Level_Salary.objects.get(pk=id)
    json = {
        'basicSalary' : level_salary.basicSalary ,
        'coefficientPay' : level_salary.coefficientPay,
        'coefficientAllowance' : level_salary.coefficientAllowance,
    }
    return JsonResponse({'data' : json}, safe=False)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def showLevel_SalaryForm(request,id =0):
    if id == 0:
        level_salary = Level_Salary()
        title = 'Add'
    else:
        level_salary = Level_Salary.objects.get(pk=id)
        title = 'Update'
  
    context = {
            'level_salary' : level_salary,
            'id': id,
            'title': title
        }
    return render(request, "salaries_form.html", context)

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def saveLevel_Salary(request):
    if request.method == "POST":
        id = int(request.POST.get('id'))
        basicSalary = request.POST.get('basicSalary')
        coefficientPay = request.POST.get('coefficientPay')
        coefficientAllowance = request.POST.get('coefficientAllowance') 
      
        
        if id == 0:
            salary = Level_Salary(basicSalary=basicSalary, coefficientPay=coefficientPay, coefficientAllowance=coefficientAllowance)
            salary.save()
            messages.success(request, 'Salary level saved successfully.')
        else:
            salary = Level_Salary.objects.get(pk=id)
            salary.basicSalary = basicSalary
            salary.coefficientPay = coefficientPay
            salary.coefficientAllowance = coefficientAllowance
            salary.save()
            messages.success(request, 'Salary level edited successfully.')
        # return render(request, "checkform.html", context)
        return redirect("/salaries/list/?keyword="+ basicSalary.split('.')[0])

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='permission_error')
def deleteLevel_Salary(request, id):
    salary = Level_Salary.objects.get(pk=id)
    salary.delete()
    messages.success(request, 'Salary level deleted successfully.')
    return redirect('/salaries/list/')

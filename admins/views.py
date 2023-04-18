import math
from django.shortcuts import render
from django.http import JsonResponse
from admins.forms import AdminForm
from admins.models import AdminApp
from django.core import serializers
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json


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
    if not sortField:
        sortField = "last_name"
    admins = AdminApp.objects.all()
    if keyword:
        admins = admins.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword) | Q(
            last_name__icontains=keyword) | Q(phone__icontains=keyword))
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


def getDetailOfAdmin(request, id):
    admin = AdminApp.objects.get(pk=id)
    json = {
        'name': admin.first_name + ' ' + admin.last_name,
        'username': admin.username,
        'password': admin.password,
        'phone': admin.phone,
    }
    return JsonResponse({'data': json}, safe=False)


def showAdminForm(request, id=0):
    if id == 0:
        admin = AdminApp()
        title = 'Add'
    else:
        admin = AdminApp.objects.get(pk=id)
        title = 'Update'
    context = {
        'admin': admin,
        'title': title,
        'id': id
    }
    return render(request, "admin_form.html", context)


def saveAdmin(request):
    if request.method == "POST":
        id = int(request.POST.get('id'))
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        if id == 0:
            admin = AdminApp(first_name=first_name, last_name=last_name,
                             username=username, password=password, phone=phone)
            admin.save()
            messages.success(request, 'The admin was saved successfully.')
        else:
            admin = AdminApp.objects.get(pk=id)
            admin.first_name = first_name
            admin.last_name = last_name
            admin.password = password
            admin.phone = phone
            admin.save()
            messages.success(request, 'The admin was edited successfully.')

        # Truyền username vào biến keyword nếu username tồn tại, nếu không truyền chuỗi rỗng
        keyword = username if username else ''
        return redirect(f"/admins/list/?keyword={keyword}")


def deleteAdmin(request, id):
    admin = AdminApp.objects.get(pk=id)
    admin.delete()
    messages.success(request, 'The admin was deleted successfully.')
    return redirect('/admins/list/')


@csrf_exempt
def checkDuplicateUsernameAndPhone(request):
    if request.method == 'POST':
        payload = request.body.decode('utf-8')
        data = json.loads(payload)
        id = int(data['id'])
        phone = data['phone']
        username = data.get('username', None)
        if id == 0:
            if AdminApp.objects.filter(username=username).exists() or AdminApp.objects.filter(phone=phone).exists():
                response = "Duplicated"
            else:
                response = "Ok"
        else:
            if AdminApp.objects.filter(username=username).exclude(id=id).exists() or AdminApp.objects.filter(phone=phone).exclude(id=id).exists():
                response = "Duplicated"
            else:
                response = "Ok"
        return JsonResponse(response, safe=False)
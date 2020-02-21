from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from people.models import Employee
from order.models import Order
from vendor.models import Meal, Vendor
import json

@login_required
def main_view(request):
    if request.method == 'GET':
        current_user = request.user
        if current_user.is_superuser:
            return HttpResponseRedirect('/admin/')
        else:
            if current_user.team is not None and current_user.team.executor == current_user:
                return HttpResponseRedirect('manager/')
            else:
                return HttpResponseRedirect('employee/')


@login_required
def employee_view(request):
    if request.method == 'GET':
        current_user = request.user
        try:
            current_employee = Employee.objects.get(user=current_user)
            context = current_employee.get_stats()
            context['order_history'] = Order.get_order_history(current_user)
            context['active_order'] = Order.get_active_order(current_user)

            team = current_user.team
            if team is not None:
                vendors = team.vendors
                context['vendors'] = [v.json_format() for v in vendors]
                context['error'] = ''
            else:
                vendors = Vendor.objects.all()
                context['vendors'] = [v.json_format() for v in vendors]
                context['error'] = 'Please assign a team to your account'

        except Employee.DoesNotExist:
            context = {'error': 'Please have your manager to register you as Employee'}

        return render(request, 'project_specific/employee.html', context=context)
    elif request.method == 'POST':
        str_data = request.body
        str_data = str_data.decode('utf-8')
        json_data = json.loads(str_data)

        if json_data['action'] == 'request_meal':
            vendor = Vendor.objects.get(pk=int(json_data['vendor_pk']))
            meals = Meal.objects.filter(vendor=vendor)
            meals = [m.json_format() for m in meals]
            print('meals ', meals)
            return HttpResponse(json.dumps(meals), content_type='application/json')


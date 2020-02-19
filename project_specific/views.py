from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from people.models import Employee
from order.models import Order


# @login_required
def main_view(request):
    if request.method == 'GET':
        current_user = request.user
        if current_user.is_superuser:
            return HttpResponseRedirect('/admin/')
        else:
            if current_user.group.executor == current_user:
                return HttpResponseRedirect('/manager/')
            else:
                return HttpResponseRedirect('/employee/')


# @login_required
def employee_view(request):
    if request.method == 'GET':
        current_user = request.user
        current_employee = Employee.objects.get(user=current_user)
        if current_employee:
            context = current_employee.get_stats()
            context['order_history'] = Order.get_order_history(current_user)
            context['error'] = ''
        else:
            context = {'error': 'Please have your manager to register you as Employee'}
        return render(request, 'project_specific/employee.html', context=context)


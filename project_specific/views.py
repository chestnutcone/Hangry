from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from people.models import Employee
from order.models import Order
from vendor.models import Meal, Vendor
import json
from user.models import CustomUser
import datetime
import csv

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
    current_user = request.user
    if request.method == 'GET':
        try:
            current_employee = Employee.objects.get(user=current_user)
            context = current_employee.get_stats()
            context['order_history'] = Order.get_order_history(current_user)
            context['active_order'] = Order.get_active_order(current_user)

            team = current_user.team
            if team is not None:
                vendors = team.vendors
                context['vendors'] = [v.json_format() for v in vendors.all()]
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
            return HttpResponse(json.dumps(meals), content_type='application/json')
        elif json_data['action'] == 'order_meal':
            ordered_meal = Order.add_order(current_user, json_data['meal_pk'], json_data['notes'])
            ordered_meal = ordered_meal.json_format()
            return HttpResponse(json.dumps(ordered_meal), content_type='application/json')


@user_passes_test(lambda u: u.team.executor == u)
def manager_view(request):
    current_user = request.user
    if request.method == 'GET':
        response = Order.order_summary(current_user.team)
        return render(request, 'project_specific/manager.html', context=response)
    elif request.method == "POST":
        str_data = request.body
        str_data = str_data.decode('utf-8')
        json_data = json.loads(str_data)

        if json_data['action'] == 'place_meal_order':
            Order.place_meal_order(json_data["meals_pk"])
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        elif json_data['action'] == 'fetch_past_orders':
            order_history = Order.get_team_history(current_user.team,
                                                   json_data['start_date'],
                                                   json_data['end_date'])
            return HttpResponse(json.dumps({'order_history': order_history}), content_type='application/json')


@user_passes_test(lambda u: u.team.executor == u)
def manager_people_view(request):
    current_user = request.user
    if request.method == 'GET':
        unregistered_users = CustomUser.objects.filter(team=None).exclude(is_superuser=True)
        unregistered_users = [u.json_format() for u in unregistered_users]

        team_users = Employee.objects.filter(user__team=current_user.team)
        team_users = [t.json_format() for t in team_users]

        context = {'unregistered_users': unregistered_users,
                   'team_users': team_users}
        return render(request, 'project_specific/manager_people.html', context=context)
    elif request.method == 'POST':
        str_data = request.body
        str_data = str_data.decode('utf-8')
        json_data = json.loads(str_data)

        if json_data['action'] == 'remove_user_from_team':
            remove_members_pk = json_data['user_pk']

            for pk in remove_members_pk:
                user = CustomUser.objects.get(pk=pk)
                user.team = None
                user.save()

            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        elif json_data['action'] == 'add_user_to_team':
            add_members_pk = json_data['user_pk']

            for pk in add_members_pk:
                user = CustomUser.objects.get(pk=pk)
                user.team = current_user.team
                user.save()

            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')


@user_passes_test(lambda u: u.team.executor == u)
def manager_download_view(request, start_date, end_date):
    current_user = request.user
    response = HttpResponse(content_type='text/csv')
    if end_date == "":
        end_date_str = datetime.datetime.now() + datetime.timedelta(days=1)
        end_date_str = str(end_date_str.date())
    else:
        end_date_str = end_date
    filename = "{}_{}_orders.csv".format(start_date, end_date_str)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    order_history = Order.get_team_history(current_user.team,
                                           start_date,
                                           end_date)
    writer = csv.writer(response, )
    title = ['vendor', 'meal', 'price', 'customer', 'notes', 'ordered', 'timestamp', 'order_failed_reason']
    writer.writerow(title)
    for order in order_history:
        writer.writerow([order[t] for t in title])
    return response


from django.db import models
from people.models import Employee
from vendor.models import Meal
from user.models import Team
from organization.models import Organization
import datetime
import pandas as pd
import pytz
from dateutil.parser import parse


# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE)
    team = models.ForeignKey(Team,
                             on_delete=models.SET_NULL,
                             null=True)
    meal = models.ForeignKey(Meal,
                             on_delete=models.SET_NULL,
                             null=True)
    notes = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    order_failed_reason = models.CharField(max_length=100)

    def json_format(self, timezone=None):
        if not timezone:
            timezone = Organization.objects.all()[0].timezone  # only one can exist
            timezone = pytz.timezone(str(timezone))

        return {'customer': str(self.customer),
                'meal': self.meal.name,
                'vendor': self.meal.vendor.name,
                'price': self.meal.price,
                'notes': self.notes,
                'ordered': str(self.ordered),
                'timestamp': str(self.timestamp.astimezone(timezone)), # display time as local to organization
                'pk': self.pk,
                'order_failed_reason': self.order_failed_reason
                }

    @staticmethod
    def order_summary(team):
        timezone = Organization.get_organization_timezone()

        today = Organization.get_today_start_utc()
        unordered = Order.objects.filter(team=team,
                                         timestamp__gte=today,
                                         ordered=False)
        unordered_json = [u.json_format(timezone) for u in unordered]

        all_orders = Order.objects.filter(team=team,
                                         timestamp__gte=today)
        all_orders_json = [o.json_format(timezone) for o in all_orders]

        if len(unordered_json):
            unordered_df = pd.DataFrame(unordered_json)

            unordered_df['price'] = unordered_df['price'].astype('float32')
            meals_by_vendors = unordered_df.groupby(["vendor", "meal"]).size().to_dict()
            meals_by_vendors_json = {}
            for (vendor, meal), v in meals_by_vendors.items():
                try:
                    meals_by_vendors_json[vendor][meal] = v
                except KeyError:
                    meals_by_vendors_json[vendor] = {meal: v}

            total_owning_by_vendors_json = unordered_df.groupby("vendor").sum().to_dict()
        else:
            meals_by_vendors_json = {'': {'': ''}}
            total_owning_by_vendors_json = {'': ''}

        vendor_info = [v.json_format() for v in team.vendors.all()]

        return {'meals_by_vendors': meals_by_vendors_json,
                'total_owning_by_vendors': total_owning_by_vendors_json,
                'vendor_info': vendor_info,
                'detail_order_info': sorted(all_orders_json, key=lambda x: (x['vendor'], x['meal']))}

    @staticmethod
    def add_order(user, meal_pk, notes):
        if meal_pk and notes:
            meal_pk = int(meal_pk)
            try:
                current_employee = Employee.objects.get(user=user)
                ordered_meal = Order(customer=current_employee,
                                     team=user.team,
                                     meal=Meal.objects.get(pk=meal_pk),
                                     notes=notes)
                ordered_meal.save()
                return ordered_meal
            except Employee.DoesNotExist:
                pass
        return []

    @staticmethod
    def get_order_history(user, days=30):
        # gets past ordered history
        timezone = Organization.get_organization_timezone()

        today = Organization.get_today_start_utc()
        cutoff = today - datetime.timedelta(days=days)
        order_history = Order.objects.filter(customer__user=user,
                                             timestamp__gte=cutoff,
                                             ordered=True)
        order_list = [order.json_format(timezone) for order in order_history]
        return order_list

    @staticmethod
    def get_team_history(team, start_date, end_date):
        """only executor of the team will call this function to get the team's history"""
        timezone = Organization.get_organization_timezone()

        start_date = parse(start_date)
        if end_date == "":
            end_date = datetime.datetime.now() + datetime.timedelta(days=1)
            end_date = end_date.date()
        else:
            end_date = parse(end_date)

        start_utc = Organization.convert_to_utc(start_date)
        end_utc = Organization.convert_to_utc(end_date)

        order_history = Order.objects.filter(team=team,
                                             timestamp__gte=start_utc).filter(timestamp__lte=end_utc)
        order_list = [o.json_format(timezone) for o in order_history]
        return order_list

    @staticmethod
    def get_active_order(user):
        timezone = Organization.get_organization_timezone()
        # get active order for today
        cutoff = Organization.get_today_start_utc()
        active_order = Order.objects.filter(customer__user=user,
                                            timestamp__gte=cutoff,
                                            ordered=False)
        order_list = [order.json_format(timezone) for order in active_order]
        return order_list

    @staticmethod
    def place_meal_order(meals_pk):
        for order_pk in meals_pk:
            order = Order.objects.get(pk=order_pk)
            customer = order.customer
            price = order.meal.price

            if not order.ordered:
                if customer.withdrawal(price):
                    order.ordered = True
                else:
                    order.order_failed_reason = "Insufficient funds. Balance {}".format(customer.balance)
                order.save()

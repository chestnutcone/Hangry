from django.db import models
from people.models import Employee
from vendor.models import Meal
from user.models import Team
import datetime


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
    timestamp = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField()

    def json_format(self):
        return {'customer': str(self.customer),
                'team': self.team.name,
                'meal': self.meal.name,
                'vendor': self.meal.vendor.name,
                'price': self.meal.price,
                'timestamp': str(self.timestamp)
                }

    @staticmethod
    def get_order_history(user, days=30):
        # gets past ordered history
        cutoff = datetime.date.today() - datetime.timedelta(days=days)
        order_history = Order.objects.filter(customer__user=user,
                                             timestamp__gte=cutoff,
                                             ordered=True)
        order_list = [order.json_format() for order in order_history]
        return order_list

    @staticmethod
    def get_active_order(user):
        # get active order for today
        cutoff = datetime.date.today()
        active_order = Order.objects.filter(customer__user=user,
                                            timestamp__gte=cutoff,
                                            ordered=False)
        order_list = [order.json_format() for order in active_order]
        return order_list

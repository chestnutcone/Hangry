from django.db import models
from people.models import Employee
from vendor.models import Meal
from user.models import Group
import datetime


# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE)
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              null=True)
    meal = models.ForeignKey(Meal,
                             on_delete=models.SET_NULL,
                             null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def json_format(self):
        return {'customer': str(self.customer),
                'group': self.group.name,
                'meal': self.meal.name,
                'timestamp': str(self.timestamp)
                }

    @staticmethod
    def get_order_history(user, days=30):
        cutoff = datetime.date.today() - datetime.timedelta(days=days)
        order_history = Order.objects.filter(customer__user=user,
                                             timestamp__gte=cutoff)
        order_list = [order.json_format() for order in order_history]
        return {'order_history': order_list}

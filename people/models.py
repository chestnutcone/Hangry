from django.db import models
from user.models import CustomUser


class Employee(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                primary_key=True)
    balance = models.FloatField(default=0)

    def json_format(self):
        return {'name': str(self.user),
                'email': str(self.user.username),
                'balance': str(self.balance),
                'pk': str(self.user.pk)}

    def withdrawal(self, amount):
        if amount >=0:
            new_balance = self.balance - amount
            if new_balance >= 0:
                self.balance = new_balance
                self.save()
                return True
        return False

    def deposit(self, amount):
        if amount >= 0:
            self.balance = self.balance + amount
            self.save()
            return True
        return False

    def __str__(self):
        return str(self.user)

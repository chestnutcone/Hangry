from django.db import models
from user.models import CustomUser

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                primary_key=True)
    balance = models.FloatField(default=0)

    def withdrawal(self, amount):
        if amount >=0:
            new_balance = self.balance - amount
            if new_balance >= 0:
                self.balance = new_balance
                return True
        return False

    def deposit(self, amount):
        if amount >= 0:
            self.balance = self.balance + amount
            return True
        return False
    
    def get_stats(self):
        return {'balance': self.balance,
                }

    def __str__(self):
        return str(self.user)

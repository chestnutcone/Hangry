from django.db import models
from user.models import CustomUser
from organization.models import Organization
import pytz


class Employee(models.Model):
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                primary_key=True)
    balance = models.FloatField(default=0)

    def json_format(self):
        return {'name': str(self.user),
                'email': str(self.user.username),
                'balance': str(self.balance),
                'pk': str(self.user.pk),
                'team': str(self.user.team)}

    def withdrawal(self, amount):
        if amount >=0:
            new_balance = self.balance - amount
            if new_balance >= 0:
                self.balance = new_balance
                self.save()
                new_transaction = Transaction(employee=self,
                                              transaction_amount=-amount,
                                              balance_after=self.balance)
                new_transaction.save()
                return True
        return False

    def deposit(self, amount):
        if amount >= 0:
            self.balance = self.balance + amount
            self.save()
            new_transaction = Transaction(employee=self,
                                          transaction_amount=amount,
                                          balance_after=self.balance)
            new_transaction.save()
            return True
        return False

    def get_transaction_history(self, start_date=None, end_date=None):
        return Transaction.get_transaction_history(self, start_date=start_date, end_date=end_date)

    @staticmethod
    def get_employee(user_pk):
        try:
            user = CustomUser.objects.get(pk=user_pk)
            employee = Employee.objects.get(user=user)
            return employee
        except CustomUser.DoesNotExist:
            return None
        except Employee.DoesNotExist:
            return None

    def __str__(self):
        return str(self.user)


class Transaction(models.Model):
    employee = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE,
                                 null=False)
    transaction_amount = models.FloatField(default=0)
    balance_after = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def json_format(self, timezone=None):
        if not timezone:
            timezone = Organization.objects.all()[0].timezone  # only one can exist
            timezone = pytz.timezone(str(timezone))
        return {'name': str(self.employee.user),
                'transaction_amount': self.transaction_amount,
                'balance_after': self.balance_after,
                'timestamp': str(self.timestamp.astimezone(timezone))}

    @staticmethod
    def get_transaction_history(employee, start_date=None, end_date=None):
        """takes employee instance"""
        if start_date and end_date:
            transaction_history = Transaction.objects.filter(employee=employee,
                                                             timestamp__gte=start_date,
                                                             timestamp__lte=end_date)
        else:
            transaction_history = Transaction.objects.filter(employee=employee)
        timezone = Organization.objects.all()[0].timezone  # only one can exist
        timezone = pytz.timezone(str(timezone))
        transaction_history = [h.json_format(timezone) for h in transaction_history]
        return transaction_history


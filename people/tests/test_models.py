from django.test import TestCase
from people.models import Employee, Transaction
from user.models import CustomUser, Team


class PeopleTestCase(TestCase):
    def setUp(self):
        employee_user = CustomUser.objects.create(username='employee')
        employee = Employee.objects.create(user=employee_user)

    def test_employee_withdrawal(self):
        employee_user = CustomUser.objects.get(username='employee')
        employee = Employee.objects.get(user=employee_user)

        # newly created object have default 0 balance
        self.assertEqual(employee.balance, 0.0)

        # cannot withdrawal if no balance less than withdrawal amount
        result = employee.withdrawal(10)
        self.assertEqual(result, False)

        # cannot withdrawal negative amount
        result = employee.withdrawal(-10)
        self.assertEqual(result, False)

        # can withdrawal 0
        result = employee.withdrawal(0)
        self.assertEqual(result, True)

        # cannot deposit negative
        result = employee.deposit(-10)
        self.assertEqual(result, False)

        # can deposit 0
        result = employee.deposit(0)
        self.assertEqual(result, True)

        # can deposit positive
        result = employee.deposit(10)
        self.assertEqual(result, True)
        self.assertEqual(employee.balance, 10.0)

        # can withdrawal positive amount of balance supports
        result = employee.withdrawal(10)
        self.assertEqual(result, True)
        self.assertEqual(employee.balance, 0.0)





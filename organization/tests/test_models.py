from django.test import TestCase
from organization.models import Organization, Timezone
import pytz
from django.core.exceptions import ValidationError

class OrganizationTestCase(TestCase):
    def setUp(self):
        org = Organization.objects.create(name='test_org')
        common_timezones = list(pytz.common_timezones)
        common_timezones.remove('GMT')
        common_timezones.remove('UTC')

        from organization.models import Timezone
        for tz in common_timezones:
            Timezone.objects.create(name=tz.strip())

    def test_one_organization(self):
        with self.assertRaises(ValidationError):
            Organization.objects.create(name='second_org')
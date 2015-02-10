from django.test import TestCase
from reporting.models import auto_chart_type

# Create your tests here.
class ModelUtilTest(TestCase):
    def test_charttype(self):
        chart_type = auto_chart_type("get users")
        self.assertEqual("pie", chart_type)

        chart_type = auto_chart_type("get commits")
        self.assertEqual("bar", chart_type)
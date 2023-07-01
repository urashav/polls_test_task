from django.test import TestCase
import django
import rest_framework
import drf_yasg


class VersionOfIncludedPackagesTestCase(TestCase):
    """ Тест на соответствие версий, входящий в проект пакетов. """

    def test_django_version(self):
        self.assertEqual((2, 2, 10, 'final', 0), django.VERSION)

    def test_rest_framework_version(self):
        self.assertEqual('3.11.0', rest_framework.VERSION)

    def test_drf_yasg_version(self):
        self.assertEqual('1.17.1', drf_yasg.__version__)

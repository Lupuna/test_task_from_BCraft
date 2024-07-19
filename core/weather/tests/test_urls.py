from django.test import SimpleTestCase
from django.urls import resolve, reverse
from weather.views import GetParisWeatherAPIView


class TestUrls(SimpleTestCase):
    def test_create_company_url_is_resolve(self):
        url = reverse('get_parish_weather')
        self.assertEqual(resolve(url).func.view_class, GetParisWeatherAPIView)
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from django.core.cache import cache


def mock_get_weather_open_meteo(lat, lon):
    return {
        "current_weather": {
            "temperature": 29.6,
            "winddirection": 155,
            "windspeed": 8.4
        },
        "hourly": {
            "soil_moisture_0_to_1cm": [0.12, 0.15, 0.13, 0.10, 0.09, 0.08, 0.11]
        },
        "current_weather_units": {
            "temperature": "°C",
            "winddirection": "°",
            "windspeed": "km/h"
        },
        "hourly_units": {
            "soil_moisture_0_to_1cm": "%"
        }
    }


@patch('weather.views.get_weather_open_meteo', side_effect=mock_get_weather_open_meteo)
class GetParisWeatherAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('get_parish_weather')
        cache.clear()

    def test_get_weather_from_api(self, mock_get_weather_open_meteo):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertIn('values', data)
        self.assertIn('units', data)
        self.assertEqual(data['values']['temperature'], 29.6)
        self.assertEqual(data['values']['moisture'], 0.11)
        self.assertEqual(data['values']['winddirection'], 155)
        self.assertEqual(data['values']['windspeed'], 8.4)
        self.assertEqual(data['units']['temperature'], "°C")
        self.assertEqual(data['units']['moisture'], "%")
        self.assertEqual(data['units']['winddirection'], "°")
        self.assertEqual(data['units']['windspeed'], "km/h")

    def test_get_weather_from_cache(self, mock_get_weather_open_meteo):
        self.client.get(self.url)

        with patch('weather.views.get_weather_open_meteo') as mock_get_weather_open_meteo_cached:
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = response.json()

            self.assertIn('values', data)
            self.assertIn('units', data)
            self.assertEqual(data['values']['temperature'], 29.6)
            self.assertEqual(data['values']['moisture'], 0.11)
            self.assertEqual(data['values']['winddirection'], 155)
            self.assertEqual(data['values']['windspeed'], 8.4)
            self.assertEqual(data['units']['temperature'], "°C")
            self.assertEqual(data['units']['moisture'], "%")
            self.assertEqual(data['units']['winddirection'], "°")
            self.assertEqual(data['units']['windspeed'], "km/h")

            mock_get_weather_open_meteo_cached.assert_not_called()

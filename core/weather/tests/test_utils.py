from django.test import TestCase
from weather.utils import get_weather_open_meteo, get_coordinates


class TestUtils(TestCase):

    def setUp(self) -> None:
        self.city = 'Paris'
        self.lat = 48.9
        self.lon = 2.3

    def test_get_coordinates(self):
        with self.subTest('has city'):
            coordinates = get_coordinates(self.city)
            lat = round(float(coordinates[0]), 1)
            lon = round(float(coordinates[-1]), 1)
            self.assertEqual((lat, lon), (self.lat, self.lon))
        with self.subTest('has no city'):
            self.assertEqual(get_coordinates('fsdughsdfglkjdsghsdpkgs'), (None, None))

    def test_get_weather_open_meteo(self):
        data_keys = ['latitude', 'longitude', 'generationtime_ms', 'utc_offset_seconds',
                     'timezone', 'timezone_abbreviation', 'elevation', 'hourly',
                     'current_weather_units', 'current_weather', 'hourly_units']
        [self.assertIn(key, data_keys) for key in get_weather_open_meteo(self.lat, self.lon).keys()]


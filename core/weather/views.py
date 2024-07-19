from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from weather.utils import get_coordinates, get_weather_open_meteo
from django.core.cache import cache


class GetParisWeatherAPIView(APIView):
    city = "Paris"

    def get(self, request, *args, **kwargs):
        cache_key = settings.CITY_PARIS_CACHE
        data = cache.get(cache_key)

        if not data:
            lat, lon = get_coordinates(self.city)
            if not lat or not lon:
                raise ValidationError('This city has no latitude or longitude')

            all_weather_data = get_weather_open_meteo(lat, lon)

            data = {
                'values': {
                    'temperature': all_weather_data['current_weather'].get('temperature'),
                    'moisture': all_weather_data['hourly'].get('soil_moisture_0_to_1cm')[-1],
                    'winddirection': all_weather_data['current_weather'].get('winddirection'),
                    'windspeed': all_weather_data['current_weather'].get('windspeed')
                },
                'units': {
                    'temperature': all_weather_data['current_weather_units'].get('temperature'),
                    'moisture': all_weather_data['hourly_units'].get('soil_moisture_0_to_1cm'),
                    'winddirection': all_weather_data['current_weather_units'].get('winddirection'),
                    'windspeed': all_weather_data['current_weather_units'].get('windspeed')
                }
            }

            cache.set(cache_key, data, 60 * 5)

        return Response(data, status=status.HTTP_200_OK)
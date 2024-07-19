from django.urls import path
from weather.views import GetParisWeatherAPIView


urlpatterns = [
    path('', GetParisWeatherAPIView.as_view(), name='get_parish_weather'),
]

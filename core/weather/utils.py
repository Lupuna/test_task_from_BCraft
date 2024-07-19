import requests
from django.conf import settings


def get_coordinates(city):
    geocode_url = settings.GEOCODE_URL.format(city=city)
    response = requests.get(
        geocode_url,
        headers={
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; Touch)'
        }
    )
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        return None, None


def get_weather_open_meteo(lat, lon):
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': 'true',
        'timezone': 'auto',
        'hourly': 'soil_moisture_0_to_1cm',
    }
    response = requests.get(settings.OPEN_METEO_URL, params=params)
    return response.json()
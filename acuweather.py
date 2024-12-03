import requests
import json
from datetime import datetime

api_key = "YAXJ2BgVH2LFs9nH0O9WZFYUjfkV4nXm"

# Полученим ключ для определения  кода города по координатам
def lock_key_by_cords(latitude, longitude):
    location_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    params = {
        "apikey": api_key,
        "q": f"{latitude},{longitude}"  # Например, "40.7128,-74.0060" для Нью-Йорка
    }
    response = requests.get(location_url, params=params)
    response = response.json()

    code = response.get('Code')
    if code == 'ServiceUnavailable':
        return {
            'success': False,
            'error': response.get('Message')
        }

    location_key = response.get('Key')
    return {
            'success': True,
            'key': location_key
        }
# наверно есть какой-то смысл почему у них код города, а не название  Хотя повторы..

print(lock_key_by_cords(40.7128,-74.0060))
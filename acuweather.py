import requests
import json
from datetime import datetime

api_key = "YAXJ2BgVH2LFs9nH0O9WZFYUjfkV4nXm"

# Полученим ключ для определения кода города по координатам
def lock_key_by_cords(latitude, longitude):
    location_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    params = {
        "apikey": api_key,
        "q": f"{latitude},{longitude}"
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

# Получение погоды по ключу, который получили выще
def get_weather(location_key):
    params = {
        "apikey": api_key,
        "details": True,
        'metric': True
    }
    url = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}'
    response = requests.get(url, params=params)
    return response.json()


def main():
    # Возьму в качестве примера Тулу
    latitude = 54.1961
    longitude = 37.6182
    result = lock_key_by_cords(latitude, longitude)

    if result['success']:
        location_key = result['key']
        weather = get_weather(location_key)
        weather_json = {
            'cord': f"{latitude}; {longitude}",
            'date': datetime.now().strftime("%d-%m-%Y"),
            'temperature': int(
                (weather['DailyForecasts'][0]['Temperature']['Minimum']['Value'] +
                 weather['DailyForecasts'][0]['Temperature']['Maximum']['Value'])/2),
            'relative_humidity': int(weather['DailyForecasts'][0]['Day']['RelativeHumidity']['Average']),
            'precipitation_probability': int(weather['DailyForecasts'][0]['Day']['PrecipitationProbability']),
            'wind_speed': int(weather['DailyForecasts'][0]['Day']['Wind']['Speed']['Value'])}
        print(weather_json)
        with open('accu.json', 'w') as f:
            json.dump(weather_json, f, indent=4)
    else:
        print(result['error'])


# Оценка погодных условий
def weather_quality(weather):
    bad_conditions = []
    if weather['temperature'] < 0:
        bad_conditions.append(f"Температура слишком низкая: {weather['temperature']}")
    if weather['temperature'] > 35:
        bad_conditions.append(f"Температура слишком большая: {weather['temperature']}")
    if weather['wind_speed'] >= 40:
        bad_conditions.append(f"Скорость ветра слишком большая: {weather['wind_speed']} метров в секунду")
    if weather['precipitation_probability'] > 70:
        bad_conditions.append(f"Вероятность выпадения осадков слишком высока: {weather['precipitation_probability']}%")
    if weather['relative_humidity'] > 80:
        bad_conditions.append(f"Слишком большая влажность: {weather['relative_humidity']}%")

    return bad_conditions


if __name__ == '__main__':
    main()


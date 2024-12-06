import requests
import json
from datetime import datetime
from pprint import pprint

from geopy.geocoders import Nominatim

# api_key = "YAXJ2BgVH2LFs9nH0O9WZFYUjfkV4nXm"
api_key = "ictE4TEiYBIjKOkZsZyF3GG8dcGeDI3U"

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


# Полученим ключ для определения кода города по координатам доп функция для получения погоды
def lock_key_by_cords(latitude, longitude):
    location_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    params = {
        "apikey": api_key,
        "q": f"{latitude},{longitude}"
    }
    response = requests.get(location_url, params=params)
    response = response.json()
    pprint(response)
    if not response:
        return {
            'success': False,
            'error': "Ошибка в получении координат"
        }
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

# Получение погоды по координатам, используя функцию выше, который получили выще
def get_weather(location_key, name):
    try:
        params = {
            "apikey": api_key,
            "details": True,
            'metric': True
        }
        url = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}'
        response = requests.get(url, params=params).json()
        weather_json = {
            'name': name,
            'date': datetime.now().strftime("%d-%m-%Y"),
            'temperature': int(
                (response['DailyForecasts'][0]['Temperature']['Minimum']['Value'] +
                 response['DailyForecasts'][0]['Temperature']['Maximum']['Value']) / 2),
            'relative_humidity': int(response['DailyForecasts'][0]['Day']['RelativeHumidity']['Average']),
            'precipitation_probability': int(response['DailyForecasts'][0]['Day']['PrecipitationProbability']),
            'wind_speed': int(response['DailyForecasts'][0]['Day']['Wind']['Speed']['Value'])}
        weather_json['bad_condition'] = weather_quality(weather_json)
        # Доп проверка на успешность
        return {'success': True,
                'weather': weather_json
                }
    except Exception as e:
        return {'success': False,
                'error': f"Проблемы с доступом к api: \n{str(e)}"
                }

def get_cords(city_name):
    try:
        # params = {
        #     "apikey": api_key,
        #     "details": True,
        #     'metric': True
        # }
        url = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city_name}&language=en-us&details=true'
        response = requests.get(url).json()
        return response[0]['Key']
    except Exception as e:
        return {'success': False,
                'error': f"Проблемы с доступом к api: \n{str(e)}"
                }



def main():
    # Возьму в качестве примера Тулу
    latitude = 54.1961
    longitude = 37.6182
    # loc_key = lock_key_by_cords(latitude, longitude)
    # weather_result = get_weather(loc_key['key'], f"{latitude}; {longitude}")
    # if weather_result['success']:
    #     weather = weather_result['weather']
    #     print(weather)
    #     with open('accu.json', 'w', encoding='utf-8') as f:
    #         json.dump(weather, f, indent=4)
    # else:
    #     print(weather_result['error'])

    name = "Moscow"
    city_key = get_cords(name)
    weather_result = get_weather(city_key, name)
    if weather_result['success']:
        weather = weather_result['weather']
        pprint(weather)
        with open('accu.json', 'w', encoding='utf-8') as f:
            json.dump(weather, f, indent=4)
    else:
        print(weather_result['error'])


if __name__ == '__main__':
    main()


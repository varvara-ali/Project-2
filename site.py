from os import access

from flask import Flask, request, render_template, jsonify
import acuweather

site = Flask(__name__)

# Обработаем главную страницу
@site.route('/')
def main_page():
    return render_template('main.html')



# Получим погоду по координатам
@site.route('/weather_by_cord', methods=['GET', 'POST'])
def weather_by_cords():
    if request.method == 'GET':
        return render_template('weather_by_cords.html')
    elif request.method == 'POST':
        form = request.form
        latitude = form['latitude']
        longitude = form['longitude']
        cords_key = acuweather.lock_key_by_cords(latitude, longitude)
        data = acuweather.get_weather(cords_key['key'], f"{latitude}; {longitude}")
        if data['success']:
            weather = data['weather']
            return render_template('weather_in_point.html', weather=weather)
        else:
            error = data['error']
            return render_template('weather_by_cords.html', error=error)


# получение погоды в городе
@site.route('/weather_by_city', methods=['GET', 'POST'])
def weather_by_city():
    if request.method == 'GET':
        return render_template('weather_by_city.html')
    elif request.method == 'POST':
        data = request.form
        city_name = data['city_name']
        city_key = acuweather.get_cords(city_name)



        if city_key:
            data = acuweather.get_weather(city_key, city_name)
            if data['success']:
                weather = data['weather']
                return render_template('weather_in_point.html', weather=weather)
            else:
                error = data['error']
                return render_template('weather_by_city.html', error=error)

        else:
            return render_template('weather_by_city.html', error='Указанный город не найден')


# получение погоды в начальной и конечной точках маршрута
@site.route('/weather_on_route', methods=['GET', 'POST'])
def weather_on_route():
    if request.method == 'GET':
        return render_template('get_weather.html')
    elif request.method == 'POST':
        form = request.form.to_dict()
        weather_list = []
        for route_point in range(1, 3):
            loc_type = form.get(f'locationType{route_point}')
            # Получение погоды в городе
            if loc_type == 'city':
                name = form.get(f'cityName{route_point}')
                if not name:
                    error = f"Не указано название города"
                    return render_template('get_weather.html', error=error)
                city_key = acuweather.get_cords(name)
                if city_key:
                    data = acuweather.get_weather(city_key, name)
                    if data['success']:
                        weather = data['weather']
                        weather_list.append(weather)

                    else:
                        error = data['error']
                        return render_template('get_weather.html', error=error)
                else:
                    error = f"Указанный город не найден"
                    return render_template('get_weather.html', error=error)
            # Получение погоды через координаты



            elif loc_type == 'coordinates':
                latitude = float(form.get(f'latitude{route_point}'))
                longitude = float(form.get(f'longitude{route_point}'))
                cords_key = acuweather.lock_key_by_cords(latitude, longitude)
                if cords_key['success'] == False:
                    return render_template('get_weather.html', error=cords_key['error'])
                data = acuweather.get_weather(cords_key['key'], f"{latitude}; {longitude}")
                if data['success']:
                    weather = data['weather']
                    weather_list.append(weather)
                else:
                    error = data['error']
                    return render_template('get_weather.html', error=error)

        return render_template('weather_in_two_points.html', weather_list=weather_list)


# Обработка ошибки 404
@site.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    site.run(port=8000, debug=True)
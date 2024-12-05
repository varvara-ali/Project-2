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
        print(form)
        latitude = form['latitude']
        longitude = form['longitude']
        print(latitude, longitude)
        cords_key = acuweather.lock_key_by_cords(latitude, longitude)
        print(cords_key)
        data = acuweather.get_weather(cords_key['key'], f"{latitude}; {longitude}")
        print(data)
        if data['success']:
            weather = data['weather']
            print(weather)
            return render_template('weather_in_point.html', weather=weather)
        else:
            error = data['error']
            print(error)
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


if __name__ == '__main__':
    site.run(port=8000, debug=True)
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
        data = acuweather.get_weather(latitude, longitude)
        print(data)
        if data['success']:
            weather = data['weather']
            print(weather)
            return render_template('weather_in_point.html', weather=weather)
        else:
            error = data['error']
            print(error)
            return render_template('weather_by_cords.html', error=error)

if __name__ == '__main__':
    site.run(port=8000, debug=True)
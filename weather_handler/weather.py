weather_url = 'http://api.openweathermap.org/data/2.5/weather'
weather_token = '401447ad3455a20147cac44f38081dc2'

def get_weather(city):
    return requests.get(weather_url+f'?appid={weather_token}&q={city}&units=metric&lang=ru').json()
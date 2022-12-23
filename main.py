import telebot
import geocoder
import requests
from config import *


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '*Welcome!*\nPlease, send to bot the location, where you want to check the '
                                      'weather. Or share your current location.', parse_mode='Markdown')


@bot.message_handler(content_types=["location"])
def location_info(message):
    if message.location is not None:
        latitude = message.location.latitude
        longitude = message.location.longitude

        user_location_info = geocoder.osm([latitude, longitude], method='reverse')

        bot.send_message(message.from_user.id, f"*Your address:*\n{user_location_info.address}",
                         parse_mode='Markdown')

        user_city = user_location_info.city
        if not user_city:
            user_city = user_location_info.state
        user_id = message.from_user.id
        weather_by_location(user_id, user_city)


def weather_by_location(user_id, user_city):
    params = {'APPID': WEATHER_API, 'q': user_city, 'units': 'metric', 'lang': 'en'}
    result = requests.get(URL, params=params)
    weather = result.json()

    bot.send_message(user_id, f"In city {weather['name']} temperature now: {weather['main']['temp']} °C" + '\n' +
                     f"Max temperature today: {weather['main']['temp_max']} °C" + '\n' +
                     f"Min temperature today: {weather['main']['temp_min']} °C" + '\n' +
                     f"Fells like: {weather['main']['feels_like']} °C" + '\n' +
                     f"Wind speed: {weather['wind']['speed']} m/s" + '\n' +
                     f"Pressure: {weather['main']['pressure']}" + '\n' +
                     f"Humidity: {weather['main']['humidity']}%" + '\n' +
                     f"Visibility: {weather['visibility']} m" + '\n' +
                     f"Clouds: {weather['clouds']['all']}%" + '\n' +
                     f"Weather now: {weather['weather'][0]['description']}")


if __name__ == '__main__':
    bot.polling(True)

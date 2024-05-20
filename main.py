import telebot
import requests

with open("TOKEN") as f:
    bot = telebot.TeleBot(f.read())
api_token = 'e898af2abc276415b2b67e613ba02639'
my_city = {680890776: "Москва"}


def make_txt_pretty(text):
    text = text.translate(str.maketrans('', '', '.,'))
    return text.lower()


def get_weather_by_place(place):
    link = f'http://api.openweathermap.org/data/2.5/weather?q={place}&lang=ru&units=metric&appid={api_token}'
    responce = requests.get(link).json()
    print(responce)
    temp_min = responce["main"]["temp_min"]
    temp_max = responce["main"]["temp_max"]

    pressure = responce["main"]["pressure"]
    wind = responce["wind"]["speed"]

    description = responce['weather'][0]['description']
    return f'Погода в городе {place}:\n{description} \nТемпература от {temp_min}°C до {temp_max}°C\nДавление {pressure} мм рт ст\n' \
           f'Скорость ветра {wind} м/c\n\n'


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    txt = make_txt_pretty(message.text)

    if txt == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif txt == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif txt == 'погода':
        bot.send_message(message.from_user.id, get_weather_by_place(my_city[message.from_user.id]))
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(content_types=["start"])
def start(message):
    bot.send_message(message.from_user.id, 'Привет, я бот, подсказывающий погоду, где ты обитаешь?')
    bot.register_next_step_handler(message, memorize_place)


def memorize_place(message):
    pass


bot.polling(none_stop=True, interval=0)

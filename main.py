import telebot
import requests

with open("TOKEN") as f:
    bot = telebot.TeleBot(f.read())
with open("APITOKEN") as f:
    api_token = f.read()
my_city = {680890776: "Москва"}


def make_txt_pretty(text):
    text = text.translate(str.maketrans('', '', '.,'))
    return text.lower()


def get_weather_by_place(place):
    link = f'http://api.openweathermap.org/data/2.5/weather?q={place}&lang=ru&units=metric&appid={api_token}'
    responce = requests.get(link)
    if responce.status_code != 200:
        return "кажется такого города нет"
    print(responce)
    responce = responce.json()
    temp_min = responce["main"]["temp_min"]
    temp_max = responce["main"]["temp_max"]

    pressure = responce["main"]["pressure"]
    wind = responce["wind"]["speed"]

    description = responce['weather'][0]['description']
    return f'Погода в городе {place.capitalize()}:\n{description.capitalize()} \nТемпература от {temp_min}°C' \
           f' до {temp_max}°C\nДавление {pressure} мм рт ст\nСкорость ветра {wind} м/c'


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    txt = make_txt_pretty(message.text)

    if txt == "привет":
        bot.send_message(message.from_user.id,
                         "Привет, чтобы узнать что я могу, напиши '/help', чтобы познакомиться, напиши '/start'")
    elif txt == "/help":
        bot.send_message(message.from_user.id, "Если хочешь узнать погоду, напиши 'погода'. Если расстроила погода на\
                             завтра, напиши 'я расстроен('")
    elif txt == 'погода':
        try:
            bot.send_message(message.from_user.id, get_weather_by_place(my_city[message.from_user.id]))
        except KeyError:
            bot.send_message(message.from_user.id, 'Кажется мы не знакомы, напиши "/start"')
    elif txt == "/start":
        bot.send_message(message.from_user.id, 'Привет, я бот, подсказывающий погоду, где ты обитаешь?')
        bot.register_next_step_handler(message, memorize_place)
    elif txt == "я расстроен(":
        bot.send_message(message.from_user.id, 'Не расстраивайся! Вот тебе ауф цитата от ДЕ (точнее Черчилля):\
                                                 "Если идёте через ад, идите, не останавливаясь."\
                                                 Если нужна ещё читата, напиши "ещё цитату!"')
    elif txt == "ещё цитату!":
        bot.send_message(message.from_user.id, '"Underidoderidoderidoderidoo" - Winston Churchill')
    else:
        bot.send_message(message.from_user.id, get_weather_by_place(txt))


def memorize_place(message):
    my_city[message.from_user.id] = make_txt_pretty(message.text)
    bot.send_message(message.from_user.id, "Отлично, я запомнил")


bot.polling(none_stop=True, interval=0)

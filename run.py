gb,obida,recom=0,0,0
import telebot
import pyowm #Погода
import time #Время
from telebot import types
from pyowm.exceptions import api_response_error
weather_token='f0d533caf440f9d7604e8da15f7abc76'

tele_token="1046167600:AAEBmpI-LJO1zHSKTCRuleYk8NeX3fKEOLw"


bot = telebot.TeleBot(tele_token)#TELEGRAM BOT TOKEN

owm = pyowm.OWM(weather_token, language= "ru")#WEATER

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,"""Привет 😎
    -----Это БОТ погоды----- 
    Он поможет тебе узнать информацию о погоде в любой точке земного шара
    Просто напиши свой город ниже.....🙃
    /help""")
    time.sleep(4)
    bot.send_message(message.chat.id, "И кстати я знаю как тебя зовут"+"\n"+message.from_user.first_name+", не так ли?"+"\n"+"Впрочем кем бы ты не был, ты красавчик!🤗")
@bot.message_handler(commands=['help'])
def help_me(message):
    bot.send_message(message.chat.id,"""Список команд:
    /start - Начальное приветствие

    Хотите узнать погоду в другом городе, просто его напишите ниже)🗣""")


@bot.message_handler(content_types=["text"])
def gorod(message):
    chat_id = message.chat.id
    place=message.text
    try:
        owm.weather_at_place(place)
        main = owm.weather_at_place(place)
        global weather
        weather = main.get_weather()#ДОСТАЕМ ОТ СЮДА ВСЮ ИНФУ, а так выглядит  прост как код!
        if message.text == "Привет":
            bot.send_message(chat_id,"И тебе привет)")
        else:
            bot.send_message(chat_id, "Какую информацию о погоде вы хотели бы знать?", reply_markup=keyboard())
            bot.send_message(chat_id, "Нехотите получить рекомендации?")
            global recom
            recom+=1
    except(api_response_error.NotFoundError):
        if message.text == "Макс.Темп" or message.text == "Средняя Темп" or message.text == "Мин.Темп" or message.text == "Скорость ветра" or message.text == "Детал Инф." or message.text == "Влажность":
            maxtemp = weather.get_temperature("celsius")["temp_max"]#выбор еденици исчесления, и функци
            midtemp =  weather.get_temperature("celsius")["temp"]#Средняя темп
            mintemp = weather.get_temperature("celsius")["temp_min"]#мин темп 
            speedwind = weather.get_wind()["speed"]#Ветер
            status = weather.get_detailed_status()#Стастус - детальный
            vlag = weather.get_humidity()#функция принимает инфу о влажности

            if message.text == "Макс.Темп":
                bot.send_message(chat_id,"Максимальная Температура в районе - ({:.0f}".format(maxtemp)+"°C)", reply_markup=keyboard())
            elif message.text == "Средняя Темп":
                bot.send_message(chat_id,"Средняя Температура в районе - ({:.0f}".format(midtemp)+"°C)", reply_markup=keyboard())
            elif message.text == "Мин.Темп":
                bot.send_message(chat_id,"Минимальная Температура в районе - ({:.0f}".format(mintemp)+"°C)", reply_markup=keyboard())
            elif message.text == "Скорость ветра":
                bot.send_message(chat_id,"Скорость ветра - {:.0f}".format(speedwind)+"м/с", reply_markup=keyboard())
            elif message.text == "Детал Инф.":
                bot.send_message(chat_id,"На данный момент - "+status, reply_markup=keyboard())
            elif message.text == "Влажность":
                bot.send_message(chat_id,"На данный момент влажность состовляет - {:.0f}".format(vlag)+"%", reply_markup=keyboard())
        elif message.text == "Хай" or message.text == "Погоду, живо!" or message.text == "Здоровенькі були!" or message.text == "Hi" or message.text == "Hello":#приветствие
            if message.text == "Здоровенькі були!":
                bot.send_message(chat_id, 
                """Здоровенькі були козаченько!
                Як твої справи?
                Наприклад в мене все 
                гаразд, 
                бо все ж я просто залізяка,
                на якій працює код 
                Данііла Чугая.
                Та й все(((😥""")
        
            elif message.text == "Хай":
                bot.send_message(chat_id,"Привет, что нужно?")
            elif message.text == "Погоду, живо!":
                bot.send_message(chat_id,"Так ты напиши город, я тебе погоду и выдам...")
            
            else:
                bot.send_message(chat_id,"Да я вижу вы с Англии)"+"\n"+"London is the capital of Great Britain?")
                global gb
                gb+=1 
             
        elif message.text == "Да" or  message.text == "Точно" or message.text == "Yes":
            if recom == 1:
                bot.send_message(chat_id,"Одну секунду......")
                time.sleep(4)
                maxtemp = weather.get_temperature("celsius")["temp_max"]#выбор еденици исчесления, и функци
                midtemp =  weather.get_temperature("celsius")["temp"]#Средняя темп
                mintemp = weather.get_temperature("celsius")["temp_min"]#мин темп 
                speedwind = weather.get_wind()["speed"]#Ветер
                status = weather.get_detailed_status()#Стастус - детальный
                vlag = weather.get_humidity()#функция принимает инфу о влажности
                if status == "дождь" or status == "дощь" or status == "ливень" or status == "небольшой дождь":
                    bot.send_message(chat_id,"Возьми зонт, на улице дождь")
                elif status == "снег" or status == "снегопад":
                    bot.send_message(chat_id,"Чел ты вообще знаешь что там на улице снег)")
                elif status == "ясно" and midtemp > 23.0:
                    bot.send_message(chat_id,"Ну и жарень конечно там, уууууууууу")
                elif status == "облачно" or status == "облачно с прояснениями":
                    bot.send_message(chat_id,"Возможен дощь, или снег"+"\n"+"Мне то откуда знать))")
                if midtemp > 23:
                    bot.send_message(chat_id, "Что сказать,там тепло....")
                elif midtemp < 23 and midtemp > 10:
                    bot.send_message(chat_id,"Не так конечно как хотелось, но все равно тепло)")
                elif midtemp < 10:
                    
                    bot.send_message(chat_id,"Ппц дубак, оденься потеплее!")   
                recom=0           
            elif gb != 1:
                bot.send_message(chat_id, "Что "+ message.text+"?")
            elif gb >= 1:
                bot.send_message(chat_id,"Молодец, хотябы что-то в этой жизне знаешь")
                gb=0
                global obida
                obida+=1
        
        elif message.text == "Обидно":
            if obida >= 1:
                bot.send_message(chat_id,"""Извинити меня пожалуйста....
                                Я и вправду виноват(""")
                obida=0
            elif obida < 0:
                bot.send_message(chat_id,"С чего это вдруг, давай спрашивай погоду"+"\n"+"А не фигнея майся!")
        if message.text == "Нет":
            bot.send_message(chat_id,"Ок)")
            recom=0        
        else:
            bot.send_message(chat_id, """Введенные вами данные неправильны, проверьте правильность написания вашего города
                            Либо нет ответа на вашу реплику....(""")
def keyboard():

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True) 
    knop1,knop2,knop3,knop4,knop5,knop6=types.KeyboardButton("Макс.Темп"),types.KeyboardButton("Средняя Темп"),types.KeyboardButton("Мин.Темп"),types.KeyboardButton("Скорость ветра"),types.KeyboardButton("Детал Инф."),types.KeyboardButton("Влажность")   
    markup.add(knop1,knop2,knop3)
    markup.add(knop4,knop5,knop6)
    return markup
while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(20)
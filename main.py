from os import getenv
import sys
import logging
import math
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message#, ContentType
from aiogram.filters import Command

import datetime 
import asyncio
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = getenv("API_KEY")
BOT_TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


code_to_smile = {
            'Clear': "Ясно \U00002600",
            'Clouds': "Хмарно \U00002601",
            'Drizzle': "Дощ \U00002614"
        }

@dp.message(Command('start'))
async def start_message(message):
    await message.answer('Привіт. Я бот котрий допоможе тобі дізнатися прогноз погоди в будь якому місті.\n'
                         'Щоб дізнатися погоду, необхідно насамперед зазначити місто.\n'
                          'Введіть назву міста: ')

@dp.message()  #content_types=types.ContentType.TEXT
async def get_weather(message: Message):
    #try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API_KEY}&units=metric"
        )
        data = r.json()
        print(f"{data=}")
        city = data['name']
        print(f"{city=}")
        #current_weather = data['main']['temp'] 
        current_weather = math.floor(data['main']['temp'])
        print(f"{current_weather=}")

        weather_description = data['weather'][0]['main']
        print(f"{weather_description=}")
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
            #print(f"{data=}")
        else:
            wd = 'Подивись у вікно \U00001F604'
            
        print(f"{wd=}")
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']) #(d/m/y)
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        daylight_hours = sunset - sunrise

        await message.answer(f"Погода в місті: {city} \nТемпература: {current_weather}°C {wd}\n"
                             f"Вологість: {humidity}%\nАтмосферний тиск: {pressure}мм.рт.ст.\n" 
                             f"Вітер: {wind}km/h\n" 
                             f"Схід сонця: {sunrise} \nЗахід сонця: {sunset}\nТривалість світлового дня: {daylight_hours} \n"
                             f"Гарного дня!")

    #except Exception as ex:  
        #await message.answer('Переконайтеся, що місто написане правильно, та введіть назву міста ще раз: ')

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

from os import getenv
import sys
import logging
import math
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters import Command
from keyboard import menu
from aiogram.filters import Text

import datetime 
import asyncio
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = getenv("API_KEY")
BOT_TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class City(StatesGroup):
    name = State()



code_to_smile = {
    'Clear': "Ясно \U00002600",
    'Clouds': "Хмарно \U00002601",
    'Drizzle': "Дощ \U00002614"
}

@dp.message(Command('start'))
async def start_message(message: Message, state: FSMContext):
    await message.answer('Привіт. Я бот котрий допоможе тобі дізнатися прогноз погоди в будь якому місті.\n'
                         'Щоб дізнатися погоду, необхідно насамперед зазначити місто.\n'
                         'Введіть назву міста: ')
    await state.set_state(City.name)

@dp.message(City.name)
async def process_name(message: Message, state: FSMContext):
    data = await state.update_data(name=message.text)
    await message.answer(
        text=f"Назва міста: {data.get('name')}", 
        reply_markup=menu())

@dp.callback_query(Text("weather_now"))
async def weather_now(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    city = data.get('name')
    await get_weather(callback.message, city, "now")
    await callback.answer()

@dp.callback_query(Text("forecast_today"))
async def forecast_today(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    city = data.get('name')
    await get_weather(callback.message, city, "today")
    await callback.answer()

@dp.callback_query(Text("forecast_week"))
async def forecast_week(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    city = data.get('name')
    await get_weather(callback.message, city, "week")
    await callback.answer()


@dp.message()
async def get_weather(message: Message, city: str, forecast_type: str):
    if forecast_type == "now":
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    elif forecast_type == "today":
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    elif forecast_type == "week":
        url = f"https://api.openweathermap.org/data/2.5/forecast/daily?q={city}&appid={API_KEY}&units=metric&cnt=7"

    r = requests.get(url)
    data = r.json()

    if forecast_type == "now":
        city = data.get('name')
        main = data.get('main', {})
        weather = data.get('weather', [{}])[0]
        wind = data.get('wind', {})
        sys = data.get('sys', {})

        current_weather = math.floor(main.get('temp', 0))
        weather_description = weather.get('main', '')

        wd = code_to_smile.get(weather_description, 'Подивись у вікно \U00001F604')

        humidity = main.get('humidity', 0)
        pressure = main.get('pressure', 0)
        wind_speed = wind.get('speed', 0)
        sunrise = datetime.datetime.fromtimestamp(sys.get('sunrise', 0))
        sunset = datetime.datetime.fromtimestamp(sys.get('sunset', 0))
        daylight_hours = sunset - sunrise

        await message.answer(f"Погода в місті: {city} \nТемпература: {current_weather}°C {wd}\n"
                            f"Вологість: {humidity}%\nАтмосферний тиск: {pressure}мм.рт.ст.\n" 
                            f"Вітер: {wind_speed}km/h\n" 
                            f"Схід сонця: {sunrise} \nЗахід сонця: {sunset}\nТривалість світлового дня: {daylight_hours} \n"
                            f"Гарного дня!")
    #elif 
async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

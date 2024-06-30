from aiogram.utils.keyboard import InlineKeyboardBuilder
    

def menu():
    builder = InlineKeyboardBuilder()

    builder.button(text="Погода зараз", callback_data="weather_now")
    builder.button(text="Прогноз погоди на сьогодні", callback_data="forecast_today")
    builder.button(text="Прогноз погоди на тиждень", callback_data="forecast_week")

    builder.adjust(1)
    return builder.as_markup()
import asyncio
import logging
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold
from aiogram import F
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token)
dp = Dispatcher()


def get_currency_rate(base_currency, target_currency):
    base_url = f"https://api.currencyapi.com/v3/latest?apikey={config.currency_api_key}"
    try:
        response = requests.get(base_url)
        data = response.json()
        exchange_rate = data['data'][target_currency]['value']
        base_rate = data['data'][base_currency]['value']
        result = float(exchange_rate) / float(base_rate)
        return result
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе: {e}")
        return None


@dp.callback_query(F.data.startswith("rate_"))
async def process_callback(callback_query: types.CallbackQuery):
    chosen_currency = callback_query.data.split("_")[1]
    target_currency = 'RUB'

    rate = get_currency_rate(chosen_currency, target_currency)
    if rate is None:
        await callback_query.answer("Ошибка получения курса!")
    else:
        await callback_query.message.answer(f"Курс 1 {chosen_currency} = {rate} {target_currency}")

    btn = [
        [
            InlineKeyboardButton(text="USD", callback_data="rate_USD"),
            InlineKeyboardButton(text="BYN", callback_data="rate_BYN"),
            InlineKeyboardButton(text="TRY", callback_data="rate_TRY"),
            InlineKeyboardButton(text="UAH", callback_data="rate_UAH"),
        ],
        [InlineKeyboardButton(text="Ввести свою валюту", callback_data="custom_currency")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=btn)

    await callback_query.message.answer("Выберите валюту", reply_markup=keyboard)


@dp.callback_query(F.data == "custom_currency")
async def process_custom_currency(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Введите пользовательскую валюту:")
    await callback_query.message.answer("Например: EUR")


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name)
    )
    await message.answer(
        **content.as_kwargs()
    )
    btn = [
        [
            InlineKeyboardButton(text="USD", callback_data="rate_USD"),
            InlineKeyboardButton(text="BYN", callback_data="rate_BYN"),
            InlineKeyboardButton(text="TRY", callback_data="rate_TRY"),
            InlineKeyboardButton(text="UAH", callback_data="rate_UAH"),
        ],
        [InlineKeyboardButton(text="Ввести свою валюту", callback_data="custom_currency")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=btn)

    await message.answer("Выберите валюту", reply_markup=keyboard)


@dp.message()
async def process_user_currency(message: types.Message):
    user_currency = message.text.upper()
    target_currency = "RUB"  # Целевая валюта для получения курса (например, российский рубль)
    rate = get_currency_rate(user_currency, target_currency)
    if rate is None:
        await message.answer("Ошибка при получении курса валюты!")
    else:
        await message.answer(f"Курс 1 {user_currency} = {rate} {target_currency}")

    btn = [
        [
            InlineKeyboardButton(text="USD", callback_data="rate_USD"),
            InlineKeyboardButton(text="BYN", callback_data="rate_BYN"),
            InlineKeyboardButton(text="TRY", callback_data="rate_TRY"),
            InlineKeyboardButton(text="UAH", callback_data="rate_UAH"),
        ],
        [InlineKeyboardButton(text="Ввести свою валюту", callback_data="custom_currency")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=btn)

    await message.answer("Выберите валюту", reply_markup=keyboard)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

import database.requests as rq

langMenu = ReplyKeyboardMarkup(
    keyboard=[
    [
        KeyboardButton(text="🇬🇧 English", ),
    ],
    [
        KeyboardButton(text="🇺🇿 Uzbek", ),
    ],
    [
        KeyboardButton(text="🇷🇺 Russian",)
    ]
],resize_keyboard=True)


keyboard_phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📱 Phone number", request_contact=True)
        ]
    ],resize_keyboard=True)


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = '💧 Mahsulotlar'),
            KeyboardButton(text = '🛒 Korzinka'),
        ],
        [
            KeyboardButton(text = '💴 Suv harid qlish'),
            KeyboardButton(text = '🛠 Sozlamalar'),
        ]
    ],resize_keyboard=True
)


change_lang = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🇺🇿 Til')
        ]
    ], resize_keyboard=True
)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

import database.requests as rq

import logging

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


keyboard_location_input = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Tasdiqlayman"),
            KeyboardButton(text="Qo'lda kiritaman")
        ]
    ],resize_keyboard=True)


keyboard_location = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Location", request_location=True)
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

def get_order_keyboard_option(basket):
    logging.info(basket)
    buttons = []
    if basket:
        buttons.append(KeyboardButton(text='I am holding my orders'))
    else:
        # If the basket is empty
        buttons.append(KeyboardButton(text='Choose products'))
    buttons.append(KeyboardButton(text='I choose your option'))
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True
    )
    return reply_markup

quantity_water_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1'),
            KeyboardButton(text='2'),
            KeyboardButton(text='3'),
        ],
        [
            KeyboardButton(text='4'),
            KeyboardButton(text='5'),
            KeyboardButton(text='6'),
        ],
        [
            KeyboardButton(text='7'),
            KeyboardButton(text='8'),
            KeyboardButton(text='9'),
        ],
        [
            KeyboardButton(text='10'),
            KeyboardButton(text='Back')
        ]
    ],resize_keyboard=True, input_field_placeholder='Qiymat kiriting'
)

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Barcha mahsulotlar'),
            KeyboardButton(text="Mahsulot qo'shish")
        ],
    ],resize_keyboard=True, input_field_placeholder='Nimadir kiriting...'
)
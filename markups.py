from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

import database.requests as rq
from utils.translation import translate as _
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


def keyboard_phone(lang):
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_("📱 Phone number",lang), request_contact=True)
        ]
    ],resize_keyboard=True)


def keyboard_location_input(lang):
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_("Tasdiqlayman",lang)),
            KeyboardButton(text=_("Qo'lda kiritaman",lang))
        ]
    ],resize_keyboard=True)


def keyboard_location(lang):
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_("Location",lang), request_location=True)
        ]
    ],resize_keyboard=True)


def main_keyboard(lang):
 return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = _('💧 Mahsulotlar',lang)),
            KeyboardButton(text = _('🛒 Korzinka',lang)),
        ],
        [
            KeyboardButton(text=_('Buyurtmani qayta takrorlash',lang))
        ],
        [
            KeyboardButton(text = _('💴 Suv harid qlish',lang)),
            KeyboardButton(text = _('🛠 Sozlamalar',lang)),
        ]
    ],resize_keyboard=True
)


def change_lang(lang):
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_('🇺🇿 Til',lang)),
            KeyboardButton(text=_('Back',lang))
        ]
    ], resize_keyboard=True
)

def get_order_keyboard_option(basket,lang):
    buttons = []
    if basket:
        buttons.append(KeyboardButton(text=_('Basket products',lang)))
    else:
        # If the basket is empty
        buttons.append(KeyboardButton(text=_('Choose products',lang)))
    buttons.append(KeyboardButton(text=_('Recommandation products',lang)))
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True
    )
    return reply_markup

def quantity_water_keyboard(lang): 
    return ReplyKeyboardMarkup(
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
            KeyboardButton(text=_('Back',lang))
        ]
    ],resize_keyboard=True, input_field_placeholder='Qiymat kiriting'
)

def admin_keyboard(lang):
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_('Barcha mahsulotlar',lang)),
            KeyboardButton(text=_("Mahsulot qo'shish",lang))
        ],
        [
            KeyboardButton(text=_('Barcha buyurtmalar',lang)),
            KeyboardButton(text=_('Buyurtmalar tarixi',lang))
        ]
    ],resize_keyboard=True, input_field_placeholder='Nimadir kiriting...'
)


def repeat_order(lang):
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_('Qayta takrorlash',lang)),
            KeyboardButton(text = _('💴 Suv harid qlish',lang)),
        ],
        [
            KeyboardButton(text=_('Back',lang))
        ]
    ],resize_keyboard=True
)

def user_type_keyboard(lang): 
    return ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_('Jismoniy shaxs',lang)),
            KeyboardButton(text=_('Yuridik shaxs',lang))
        ]
    ],resize_keyboard=True
)
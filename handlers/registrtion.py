import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import markups as btn
import database.requests as rq
from utils.translation import translate as _

regis_router = Router()


class UserFrom(StatesGroup):
    language = State()
    phone_number = State()

class UserLang(StatesGroup):
    case = State()
    lang = State()
    

@regis_router.message(Command('start'))
async def start_run(message: Message, state: FSMContext):
    user = await rq.get_user(tg_id=message.from_user.id)
    if user:
        await message.answer(_("You are already on the page",user['lang']), reply_markup=btn.main_keyboard)
    else:
        await state.set_state(UserFrom.language)
        await message.answer(
            "Please select your language:",
            reply_markup=btn.langMenu,
        )
        

@regis_router.message(UserFrom.language, F.text)
async def process_language(message: Message, state: FSMContext):
    # Define the mapping of languages
    languages = {
        '🇬🇧 English': "en",
        '🇺🇿 Uzbek': "uz",
        '🇷🇺 Russian': "ru"
    }
    user = await rq.get_user(tg_id=message.from_user.id)

    if message.text not in languages:
        await message.answer(_("Please select a valid language from the options.",user['lang']))
        return  

    await state.update_data(language=languages[message.text])
    
    await message.answer("Enter your phone number or send number", reply_markup=btn.keyboard_phone)
        
    await state.set_state(UserFrom.phone_number)


@regis_router.message(UserFrom.phone_number)
async def process_phone_number(message: Message, state: FSMContext):

    user = await rq.get_user(tg_id=message.from_user.id)
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    await rq.create_user(message.from_user.id, data['language'], data['phone_number'])
    await message.answer("Welcome to real words",reply_markup=btn.main_keyboard)

    await state.clear()



@regis_router.message(F.text == '🛠 Sozlamalar')
async def settings_user(message:Message):
    await message.answer('Tilni tanlang', reply_markup=btn.change_lang)


@regis_router.message(F.text == '🇺🇿 Til')
async def settings_user(message:Message, state:FSMContext):
    user = await rq.get_user(tg_id=message.from_user.id)

    await message.answer(_('Kerakli tilni tanglang',user['lang']), reply_markup=btn.langMenu)
    await state.set_state(UserLang.lang)


@regis_router.message(UserLang.lang)
async def handle_language_selection(message:Message, state:FSMContext):
    user = await rq.get_user(tg_id=message.from_user.id)

    languages = {
        '🇬🇧 English': "en",
        '🇺🇿 Uzbek': "uz",
        '🇷🇺 Russian': "ru"
    }

    selected_language = message.text
    if selected_language not in languages:
        await message.answer(_("Please select a valid language from the options.",user['lang']))
        return
    logging.info(languages[selected_language])
    await rq.change_user_lang(tg_id=message.from_user.id, lang=languages[selected_language])
    await message.answer(f"✅ {_('Language successfully changed',user['lang'])}", reply_markup=btn.main_keyboard)
    await state.clear()


@regis_router.message(F.text == 'Back')
async def go_back(message:Message):

    user = await rq.get_user(tg_id=message.from_user.id)
    await message.answer(_('You come to the main home again',user['lang']), reply_markup=btn.main_keyboard)

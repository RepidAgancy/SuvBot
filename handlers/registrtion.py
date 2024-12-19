import logging

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# from utils.translation import set_language
import markups as btn
import database.requests as rq
from utils.translation import translate as _


regis_router = Router()


class UserFrom(StatesGroup):
    language = State()
    user_type = State()
    company_name = State()
    phone_number = State()

class UserLang(StatesGroup):
    case = State()
    lang = State()
    

@regis_router.message(StateFilter(None), Command('start'))
async def start_run(message: Message, state: FSMContext):
    user = await rq.get_user(tg_id=message.from_user.id)
    if 'message' not in user :
        await message.answer(_("You are already on the page",user['lang']), reply_markup=btn.main_keyboard(user['lang']))
    elif user['message']:
        await state.set_state(UserFrom.language)
        await message.answer(
            "Til tanlang:",
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

    if message.text not in languages:
        await message.answer("Iltimos quyidagi tillardan birini tanlang!")
        return  

    await state.update_data(language=languages[message.text])
    user = await state.get_data()
    await state.set_state(UserFrom.user_type)
    await message.answer(_('Foydalanuvchi turini kiritng',user['language']), reply_markup=btn.user_type_keyboard(user['language']))


@regis_router.message(UserFrom.user_type)
async def company_name_regis(message:Message, state:FSMContext):
    user =await state.get_data()
    await state.update_data(user_type=message.text)

    if message.text in ['Yuridik shaxs','Legal entity','Юридическое лицо']:
        await state.set_state(UserFrom.company_name)
        await message.answer(_('Kompany nomini kiriting', user['language']))
    elif message.text in ['Jismoniy shaxs','Indiviual','Физическое лицо']:
        await state.update_data(company_name=None)
        await state.set_state(UserFrom.phone_number)
        await message.answer(_('Telefon raqamingizni kiriting',user['language']), reply_markup=btn.keyboard_phone(user['language']))


@regis_router.message(UserFrom.company_name)
async def comapny_name_regis(message:Message, state:FSMContext):
    user =await state.get_data()
    if len(message.text) > 100:
        await message.reply(_('Kompaniya nomi 100 sozdan oshmasin',user['language']))
        return 
    
    await state.update_data(company_name=message.text)

    await state.set_state(UserFrom.phone_number)
    await message.answer(_('Telefon raqam kiriting',user['language']), reply_markup=btn.keyboard_phone(user['language']))




@regis_router.message(UserFrom.phone_number)
async def process_phone_number(message: Message, state: FSMContext):

    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    await rq.create_user(message.from_user.id, data['language'], data['phone_number'],data['company_name'],data['user_type'])
    await message.answer(_("Botimizga xush kelibsiz",data['language']),reply_markup=btn.main_keyboard(data['language']))

    await state.clear()



@regis_router.message(F.text.in_(['🛠 Sozlamalar','🛠 Настройки','🛠 Settings']))
async def settings_user(message:Message):
    user = await rq.get_user(message.from_user.id)
    await message.answer(_('Tilni tanlang',user['lang']), reply_markup=btn.change_lang(user['lang']))


@regis_router.message(F.text.in_(['🇺🇿 Til','🇺🇿 Язык','🇺🇿 Language']))
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
    await message.answer(f"✅ {_('Language successfully changed',languages[selected_language])}", reply_markup=btn.main_keyboard(languages[selected_language]))
    await state.clear()


@regis_router.message(F.text.in_(['Back','Ortga','Назад']))
async def go_back(message:Message, state:FSMContext):

    user = await rq.get_user(tg_id=message.from_user.id)
    await message.answer(_('You come to the main home again',user['lang']), reply_markup=btn.main_keyboard(user['lang']))
    await state.clear()

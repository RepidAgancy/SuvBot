from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import markups as btn
import database.requests as rq


regis_router = Router()


class UserFrom(StatesGroup):
    language = State()
    phone_number = State()
    

@regis_router.message(Command('start'))
async def start_run(message: Message, state: FSMContext):
    if await rq.get_user(tg_id=message.from_user.id):
        await message.answer("You are already on the page", reply_markup=btn.main_keyboard)
    else:
        await state.set_state(UserFrom.language)
        await message.answer(
            "Please select your language:",
            reply_markup=btn.langMenu,
        )

# @regis_router.message(Command('cancel'))
# @regis_router.message(F.text.casefold() == 'cancel')
# async def cancel_handler(message: Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return 
#     logging.info("Cancelling state %r", current_state)
#     await state.clear()
#     await message.answer("Cancelled.",reply_markup=ReplyKeyboardRemove())


@regis_router.message(UserFrom.language, F.text)
async def process_language(message: Message, state: FSMContext):
    # Define the mapping of languages
    languages = {
        '🇬🇧 English': "en",
        '🇺🇿 Uzbek': "uz",
        '🇷🇺 Russian': "ru"
    }

    if message.text not in languages:
        await message.answer("Please select a valid language from the options.")
        return  

    await state.update_data(language=languages[message.text])
    
    await message.answer("Enter your phone number or send number", reply_markup=btn.keyboard_phone)
        
    await state.set_state(UserFrom.phone_number)


@regis_router.message(UserFrom.phone_number)
async def process_phone_number(message: Message, state: FSMContext):

    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    await state.update_data(phone_number=phone_number)
    data = await state.get_data()
    await rq.create_user(message.from_user.id, data['language'], data['phone_number'])
    await message.answer("Welcome to real words")

    await state.clear()


# @regis_router.message(Registration.company_name)
# async def process_company_name(message: Message, state: FSMContext):
#     await state.update_data(company_name=message.text)

#     await message.answer("Enter company contact:", reply_markup=btn.regis_btn_phone)

#     await state.set_state(Registration.company_contact)


# @regis_router.message(Registration.company_contact)
# async def process_company_contact(message: Message, state: FSMContext):
#     await state.update_data(company_contact=message.text)

#     await message.answer("Enter number of employees:",reply_markup=btn.regis_btn)

#     await state.set_state(Registration.number_employee)


# @regis_router.message(Registration.number_employee)
# async def process_number_employee(message: Message, state: FSMContext):
#     await state.update_data(number_employee=message.text)

#     await message.answer("Enter how many days will be enough for you:",reply_markup=btn.regis_btn)

#     await state.set_state(Registration.time_drink_water)


# @regis_router.message(Registration.time_drink_water)
# async def process_time_drink_water(message: Message, state: FSMContext):
#     await state.update_data(time_drink_water=message.text)

#     # Final answer
#     data = await state.get_data()
#     await message.answer(f"Registration complete: {data}")

#     # Clear the state
#     await state.clear()






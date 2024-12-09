from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup,KeyboardButton

import markups as btn
import database.requests as rq

order_router = Router()

class Order(StatesGroup):
    company_name = State()
    company_contact = State()
    number_employee = State()
    time_drink_water = State()
    water_litr = State()


@order_router.message(F.text == '💴 Suv harid qlish')
async def create_order(message:Message, state:FSMContext):
    await state.set_state(Order.company_name)
    await message.answer("Enter company name:")


@order_router.message(Order.company_name)
async def order_company_name(message:Message, state:FSMContext):
    await state.update_data(company_name = message.text)
    await message.answer("Enter company contact:", reply_markup=btn.keyboard_phone)
    await state.set_state(Order.company_contact)


@order_router.message(Order.company_contact)
async def order_company_employee(message:Message, state:FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    await state.update_data(company_contact=phone_number)
    await message.answer("How many people are working:")
    await state.set_state(Order.number_employee)


@order_router.message(Order.number_employee)
async def order_company_number_employee(message:Message, state:FSMContext):

    await state.update_data(number_employee=message.text)
    await message.answer("How may days needed water:")
    await state.set_state(Order.time_drink_water)


@order_router.message(Order.time_drink_water)
async def order_company_time_drink(message:Message, state:FSMContext):

    await state.update_data(time_drink_water=message.text)
    data = await state.get_data()

    lister_water = int(data["number_employee"]) * int(data["time_drink_water"]) * 0.6
    result = f'''
    Based our calculation:
    Number of employees:{data['number_employee']}
    Water needed in {data['time_drink_water']}
    ------------------------------------------
    Our suggestion to buy {round(lister_water/20)} ta 20 litr '''

    await message.answer(result)

    await message.answer("How may litrs needed:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text = 'I am holding my orders'),
                KeyboardButton(text = 'I choose your option'),
            ]
        ], resize_keyboard=True
    ))
    await state.set_state(Order.water_litr)


@order_router.message(Order.water_litr, F.text == 'I am holding my orders')
async def order_user_desire(message:Message, state:FSMContext):
    data = await state.get_data()
    basket = await rq.get_basket(user_id=message.from_user.id)


    await rq.create_order(user_id=message.from_user.id,
                          company_name=data['company_name'],
                          basket_id = basket['id'],
                          company_contact = data['company_contact'],
                          number_employee = data['number_employee'],
                          time_drink = data['time_drink_water'],
                          created_at = datetime.now(),
                          )
    await state.clear()
    await message.answer('Order successfully added, after 2 days later you will get', reply_markup=btn.main_keyboard)


@order_router.message(Order.water_litr, F.text == 'I choose your option')
async def order_user_recommend(message:Message, state:FSMContext):

    data = await state.get_data()

    product_litr = await rq.get_product_by_litr(20)
    lister_water = int(data["number_employee"]) * int(data["time_drink_water"]) * 0.6
    await rq.add_basket_item(user_id=message.from_user.id,product_id=product_litr['id'], quantity=round(lister_water/20))

    basket = await rq.get_basket(user_id=message.from_user.id)
    await rq.create_order(user_id=message.from_user.id,
                          company_name=data['company_name'],
                          basket_id = basket['id'],
                          company_contact = data['company_contact'],
                          number_employee = data['number_employee'],
                          time_drink = data['time_drink_water'],
                          created_at = datetime.now(),
                          )
    await state.clear()
    await message.answer('Order successfully added, after 2 days later you will get', reply_markup=btn.main_keyboard)
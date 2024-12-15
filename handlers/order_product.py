from datetime import datetime, timedelta
import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup,KeyboardButton

import markups as btn
import database.sync_to_async as sn
import utils.util as util
import database.requests as rq
from utils.regex import match_phone_number

order_router = Router()

class Order(StatesGroup):
    company_name = State()
    company_contact = State()
    location = State()
    location_input = State()
    location_confirm = State()
    number_employee = State()
    time_drink_water = State()
    product_add = State()
    product_show = State()
    product_qun = State()
    product_finish = State()


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
        phone = message.contact.phone_number
        if not match_phone_number(phone):
            await message.answer('Please input vaild phone number')
            return 
        else:
            phone_number = message.contact.phone_number
    else:
        phone = message.text
        if not match_phone_number(phone):
            await message.answer('Please input vaild phone number')
            return 
        else:
            phone_number = message.text

    await state.update_data(company_contact=phone_number)
    await message.answer("Enter company location or type where you what", reply_markup=btn.keyboard_location)
    await state.set_state(Order.location)


@order_router.message(Order.location)
async def order_company_locatiop(message:Message, state:FSMContext):
    if message.location:
        location_=util.verify_location_yandex(message.location.latitude,message.location.longitude,)
        await message.answer(f"Bu mazilni tasdiqlaysizmi **{location_}**",
                             parse_mode="Markdown",
                             reply_markup=btn.keyboard_location_input)
        await state.update_data(location =location_ )
    elif message.text == 'Tasdiqlayman':
        user_data = await state.get_data()
        await state.update_data(location=user_data.get("location"))    
        await message.answer("How many emplyee have")
        await state.set_state(Order.number_employee)
    elif message.text == "Qo'lda kiritaman":
        await message.answer("Qolda kirit")
        await state.set_state(Order.location_input)
    else:
        await message.answer("Input location !!!!!")
        return
    
@order_router.message(Order.location_input)
async def order_location_input(message:Message, state:FSMContext):
    if message.text:
        await state.update_data(location=message.text)

    await message.answer('How many employyes have')
    await state.set_state(Order.number_employee)


@order_router.message(Order.number_employee)
async def order_company_number_employee(message:Message, state:FSMContext):
    if not message.text.isdigit():
        await message.answer("Please input digits only")
        return 
    await state.update_data(number_employee=message.text)
    await message.answer("How may days needed water:")
    await state.set_state(Order.time_drink_water)


@order_router.message(Order.time_drink_water)
async def order_company_time_drink(message:Message, state:FSMContext):
    if not message.text.isdigit():
        await message.reply('Please input digits only')
        return 
    if not message.text.isdigit():
        await message.reply('Please input digits only')
        return 

    await state.update_data(time_drink_water=message.text)
    data = await state.get_data()

    lister_water = int(data["number_employee"]) * int(data["time_drink_water"]) * 0.6
    result = f'''
    Based our calculation:
    Number of employees:{data['number_employee']}
    Water needed in {data['time_drink_water']}
    Location in {data['location']}
    ------------------------------------------
    Our suggestion to buy {round(lister_water/20)} ta 20 litr '''

    await message.answer(result)
    basket = await rq.get_basket_item(message.from_user.id)

    await message.answer("How may litrs needed:",reply_markup=btn.get_order_keyboard_option(basket))
    await state.set_state(Order.product_add)


@order_router.message(Order.product_add, F.text == 'Choose products')
async def choose_product_order(message:Message, state:FSMContext):
    await message.answer('Choose product and continue', reply_markup=await rq.all_products_keyboard())
    await state.set_state(Order.product_show)


@order_router.message(Order.product_show)
async def adding_product(message:Message, state:FSMContext):
    await state.update_data(product_add=message.text)
    await message.answer("How many do you need Jigar", reply_markup=btn.quantity_water_keyboard)
    await state.set_state(Order.product_qun)


@order_router.message(Order.product_qun)
async def order_product_quantity(message:Message, state:FSMContext):
    try:
        logging.info(message.text)
        if not message.text.isdigit():
            await message.answer("Please enter a valid quantity (digits only).")
            return
        
        product = await state.get_data()
        product_id = await rq.get_product_by_litr(product['product_add'])

        if not product_id:
            await message.answer("Error: Product not found.")
            return

        await rq.add_basket_item(
            product_id=product_id['id'],
            user_id=message.from_user.id,
            quantity=int(message.text)
        )
        
        await message.answer("Processing your order...")
        data = await state.get_data()
        basket = await rq.get_basket(user_id=message.from_user.id)

        if not basket:
            await message.answer("Error: Basket not found.")
            return

        await rq.create_order(
            user_id=message.from_user.id,
            company_name=data['company_name'],
            basket_id=basket['id'],
            company_contact=data['company_contact'],
            number_employee=data['number_employee'],
            time_drink=data['time_drink_water'],
            created_at=datetime.now(),
            notify_user = datetime.now() + timedelta(days=int(data['time_drink_water'])-2)
        )
        await state.clear() 
        await message.answer(
            "Order successfully added! Delivery will take place in 2 days.",
            reply_markup=btn.main_keyboard
        )

        await state.set_state(Order.product_finish)  # Correctly set the next state
    except Exception as e:
        logging.error(f"Error in order_product_quantity: {e}")
        await message.answer("An error occurred. Please try again.")


@order_router.message(Order.product_add, F.text == 'I am holding my orders')
async def order_user_desire(message:Message, state:FSMContext):
    await message.answer('finfifnfnf')
    data = await state.get_data()
    basket = await rq.get_basket(user_id=message.from_user.id)


    await rq.create_order(user_id=message.from_user.id,
                          company_name=data['company_name'],
                          basket_id = basket['id'],
                          company_contact = data['company_contact'],
                          number_employee = data['number_employee'],
                          time_drink = data['time_drink_water'],
                          created_at = datetime.now(),
                          notify_user = datetime.now() + timedelta(days=int(data['time_drink_water'])-2)
                          )
    await state.clear()
    await message.answer('Order successfully added, after 2 days later you will get', reply_markup=btn.main_keyboard)


@order_router.message(Order.product_add, F.text == 'I choose your option')
async def order_user_recommend(message:Message, state:FSMContext):

    data = await state.get_data()

    product_litr = await rq.get_product_by_litr('18.9L Suv')
    lister_water = int(data["number_employee"]) * int(data["time_drink_water"]) * 0.6
    await rq.add_basket_item(user_id=message.from_user.id,product_id=product_litr['id'], quantity=round(lister_water/18.9))

    basket = await rq.get_basket(user_id=message.from_user.id)
    await rq.create_order(user_id=message.from_user.id,
                          company_name=data['company_name'],
                          basket_id = basket['id'],
                          company_contact = data['company_contact'],
                          number_employee = data['number_employee'],
                          time_drink = data['time_drink_water'],
                          created_at = datetime.now(),
                          notify_user = datetime.now() + timedelta(days=int(data['time_drink_water'])-2)
                          )
    await state.clear()
    await message.answer('Order successfully added, after 2 days later you will get', reply_markup=btn.main_keyboard)
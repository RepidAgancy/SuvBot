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
from utils.translation import translate as _

order_router = Router()

class Order(StatesGroup):
    location = State()
    location_input = State()
    location_confirm = State()
    number_employee = State()
    time_drink_water = State()
    product_add = State()
    product_show = State()
    product_qun = State()
    product_finish = State()


@order_router.message(F.text.in_(['💴 Suv harid qilish','💴 Купить воду','💴 Buy water']))
async def create_order(message:Message, state:FSMContext):
    user = await rq.get_user(message.from_user.id)
    await state.set_state(Order.location)
    await message.answer(_("Kompaniyani locatsiyasini kiriting:",user['lang']), reply_markup=btn.keyboard_location(user['lang']))


@order_router.message(Order.location)
async def order_company_locatiop(message:Message, state:FSMContext):
    user = await rq.get_user(message.from_user.id)
    if message.location:
        location_=util.verify_location_yandex(message.location.latitude,message.location.longitude,)
        await message.answer(_('Bu mazilni tasdiqlaysizmi **{location_}**'.format(location_=location_),user['lang']),
                             parse_mode="Markdown",
                             reply_markup=btn.keyboard_location_input(user['lang']))
        await state.update_data(location =location_ )
    elif message.text in ['Tasdiqlayman','Confirm','Подтверждаю']:
        user_data = await state.get_data()
        await state.update_data(location=user_data.get("location"))    
        await message.answer(_("How many emplyee have",user['lang']))
        await state.set_state(Order.number_employee)
    elif message.text == ["Qo'lda kiritaman",'Введите вручную','Write location']:
        await message.answer(_("Qolda kirit",user['lang']))
        await state.set_state(Order.location_input)
    else:
        await message.answer(_("Input location !!!!!",user['lang']))
        return
    
@order_router.message(Order.location_input)
async def order_location_input(message:Message, state:FSMContext):
    user= await rq.get_user(message.from_user.id)
    if message.text:
        await state.update_data(location=message.text)

    await message.answer(_('How many employyes have',user['lang']))
    await state.set_state(Order.number_employee)


@order_router.message(Order.number_employee)
async def order_company_number_employee(message:Message, state:FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not message.text.isdigit():
        await message.answer(_("Please input digits only",user['lang']))
        return 
    await state.update_data(number_employee=message.text)
    await message.answer(_("How may days needed water:",user['lang']))
    await state.set_state(Order.time_drink_water)


@order_router.message(Order.time_drink_water)
async def order_company_time_drink(message:Message, state:FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not message.text.isdigit():
        await message.reply(_('Please input digits only',user['lang']))
        return 
    if not message.text.isdigit():
        await message.reply(_('Please input digits only',user['lang']))
        return 

    await state.update_data(time_drink_water=message.text)
    data = await state.get_data()

    lister_water = int(data["number_employee"]) * int(data["time_drink_water"]) * 0.6
    response = _(
        "According to your input:\n"
        "— Number of employees: {number_employee}\n"
        "— Number of days: {time_drink_water}\n"
        "— Location: {location}\n\n"
        "Based on the provided information, you need to purchase {water_needed} units of 18.9 liters of water.",
        user['lang']
    ).format(
        number_employee=data['number_employee'],
        time_drink_water=data['time_drink_water'],
        location=data['location'],
        water_needed=round(lister_water/18.9)
    )

    await message.answer(response)
    basket = await rq.get_basket_item(message.from_user.id)

    await message.answer(_("How may litrs needed:",user['lang']),reply_markup=btn.get_order_keyboard_option(basket,user['lang']))
    await state.set_state(Order.product_add)


@order_router.message(Order.product_add, F.text.in_(['Choose products','Mahsulot tanlash','Выбор продукта']))
async def choose_product_order(message:Message, state:FSMContext):
    user = await rq.get_user(message.from_user.id)
    await message.answer(_('Choose product and continue',user['lang']), reply_markup=await rq.all_products_keyboard(user['lang']))
    await state.set_state(Order.product_show)


@order_router.message(Order.product_show)
async def adding_product(message:Message, state:FSMContext):
    await state.update_data(product_add=message.text)
    user = await rq.get_user(message.from_user.id)
    await message.answer(_("How many do you need product?",user['lang']), reply_markup=btn.quantity_water_keyboard(user['lang']))
    await state.set_state(Order.product_qun)


@order_router.message(Order.product_qun)
async def order_product_quantity(message:Message, state:FSMContext):
    try:
        user = await rq.get_user(message.from_user.id)
        if not message.text.isdigit():
            await message.answer(_("Please enter a valid quantity (digits only).",user['lang']))
            return
        
        product = await state.get_data()
        product_id = await rq.get_product_by_litr(product['product_add'])

        if not product_id:
            await message.answer(_("Error: Product not found.",user['lang']))
            return

        await rq.add_basket_item(
            product_id=product_id['id'],
            user_id=message.from_user.id,
            quantity=int(message.text)
        )
        
        data = await state.get_data()
        basket = await rq.get_basket(user_id=message.from_user.id)

        if not basket:
            await message.answer(_("Error: Basket not found.",user['lang']))
            return

        await rq.create_order(
            user_id=message.from_user.id,
            basket_id=basket['id'],
            number_employee=data['number_employee'],
            time_drink=data['time_drink_water'],
            location=data['location'],
            created_at=datetime.now(),
            notify_user = datetime.now() + timedelta(days=int(data['time_drink_water'])-2)
        )
        await state.clear() 
        await message.answer(
            _("Order successfully added! Delivery will take place in 2 days.",user['lang']),
            reply_markup=btn.main_keyboard(user['lang'])
        )

        await state.set_state(Order.product_finish)  # Correctly set the next state
    except Exception as e:
        await message.answer(_("An error occurred. Please try again.",user['lang']))


@order_router.message(Order.product_add, F.text.in_(['Товары в корзине','Korzinkadagi mahsulotlar','Basket products']))
async def order_user_desire(message:Message, state:FSMContext):
    user = await rq.get_user(message.from_user.id)
    data = await state.get_data()
    basket = await rq.get_basket(user_id=message.from_user.id)

    await rq.create_order(user_id=message.from_user.id,
                          basket_id = basket['id'],
                          number_employee = data['number_employee'],
                          time_drink = data['time_drink_water'],
                          location=data['location'],
                          created_at = datetime.now(),
                          notify_user = datetime.now() + timedelta(days=int(data['time_drink_water'])-2)
                          )
    await state.clear()
    await message.answer(_('Order successfully added, after 2 days later you will get',user['lang']), reply_markup=btn.main_keyboard(user['lang']))


@order_router.message(Order.product_add, F.text.in_(['Получить предложение','Tafsiyani olish','Recommandation products']))
async def order_user_recommend(message:Message, state:FSMContext):
    deleted_item = await rq.delete_basket_choose(user_id=message.from_user.id)
    data = await state.get_data()
    user = await rq.get_user(message.from_user.id)
    
    product_litr = await rq.get_product_by_litr('18.9L Suv')
    lister_water = int(data["number_employee"]) * int(data["time_drink_water"]) * 0.6
    await rq.add_basket_item(user_id=message.from_user.id,product_id=product_litr['id'], quantity=round(lister_water/18.9))

    basket = await rq.get_basket(user_id=message.from_user.id)
    await rq.create_order(user_id=message.from_user.id,
                          basket_id = basket['id'],
                          number_employee = data['number_employee'],
                          time_drink = data['time_drink_water'],
                          location=data['location'],
                          created_at = datetime.now(),
                          notify_user = datetime.now() + timedelta(days=int(data['time_drink_water'])-2)
                          )
    await state.clear()
    await message.answer(_('Order successfully added, after 2 days later you will get',user['lang']), reply_markup=btn.main_keyboard(user['lang']))
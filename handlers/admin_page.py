import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter

from utils.filters import AdminFilter
from utils.ppginator import Paginator
import markups as btn
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import database.requests as rq
import database.sync_to_async as syn

ADMIN_IDS = [5714872865]

class ProductAdd(StatesGroup):
    name = State()
    price = State()
    image = State()

admin_router = Router()

admin_router.message.filter(AdminFilter(admin_ids=ADMIN_IDS))

@admin_router.message(Command("start"))
async def run_as_admin(message: Message):
    await message.answer('You are on the main page',reply_markup=btn.admin_keyboard)


@admin_router.message(F.text == 'Barcha mahsulotlar')
async def all_products(message:Message):
    products = await rq.get_all_products()
    logging.info(products)
    for product in products:
        await message.answer_photo(photo=product['image'], caption=f"Nomi: {product['name']}\nNarxi: {product['price']} so'm")


@admin_router.message(StateFilter(None), F.text=="Mahsulot qo'shish")
async def add_product_admin(message:Message, state:FSMContext):
    await message.answer('Tovarni nomini kiriting')
    await state.set_state(ProductAdd.name)


@admin_router.message(ProductAdd.name)
async def add_product_name(message:Message, state:FSMContext):
    if len(message.text) >= 100:
        await message.reply('100 dan ortiq bolmagan so\'z kiriting')
        return
    await state.update_data(name=message.text)
    await message.answer('Tovarni narxini qoshing')
    await state.set_state(ProductAdd.price)


@admin_router.message(ProductAdd.price)
async def add_product_price(message:Message, state:FSMContext):
    if not message.text.isdigit():
        await message.reply('Iltimos jigar faqat sonlar kirit')
        return 
    await state.update_data(price=message.text)
    await message.answer('Tovarni rasmnini tashang')
    await state.set_state(ProductAdd.image)


@admin_router.message(ProductAdd.image)
async def add_product_image(message:Message, state:FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer('Tovar muvvaffaqiyatli qoshildi')
    data = await state.get_data()
    msg = await rq.add_product(name=data['name'],
                         price=data['price'],
                         image=data['image'])
    await message.answer(msg['message'])
    await state.clear()


@admin_router.message(F.text == 'Barcha buyurtmalar')
async def all_orders_admin(message:Message):
    orders = await rq.get_all_orders()
    logging.info(orders)
    messages_order = await syn.format_orders_for_message(orders)
    
    for data, id in messages_order:
        await message.answer(data, reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Bajarildi', callback_data=f'done_{id}')
                ]
            ]
        ))

@admin_router.callback_query(F.data.contains('done_'))
async def done_order_products(callback:CallbackQuery):
    id = callback.data[5:]

    await rq.order_make_done(int(id))
    await callback.answer('Product succeessfully bajarildi')
    await callback.message.delete()
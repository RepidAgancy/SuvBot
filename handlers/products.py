import logging
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.translation import translate as _

import database.requests as rq
import markups as btn

class ProductBasket(StatesGroup):
    name = State()
    quantity = State()

product_router = Router()


@product_router.message(StateFilter(None), F.text.in_(['💧 Mahsulotlar','💧 Продукты','💧 Products']))
async def all_product(message:Message, state:FSMContext):
    user = await rq.get_user(message.from_user.id)
    await message.answer(_("All products",user['lang']), reply_markup=await rq.all_products_keyboard(user['lang']))
    await state.set_state(ProductBasket.name)


@product_router.message(ProductBasket.name, F.text)
async def handle_product_selection(message: Message, state:FSMContext):
    product = await rq.get_product_by_litr(message.text)
    user = await rq.get_user(message.from_user.id)
    text = _(
            '''
Nomi: {name}

Narxi: {price}
            ''', user['lang']
        ).format(
            name=product['name'],
            price=product['price']
        )
    await message.answer_photo(photo=product['image'], caption=text)
    await state.update_data(name=product['id'])
    await message.answer(_('Nechta kerak',user['lang']), reply_markup=btn.quantity_water_keyboard(user['lang']))
    await state.set_state(ProductBasket.quantity)


@product_router.message(ProductBasket.quantity)
async def handle_product_quantity(message:Message, state:FSMContext):
    user = await rq.get_user(message.from_user.id)
    if not message.text.isdigit():
        await message.answer(_('Please raqam kiriting',user['lang']))
        return
    await state.update_data(quantity=message.text)
    data = await state.get_data()
    product_add = await rq.add_basket_item(product_id=int(data['name']),
                                         user_id=message.from_user.id,
                                         quantity=int(data['quantity'])
                                         )
    await message.answer(_("Product add basket successfully",user['lang']),reply_markup=btn.main_keyboard(user['lang']))
    await state.clear()
    

@product_router.callback_query(F.data.contains('delete_cart_'))
async def delete_message_cart(callback:CallbackQuery):
    user = await rq.get_user(callback.from_user.id)
    id = callback.data[12:]
    await callback.answer(_('Item is deleted successfully',user['lang']))
    await rq.delete_basket(int(id))
    await callback.message.delete()


@product_router.callback_query(F.data.contains('add_'))
async def message_add_cart(callback:CallbackQuery):
    id = callback.data[4:]
    await rq.add_cart_quantity(int(id))
    basket_item = await rq.get_basket_item_change(int(id))
    original_caption = callback.message.caption
    user = await rq.get_user(callback.from_user.id)

    if original_caption:  
        lines = original_caption.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("📦 Quantity:"):
                lines[i] = f"📦 Quantity: {basket_item['quantity']}"
            elif line.startswith("🔢 Total:"):
                lines[i] = f"🔢 Total:: {basket_item['total_price']} UZS"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Delete", callback_data=f"delete_cart_{id}"),
            ],
            [
                InlineKeyboardButton(text="➕ 1", callback_data=f"add_{id}"),
                InlineKeyboardButton(text="➖ 1", callback_data=f"subtract_{id}"),
            ]
        ])

        updated_caption = '\n'.join(lines)

        await callback.message.edit_caption(caption=updated_caption, reply_markup=keyboard)
        await callback.answer("Item added")
    else:
        await callback.answer("Unable to update message. No caption found.", show_alert=True)


@product_router.callback_query(F.data.contains('subtract_'))
async def message_substract_cart(callback:CallbackQuery):
    
    id = callback.data[9:]
    await rq.substratc_cart_quantity(int(id))

    basket_item = await rq.get_basket_item_change(id)
    original_caption = callback.message.caption
    
    if original_caption: 
        lines = original_caption.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("📦 Quantity:"):
                lines[i] = f"📦 Quantity: {basket_item['quantity']}"  
            elif line.startswith("🔢 Total:"):
                lines[i] = f"🔢 Total:: {basket_item['total_price']} UZS"
            
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Delete", callback_data=f"delete_cart_{basket_item['id']}"),
            ],
            [
                InlineKeyboardButton(text="➕ 1", callback_data=f"add_{basket_item['id']}"),
                InlineKeyboardButton(text="➖ 1", callback_data=f"subtract_{basket_item['id']}"),
            ]
            ])
        updated_caption = '\n'.join(lines)
    
        await callback.message.edit_caption(caption=updated_caption, reply_markup=keyboard)
            
        await callback.answer("Item substracted")
    else:
        await callback.answer("Unable to update message. No caption found.", show_alert=True)


@product_router.message(F.text.in_(['Buyurtmani qayta takrorlash','Повторить заказ','Repeat the order']))
async def repeat_older_order(message:Message):
    order_last = await rq.last_order_repeat(message.from_user.id)
    user = await rq.get_user(message.from_user.id)
    if not order_last:
        await message.answer('Sizda hali oxirga buyurtma yoq')
        return 
    text =_(
        '''
📋 Company Details:
- 🏢 Company Name: {company_name}
- 📞 Contact: {company_contact}
- 👷 Number of Employees: {number_employee} ta
- 📍 Address: {location}
- 🚚 Delivery Time: {time_drink} kun
- 🕒 Order Date: {created_at}

📦 Products:
        ''', user['lang']
    ).format(
        company_name=order_last['company_name'],
        company_contact=order_last['company_contact'],
        number_employee=order_last['number_employee'],
        location=order_last['location'],
        time_drink=order_last['time_drink'],
        created_at=order_last['created_at'].strftime('%Y-%m-%d')
    )

# Add products using a loop
    for product in order_last['products']:
        text += _(
            '''
    - 🛍 Product Name: {product_name}
    - 🔢 Quantity: {quantity}
    - 💰 Price: {price} UZS
            ''', user['lang']
        ).format(
            product_name=product['product_name'],
            quantity=product['quantity'],
            price=product['price']
        )
        
    await message.answer(text,reply_markup=btn.repeat_order(user['lang']))


@product_router.message(F.text.in_(['Qayta takrorlash','Repeat once','Повторите еще раз']))
async def repeat_order_once(message:Message):
    user = await rq.get_user(message.from_user.id)
    order_last = await rq.last_order_repeat(message.from_user.id)
    await rq.repeat_order_create(user_id=message.from_user.id,
                          basket_id = order_last['basket_id'],
                          number_employee = order_last['number_employee'],
                          time_drink = order_last['time_drink'],
                          location=order_last['location'],
                          created_at = datetime.now(),
                          notify_user = datetime.now() + timedelta(days=int(order_last['time_drink'])-2)
                          )
    await message.answer(_('Buyurtma rasmilashtirildi',user['lang']),reply_markup=btn.main_keyboard(user['lang']))
    


from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database.requests as rq
import markups as btn

class ProductBasket(StatesGroup):
    name = State()
    quantity = State()

product_router = Router()


@product_router.message(StateFilter(None), F.text == '💧 Mahsulotlar')
async def all_product(message:Message, state:FSMContext):
    await message.answer("All products", reply_markup=await rq.all_products_keyboard())
    await state.set_state(ProductBasket.name)


@product_router.message(ProductBasket.name, F.text)
async def handle_product_selection(message: Message, state:FSMContext):
    product = await rq.get_product_by_litr(message.text)
    text = f'''
        Nomi: {product['name']}


    Narxi: {product['price']}
    '''
    await message.answer_photo(photo=product['image'], caption=text)
    await state.update_data(name=product['id'])
    await message.answer('Nechta kerak', reply_markup=btn.quantity_water_keyboard)
    await state.set_state(ProductBasket.quantity)


@product_router.message(ProductBasket.quantity)
async def handle_product_quantity(message:Message, state:FSMContext):
    if not message.text.isdigit():
        await message.answer('Please raqam kiriting')
        return
    await state.update_data(quantity=message.text)
    data = await state.get_data()
    product_add = await rq.add_basket_item(product_id=data['name'],
                                         user_id=message.from_user.id,
                                         quantity=data['quantity']
                                         )
    await message.answer(product_add['message'],reply_markup=btn.main_keyboard)
    await state.clear()
    

@product_router.callback_query(F.data.contains('delete_cart_'))
async def delete_message_cart(callback:CallbackQuery):
    
    id = callback.data[12:]
    await callback.answer('Item is deleted successfully')
    await rq.delete_basket(int(id))
    await callback.message.delete()


@product_router.callback_query(F.data.contains('add_'))
async def message_add_cart(callback:CallbackQuery):
    id = callback.data[4:]
    await rq.add_cart_quantity(int(id))
    basket_item = await rq.get_basket_item_change(int(id))
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

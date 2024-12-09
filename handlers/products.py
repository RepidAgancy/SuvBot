import logging

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

import database.requests as rq
import markups as btn

product_router = Router()


@product_router.message(F.text == '💧 Mahsulotlar')
async def all_product(message:Message):
    await message.answer("All products", reply_markup=await rq.all_products_keyboard())


@product_router.message(F.text.contains('L'))
async def handle_product_selection(message: Message):
    product = await rq.get_product_by_litr(message.text[:-1])
    await rq.add_basket_item(product['id'],user_id=message.from_user.id)
    await message.answer(f"Product added basket successfully", reply_markup=btn.main_keyboard)


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

    basket_item = await rq.get_basket_item(id)
    original_text = callback.message.text
    
    lines = original_text.split('\n')
    for i, line in enumerate(lines):
        if line.startswith("Quantity:"):
            lines[i] = f"Quantity: {basket_item['quantity']}"  # Update only the quantity line
        elif line.startswith("Total:"):
            lines[i] = f"Total: {basket_item['total_price']} UZS"
            
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Delete", callback_data=f"delete_cart_{basket_item['id']}"),
        ],
        [
            InlineKeyboardButton(text="➕ 1", callback_data=f"add_{basket_item['id']}"),
            InlineKeyboardButton(text="➖ 1", callback_data=f"subtract_{basket_item['id']}"),
        ]
        ])
    updated_text = '\n'.join(lines)
    await callback.message.edit_text(updated_text, reply_markup=keyboard)
    
    await callback.answer("Item added")


@product_router.callback_query(F.data.contains('subtract_'))
async def message_substract_cart(callback:CallbackQuery):
    
    id = callback.data[9:]
    await rq.substratc_cart_quantity(int(id))

    basket_item = await rq.get_basket_item(id)
    original_text = callback.message.text
    
    lines = original_text.split('\n')
    for i, line in enumerate(lines):
        if line.startswith("Quantity:"):
            lines[i] = f"Quantity: {basket_item['quantity']}"  # Update only the quantity line
        elif line.startswith("Total:"):
            lines[i] = f"Total: {basket_item['total_price']} UZS"
            
    # Recreate the message with updated quantity
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Delete", callback_data=f"delete_cart_{basket_item['id']}"),
        ],
        [
            InlineKeyboardButton(text="➕ 1", callback_data=f"add_{basket_item['id']}"),
            InlineKeyboardButton(text="➖ 1", callback_data=f"subtract_{basket_item['id']}"),
        ]
        ])
    updated_text = '\n'.join(lines)
    await callback.message.edit_text(updated_text, reply_markup=keyboard)
    
    await callback.answer("Item substracted")






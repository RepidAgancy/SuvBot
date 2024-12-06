from aiogram import F, Router
from aiogram.types import Message

import database.requests as rq
import markups as btn

order_item_router = Router()


@order_item_router.message(F.text == '🛒 Korzinka')
async def all_product(message:Message):
    await message.answer("All products", reply_markup=await rq.get_all_order_item_keyboard())


# @order_item_router.message(F.text)
# async def handle_product_selection(message: Message):
#     product = await rq.get_product_by_name(message.text[:-1])
#     await rq.create_order_item(product_id=product.id)
#     await message.answer("Product added basket successfully")



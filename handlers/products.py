from aiogram import F, Router
from aiogram.types import Message

import database.requests as rq
import markups as btn

product_router = Router()


@product_router.message(F.text == '💧 Mahsulotlar')
async def all_product(message:Message):
    await message.answer("All products", reply_markup=await rq.all_products_keyboard())


@product_router.message(F.text)
async def handle_product_selection(message: Message):
    product = await rq.get_product_by_litr(message.text[:-1])
    await rq.create_order_item(product['id'],0,0)
    await message.answer(f"Product added basket successfully {product['id']}")



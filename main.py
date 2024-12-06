import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers.registrtion import regis_router
from handlers.order_product import order_router
from handlers.products import product_router
from handlers.order_item import order_item_router

from  database.models import async_main 

bot = Bot(token="7616860051:AAGChACPznkdKfvJU2rgQJ6JrnvHacmJNwg")
dp = Dispatcher()

dp.include_router(regis_router)
dp.include_router(order_router)
dp.include_router(product_router)
dp.include_router(order_item_router)



async def main():
    await dp.start_polling(bot)
    await async_main()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

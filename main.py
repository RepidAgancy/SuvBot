import asyncio
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher

from handlers.registrtion import regis_router
from handlers.order_product import order_router
from handlers.products import product_router
from handlers.order_item import order_item_router
from handlers.admin_page import admin_router
import database.requests as rq
from aiogram.types import InputFile

from  database.models import async_main 

async def send_notification_for_user(bot: Bot, user_id: int):
    await bot.send_message(chat_id=user_id, text="Suvingiz kam qoldi, yana buyurtma qilishni xoxlaysizmi")


    
bot = Bot(token="7616860051:AAGChACPznkdKfvJU2rgQJ6JrnvHacmJNwg")
dp = Dispatcher()


dp.include_router(admin_router)
dp.include_router(regis_router)
dp.include_router(order_router)
dp.include_router(product_router)
dp.include_router(order_item_router)


async def main():
    scheduler = AsyncIOScheduler()
    orders = await rq.get_all_orders_user()

    for order in orders:
        
        created_at = order['created_at']
        user_id = order['user_id'] 
        run_date = created_at + timedelta(days=2)
        logging.info(run_date)
    

        scheduler.add_job(send_notification_for_user, trigger='date',run_date=run_date,kwargs={'bot':bot,'user_id':user_id})
    scheduler.start()
    await dp.start_polling(bot)
    await async_main()
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

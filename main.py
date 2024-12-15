import asyncio
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from aiogram import Bot, Dispatcher

from handlers.registrtion import regis_router
from handlers.order_product import order_router
from handlers.products import product_router
from handlers.order_item import order_item_router
from handlers.admin_page import admin_router
from database.models import jobstores
import database.requests as rq

from  database.models import async_main 
    
bot = Bot(token="7616860051:AAGChACPznkdKfvJU2rgQJ6JrnvHacmJNwg")


scheduler = AsyncIOScheduler(jobstores)

async def send_notification_for_user(bot: Bot):
    # Replace with your actual function to get users to notify
    get_users = rq.get_order_by_notify_user(datetime=datetime.now() - timedelta(days=2))
    logging.info(get_users)
    
    # Iterate through the list of users and notify each
    if get_users:
        for user in get_users:
            await bot.send_message(
                chat_id=user['user_id'], 
                text="Suvingiz kam qoldi, yana buyurtma qilishni xoxlaysizmi?"
        )

scheduler.add_job(
    send_notification_for_user, 
    trigger=IntervalTrigger(days=1),  
    kwargs={'bot':bot}  
)

async def main():
    scheduler.start()
    await dp.start_polling(bot)
    await async_main()


dp = Dispatcher()





dp.include_router(admin_router)
dp.include_router(regis_router)
dp.include_router(order_router)
dp.include_router(product_router)
dp.include_router(order_item_router)



    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")




    
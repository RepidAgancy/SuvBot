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
from database.models import async_session
from database.models import Order
from apscheduler.triggers.date import DateTrigger
from aiogram.utils.i18n import I18n 
from sqlalchemy import select

from  database.models import async_main 
    
bot = Bot(token="7616860051:AAGChACPznkdKfvJU2rgQJ6JrnvHacmJNwg")


scheduler = AsyncIOScheduler()

dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(regis_router)
dp.include_router(order_router)
dp.include_router(product_router)
dp.include_router(order_item_router)

scheduled_orders = set()

async def send_notification(bot: Bot, user_id: int):
    """Send a notification to the user."""
    await bot.send_message(
        chat_id=user_id,
        text="Suvingiz kam qoldi, yana buyurtma qilishni xoxlaysizmi?"
    )

async def monitor_and_schedule_orders(bot: Bot):
    """Continuously monitor the database for new orders and schedule notifications."""
    while True:
        async with async_session() as session:
            async with session.begin():
                # Query orders that need notifications and have not been scheduled
                result = await session.execute(
                    select(Order).where(
                        Order.notify_user > datetime.now(),
                        Order.is_checked == True
                    )
                )
                orders = result.scalars().all()

                for order in orders:
                    if order.id not in scheduled_orders:
                        logging.info(f"Scheduling notification for Order ID {order.id} at {order.notify_user}")
                        scheduler.add_job(
                            send_notification,
                            trigger=DateTrigger(run_date=order.notify_user),
                            kwargs={'bot': bot, 'user_id': int(order.user_id)},
                        )
                        scheduled_orders.add(order.id)
        
        # Sleep for a short interval before checking again
        await asyncio.sleep(10)





async def main():
    scheduler.start()
    asyncio.create_task(monitor_and_schedule_orders(bot))
    
    await dp.start_polling(bot)
    await async_main()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")




    
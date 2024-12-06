from database.models import async_session
from database.models import User, OrderItem, Product
from sqlalchemy import select

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

async def set_user(tg_id: int):
    async with async_session as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def create_user(tg_id: int, language: str, phone_number: str):
    async with async_session() as session:
        async with session.begin():
            user = User(tg_id=tg_id, language=language, phone_number=phone_number)
            session.add(user)
            await session.commit()

async def get_user(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).filter(User.tg_id == tg_id))
            user = result.scalars().first()  
            return user
        
async def all_products_keyboard():
    async with async_session() as session:
        async with session.begin():
            # Fetch only necessary fields from the database
            result = await session.execute(select(Product.id, Product.liters))
            products = result.all()  # Returns a list of tuples (id, liters)

    keyboard = []
    row = []
    for i, (product_id, liters) in enumerate(products, start=1):
        row.append(KeyboardButton(text=f"{liters}L"))  # Use `liters` directly

        if i % 2 == 0 or i == len(products):
            keyboard.append(row)
            row = []  

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
        
async def create_product(*args):
    async with async_session() as session:
        async with session.begin():
            order = Product(*args)
            session.add(order)
            return session.commit()
        

async def get_product_by_litr(product_litr: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Product).where(Product.liters == int(product_litr)))
            product =  result.scalars().first()
            return {'id':product.id}
        

async def create_order_item(product_id: int):
    async with async_session() as session:
        async with session.begin():
            order_item = OrderItem(product_id=product_id,quantity=1,)
            session.add(order_item)
            return session.commit()

async def get_order_items():
    async with async_session() as session: 
        async with session.begin():
            result = await session.execute(select(OrderItem)) 
            return result.scalars().all()
        

async def get_all_order_item_keyboard():
    async with async_session() as session:
        async with session.begin():
            # Query all OrderItem records
            result = await session.execute(select(OrderItem))
            order_items = result.scalars().all()
    
    # Create the inline keyboard
    keyboard = InlineKeyboardMarkup(row_width=3)  # Adjust row width as needed

    for item in order_items:
        # Add a row for each OrderItem with its unique ID and buttons
        keyboard.add(
            InlineKeyboardButton(f"{item.name} (+1)", callback_data=f"add_{item.id}"),
            InlineKeyboardButton(f"{item.name} (-1)", callback_data=f"remove_{item.id}"),
            InlineKeyboardButton(f"Delete {item.name}", callback_data=f"delete_{item.id}")
        )
    
    return keyboard

            

        

        


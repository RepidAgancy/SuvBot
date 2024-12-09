from database.models import async_session
from database.models import User, Order, Product, Basket,BasketItem

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database.sync_to_async import get_all_items

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
            return {'id':user.id, 'lang':user.language}
        

async def change_user_lang(tg_id:int, lang:str):
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(select(User).where(User.tg_id == tg_id))
            users =  user.scalar_one_or_none()
            users.language = lang
            await session.commit()
            return {'lang':users.language}


async def all_products_keyboard():
    async with async_session() as session:
        async with session.begin():
            # Fetch only necessary fields from the database
            result = await session.execute(select(Product.id, Product.litrs))
            products = result.all()  # Returns a list of tuples (id, liters)

    keyboard = []
    row = []
    for i, (product_id, name) in enumerate(products, start=1):
        row.append(KeyboardButton(text=f"{name}L"))  # Use `liters` directly

        if i % 2 == 0 or i == len(products):
            keyboard.append(row)
            row = []  
    keyboard.append([KeyboardButton(text='Back')])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


async def add_basket_item(product_id:int, user_id:int, quantity = 1):
    async with async_session() as session:
        async with session.begin():
            basket_query = await session.execute(select(Basket).where(Basket.user_id == user_id))
            basket = basket_query.scalars().first()

            if not basket:
                basket = Basket(user_id=user_id)
                session.add(basket)
                await session.flush()

            basket_item = BasketItem(product_id=product_id,quantity=quantity,basket_id=basket.id,)
            session.add(basket_item)
            await session.commit()
    return {"message": "Basket item added successfully"}



async def get_all_basket_items_with_products(user_id: int):
    async with async_session() as session:
        async with session.begin():
            basket = await session.execute(select(Basket).where(Basket.user_id == user_id))
            basket = basket.scalars().first()

            if not basket:
                return {"message": "Basket not found"}

           
            basket_items = await session.execute(
                select(BasketItem).where(BasketItem.basket_id == basket.id,BasketItem.ordered==False).options(selectinload(BasketItem.product))
            )
            items = basket_items.scalars().all()
            
            return await get_all_items(items)
        

async def delete_basket(basket_id: int):
    async with async_session() as session:
        async with session.begin():
            # Fetch the basket associated with the user
            basket = await session.execute(select(BasketItem).where(BasketItem.id == basket_id))
            basket = basket.scalars().first()

            # Check if the basket exists
            if not basket:
                return {"message": "Basket not found"}
            
            # Delete the basket
            await session.delete(basket)  # Delete the Basket object
            await session.commit()  # Commit the transaction

    return {"message": "Basket deleted successfully"}


async def add_cart_quantity(basket_id: int):
    async with async_session() as session:
        async with session.begin():

            result = await session.execute(select(BasketItem).where(BasketItem.id == basket_id))
            basket_item = result.scalar_one_or_none()
            basket_item.quantity += 1
    
        
async def substratc_cart_quantity(basket_id: int):
    async with async_session() as session:
        async with session.begin():

            result = await session.execute(select(BasketItem).where(BasketItem.id == basket_id))
            basket_item = result.scalar_one_or_none()
            basket_item.quantity -= 1


async def get_basket_item(basket_id:int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(BasketItem).where(BasketItem.id == basket_id))
            basket_item = result.scalar_one_or_none()
            product = await session.execute(select(Product).where(Product.id==basket_item.product_id))
            product_price = product.scalar_one_or_none()
            return {'id':basket_item.id ,'quantity':basket_item.quantity,'total_price':basket_item.quantity*product_price.price}
            

async def create_product(*args):
    async with async_session() as session:
        async with session.begin():
            product = Product(*args)
            session.add(product)
            await session.commit()
        

async def get_product_by_litr(product_litr: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Product).where(Product.litrs == int(product_litr)))
            product =  result.scalars().first()
            return {'id':product.id}
        

async def create_order(*args, **kwargs):
    async with async_session() as session: 
        async with session.begin():
            order = Order(**kwargs)
            session.add(order)
            await session.flush()

            result = await session.execute(select(BasketItem).where(BasketItem.basket_id==kwargs['basket_id']))
            basket_items = result.scalars().all()  

            for basket_item in basket_items:
                basket_item.ordered = True

            await session.commit()

async def get_basket(user_id:int):
    async with async_session() as session:
        async with session.begin():
            basket = await session.execute(select(Basket).where(Basket.user_id==user_id))
            result = basket.scalars().first()
            return {'id':result.id}
        
            

        

        


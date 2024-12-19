import logging

from datetime import datetime, timedelta

from database.models import async_session
from database.models import User, Order, Product, Basket,BasketItem
from apscheduler.triggers.date import DateTrigger

from utils.translation import translate as _
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from database.sync_to_async import get_all_items

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def set_user(tg_id: int):
    async with async_session as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def create_user(tg_id: int, language: str, phone_number: str, company_name:str, user_type:str):
    async with async_session() as session:
        async with session.begin():
            user = User(tg_id=tg_id, language=language, phone_number=phone_number,company_name=company_name, user_type=user_type)
            session.add(user)
            await session.commit()


async def get_user(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).filter(User.tg_id == tg_id))
            user = result.scalar_one_or_none()
            if user:
                return {'id': user.id, 'lang': user.language} if user else None
            return {'message':'Not found'}
        

async def get_all_orders_user():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(Order))
            order_result = result.scalars().all()
            # orders = [{'user_id': order.user.id, 'created_at': order.created_at} for order in order_result]
            return [{'user_id':order.user_id, 'created_at':order.created_at} for order in order_result]
        

async def change_user_lang(tg_id:int, lang:str):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.tg_id == tg_id))
            user = result.scalar_one_or_none()  # Retrieve the user object
            
            if user:
                user.language = lang  # Update the language
                await session.commit()  # Commit the transaction

            else:
                raise ValueError("User not found")


async def all_products_keyboard(lang):
    async with async_session() as session:
        async with session.begin():
            # Fetch only necessary fields from the database
            result = await session.execute(select(Product.id, Product.name))
            products = result.all()  # Returns a list of tuples (id, liters)

    keyboard = []
    row = []
    for i, (product_id, name) in enumerate(products, start=1):
        row.append(KeyboardButton(text=f"{name}"))  # Use `liters` directly

        if i % 2 == 0 or i == len(products):
            keyboard.append(row)
            row = []  
    keyboard.append([KeyboardButton(text=_('Back',lang))])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


async def add_basket_item(product_id:int, user_id:int, quantity:int):
    async with async_session() as session:
        async with session.begin():
            basket_query = await session.execute(select(Basket).where(Basket.user_id == user_id, Basket.ordered == False))
            basket = basket_query.scalars().first()

            if not basket:
                basket = Basket(user_id=user_id)
                session.add(basket)
                await session.flush()

            product = await session.execute(select(Product).where(Product.id == product_id))
            result = product.scalars().first()
            basket.total_price += int(result.price) * quantity

            basket_item = BasketItem(product_id=product_id,quantity=quantity,basket_id=basket.id,)
            session.add(basket_item)
            await session.commit()
    return {"message": "Basket item added successfully"}


async def add_basket_item_user_desire(product_id:int, user_id:int, quantity:int):
    async with async_session() as session:
        async with session.begin():
            basket = Basket(user_id=user_id)
            session.add(basket)
            await session.flush()
            basket_query = await session.execute(select(Basket)
                                           .where(Basket.user_id==user_id, Basket.ordered==False)
                                           .order_by(desc(Basket.id)))
            basket = basket_query.scalar_one_or_none()

            product = await session.execute(select(Product).where(Product.id == product_id))
            result = product.scalars().first()
            basket.total_price += int(result.price) * quantity

            basket_item = BasketItem(product_id=product_id,quantity=quantity,basket_id=basket.id,)
            session.add(basket_item)
            await session.commit()
    return {"message": "Basket item added successfully"}


async def get_all_basket_items_with_products(user_id: int):
    async with async_session() as session:
        async with session.begin():
            basket = await session.execute(select(Basket).where(Basket.user_id == user_id, Basket.ordered == False))
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

async def delete_basket_choose(user_id: int):
    try:
        async with async_session() as session:
            async with session.begin():
                # Fetch the basket for the user
                basket_query = await session.execute(
                    select(Basket).where(Basket.user_id == user_id,Basket.ordered==False)
                )
                basket = basket_query.scalars().first()
                
                if not basket:
                    return {"success": False, "message": "Basket not found"}
                
                # Delete the basket
                await session.delete(basket)
                await session.flush()

        return {"success": True, "message": "Basket deleted successfully"}

    except Exception as e:
        logging.error(f"Error deleting basket for user {user_id}: {e}")
        return {"success": False, "message": "An error occurred while deleting the basket"}


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


async def get_basket_item_change(basket_id:int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(BasketItem).where(BasketItem.id == basket_id))
            basket_item = result.scalar_one_or_none()
            product = await session.execute(select(Product).where(Product.id==basket_item.product_id))
            product_price = product.scalar_one_or_none()
            return {'id':basket_item.id ,'quantity':basket_item.quantity,'total_price':basket_item.quantity*product_price.price}
            

async def get_basket_item(user_id:int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                select(BasketItem)
                .join(Basket)  # Join the BasketItem with Basket
                .where(BasketItem.ordered == False, Basket.user_id == user_id, )
            )
            return result.scalars().first()


async def create_product(*args):
    async with async_session() as session:
        async with session.begin():
            product = Product(*args)
            session.add(product)
            await session.commit()
        

async def get_product_by_litr(product_name: str):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Product).where(Product.name == product_name))
            product =  result.scalars().first()
            if product:
                return {'id':product.id,'image':product.image, 'price':product.price, 'name':product.name}
            return {'message':'Product not found'}
        

async def create_order(*args, **kwargs):
    async with async_session() as session: 
        async with session.begin():
            basket = await session.execute(select(Basket).where(Basket.id == kwargs['basket_id'], Basket.ordered == False))
            basket_result = basket.scalar_one_or_none()
            basket_result.ordered = True

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
            basket = await session.execute(
                select(Basket)
                .where(Basket.user_id == user_id, Basket.ordered==False)
            )
            result = basket.scalars().first()

            if result:
                return {'id': result.id}
            return {'message': 'No basket found'}
        

async def get_all_orders():
    async with async_session() as session:
        async with session.begin():
            # Perform the query to get both orders and basket items
            
            query = (
                select(Order, BasketItem, User)
                .options(selectinload(Order.user),
                    selectinload(BasketItem.product))
                .join(BasketItem, BasketItem.basket_id == Order.basket_id)
                .join(User, User.tg_id == Order.user_id)
                .where(BasketItem.ordered == True, Order.is_checked == False)
            )

            result = await session.execute(query)
            if not result.first():
                return {'message':'Buyurtmalar hali yoq'}

            order_items = {}
            for order, basket_item, user in result.all():
                if order.id not in order_items:
                    order_items[order.id] = {
                        'order_id': order.id,
                        'company_name': user.company_name if user else None,
                        'company_contact': user.phone_number if user else None,
                        'number_employee': order.number_employee,
                        'location':order.location,
                        'time_drink': order.time_drink,
                        'created_at': order.created_at,
                        'products': []
                    }
                # Append product details to the products list
                product = basket_item.product
                order_items[order.id]['products'].append({
                    'basket_id': basket_item.basket_id,
                    'product_name': product.name,
                    'quantity': basket_item.quantity,
                    'price': product.price,
                })

            # Convert to a list of orders
            return list(order_items.values())
        

async def get_near_expiry_orders():
    async with async_session() as session:
        async with session.begin():
            # Get orders where the `is_checked` field is True
            expiring_orders = await session.execute(select(Order).where(Order.is_checked == True))
            result = expiring_orders.scalars().all()
            return result
        

async def add_product(name:str, price:float, image):
    async with async_session() as session:
        async with session.begin():
            product = Product(
                name=name,
                price=price,
                image=image
            )
            session.add(product)
            await session.commit()
            return {'message':"Product added successfuly"}
        

async def get_all_products():
    async with async_session() as session:
        async with session.begin():
            all_product = await session.execute(select(Product))
            results = all_product.scalars().all()
            return [{'id':result.id, 'name':result.name, 'price':result.price, 'image':result.image} for result in results]
        
        
async def get_order_by_notify_user(datetime:datetime):
    async with async_session() as session:
        async with session.begin():
            results = await session.execute(select(Order).where(Order.notify_user==datetime))
            orders = results.scalars().all()
            return [
                {'id':result.id,
                 'user_id':result.user_id,
                 'notify_user':result.notify_user
                 }
                 for result in orders
            ]


async def order_make_done(order_id:int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Order).where(Order.id == order_id))
            order = result.scalars().first()
            order.is_checked = True


async def last_order_repeat(user_id:int,lang):
    async with async_session() as session:
        async with session.begin():

            last_order_query = (
                select(Order, User)
                .options(selectinload(Order.user))
                .where(Order.is_checked == True, Order.user_id == user_id)
                .order_by(Order.created_at.desc())
                .limit(1)  # Only fetch the latest order
            )
            last_order_result = await session.execute(last_order_query)
            if not last_order_result.first():
                return {'message':_('Sizda hali buyurtmalar yoq',lang)}
            
            last_order,user = last_order_result.first()  # Get the last order or None
            
            if not last_order:
                return None  # No orders found for the user
            
            # Step 2: Query all BasketItems and Products for the last order
            basket_items_query = (
                select(BasketItem)
                .options(selectinload(BasketItem.product))
                .where(BasketItem.basket_id == last_order.basket_id, BasketItem.ordered == True)
            )
            basket_items_result = await session.execute(basket_items_query)
            basket_items = basket_items_result.scalars().all()
            
            # Step 3: Construct the response
            order_item = {
                'order_id': last_order.id,
                'company_name':user.company_name,
                'basket_id':last_order.basket_id,
                'company_contact':user.phone_number,
                'location':last_order.location,
                'number_employee': last_order.number_employee,
                'time_drink': last_order.time_drink,
                'created_at': last_order.created_at,
                'products': []
            }
            
            for basket_item in basket_items:
                product = basket_item.product
                order_item['products'].append({
                    'basket_id': basket_item.basket_id,
                    'product_name': product.name,
                    'quantity': basket_item.quantity,
                    'price': product.price,
                })
            
            return order_item
        

async def get_all_orders_done():
    async with async_session() as session:
        async with session.begin():
            # Perform the query to get both orders and basket items
            
            query = (
                select(Order, BasketItem, User)
                .options(selectinload(Order.user),
                    selectinload(BasketItem.product))
                .join(BasketItem, BasketItem.basket_id == Order.basket_id)
                .join(User, User.tg_id == Order.user_id)
                .where(BasketItem.ordered == True, Order.is_checked == True)
            )

            result = await session.execute(query)

            order_items = {}
            for order, basket_item, user in result.all():
                if order.id not in order_items:
                    order_items[order.id] = {
                        'order_id': order.id,
                        'company_name': user.company_name if user else None,
                        'company_contact': user.phone_number if user else None,
                        'number_employee': order.number_employee,
                        'location':order.location,
                        'time_drink': order.time_drink,
                        'created_at': order.created_at,
                        'products': []
                    }
                # Append product details to the products list
                product = basket_item.product
                order_items[order.id]['products'].append({
                    'basket_id': basket_item.basket_id,
                    'product_name': product.name,
                    'quantity': basket_item.quantity,
                    'price': product.price,
                })

            # Convert to a list of orders
            return list(order_items.values())
        

async def repeat_order_create(*args,**kwargs):
    async with async_session() as session:
        async with session.begin():
            order = Order(**kwargs)
            session.add(order)
            await session.commit()



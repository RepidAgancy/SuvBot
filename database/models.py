import asyncio

from sqlalchemy import BigInteger, String, ForeignKey, Integer, DateTime, Boolean, Column, Float, LargeBinary
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    tg_id = Column(BigInteger)
    language = Column(String)
    phone_number = Column(String)

    orders = relationship("Order", back_populates='user')
    basket = relationship("Basket", back_populates="user", uselist=False)  # One basket per user


# Product Model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String, nullable=False)

    basket_items = relationship("BasketItem", back_populates="product")


# Basket Model
class Basket(Base):
    __tablename__ = 'baskets'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="basket")
    basket_items = relationship("BasketItem", back_populates="basket", cascade="all, delete-orphan")


# BasketItem Model
class BasketItem(Base):
    __tablename__ = 'basket_items'

    id = Column(Integer, primary_key=True, index=True)
    basket_id = Column(Integer, ForeignKey("baskets.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    ordered = Column(Boolean, default=False)

    # Relationships
    basket = relationship("Basket", back_populates="basket_items")
    product = relationship("Product", back_populates="basket_items")


# Order Model
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    basket_id = Column(Integer, ForeignKey('baskets.id'), nullable=False)
    company_name = Column(String, nullable=False)
    company_contact = Column(String, nullable=False)
    number_employee = Column(Integer, nullable=False)
    time_drink = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    notify_user = Column(DateTime)
    is_checked = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="orders")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(async_main())
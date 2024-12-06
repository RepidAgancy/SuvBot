import asyncio

from sqlalchemy import BigInteger, String, ForeignKey, Integer, DateTime, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    language: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)

    orders = relationship("Order", back_populates='user')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String)
    company_contact: Mapped[str] = mapped_column(String)
    number_employees: Mapped[int] = mapped_column(Integer)  
    time_to_drink: Mapped[int] = mapped_column(Integer)     
    order_item_id: Mapped[int] = mapped_column(Integer)     
    created_at: Mapped[str] = mapped_column(DateTime)  
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='orders') 
    order_items = relationship('OrderItem', back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id')) 
    quantity: Mapped[int] = mapped_column(Integer)

    product = relationship('Product', back_populates='order_items')
    order = relationship('Order', back_populates='order_items') 


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    liters: Mapped[int] = mapped_column(Integer)  
    price: Mapped[float] = mapped_column(DECIMAL)

    order_items = relationship('OrderItem', back_populates='product')


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(async_main())
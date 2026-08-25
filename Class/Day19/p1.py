# Setting up SQL Alchemy ORM
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# 1. creating an Engine
engine = create_engine('sqlite:///advpy3.db', echo=False) #echo=True shows SQL

# 2. create Base class
Base = declarative_base()

# 3. Define Models(Python classes)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    city = Column(String(50))
    created_at = Column(DateTime,default=datetime.now)

    orders = relationship('Order',back_populates='user')

    def __repr__(self):
        return f"User(id={self.id},name='{self.name}',age={self.age},city='{self.city}')"

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float)
    stock = Column(Integer,default=0)
    category = Column(String(50))

    order_item = relationship('OrderItem', back_populates='product')

    def __repr__(self):
        return f"Product(id={self.id},name='{self.name}',price={self.price},stock={self.stock})"

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer,primary_key=True, autoincrement=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    order_date = Column(DateTime, default=datetime.now)
    total_amount = Column(Float, default=0.0)
    status = Column(String(20), default='pending')

    user = relationship('User',back_populates='orders')
    items = relationship('OrderItem', back_populates='order')

    def __repr__(self):
        return f"Order(id={self.id},user_id={self.user_id},total = {self.total_amount},status='{self.status}')"

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer,primary_key=True, autoincrement=True)
    order_id = Column(Integer,ForeignKey('orders.id'))
    product_id = Column(Integer,ForeignKey('products.id'))
    quantity = Column(Integer, default=1)   
    unit_price = Column(Float) 

    order = relationship('Order',back_populates='items')
    product = relationship('Product', back_populates='order_items')

    def __repr__(self):
        return f"OrderItem(order_id={self.order_id},product_id={self.product_id},qty={self.quantity})"

# 4. Create Table
Base.metadata.create_all(engine)
print("Tables Created Successfully")

# 5 Create session
Session = sessionmaker(bind=engine)
session = Session()
from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default='CURRENT_TIMESTAMP')


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(150))
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(Enum('Electronics', 'Clothing', 'Books', 'Other'), nullable=False)


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    position = Column(Enum('Manager', 'Storekeeper', 'Support'), nullable=False)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    order_date = Column(DateTime, default='CURRENT_TIMESTAMP')
    total_price = Column(Float, nullable=False)
    is_processed = Column(Boolean, default=False)

    customer = relationship("Customer", back_populates="orders")
    employee = relationship("Employee")


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")

# Relace pro propojení tabulek
Customer.orders = relationship("Order", order_by=Order.id, back_populates="customer")
Order.order_items = relationship("OrderItem", order_by=OrderItem.id, back_populates="order")

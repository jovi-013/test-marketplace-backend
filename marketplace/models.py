from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    user_type = Column(String) # "buyer", "seller", "admin"
    
    selling_products = relationship("SellerProduct", back_populates="seller")
    purchase_orders = relationship("Order", foreign_keys="[Order.buyer_id]", back_populates="buyer")
    sale_orders = relationship("Order", foreign_keys="[Order.seller_id]", back_populates="seller")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    image_url = Column(String, nullable=True)

    sellers = relationship("SellerProduct", back_populates="product")

class SellerProduct(Base):
    __tablename__ = "seller_products"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    seller_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    seller = relationship("User", back_populates="selling_products")
    product = relationship("Product", back_populates="sellers")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"))
    seller_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float)
    status = Column(String, default="PENDING") # PENDING, CONFIRMED, CANCELED

    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="purchase_orders")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="sale_orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    seller_product_id = Column(Integer, ForeignKey("seller_products.id"))
    quantity = Column(Integer)
    price_at_purchase = Column(Float)

    order = relationship("Order", back_populates="items")
    product_item = relationship("SellerProduct")

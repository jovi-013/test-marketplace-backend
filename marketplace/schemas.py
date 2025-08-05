from pydantic import BaseModel, EmailStr
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str

# SellerProduct
class SellerProductBase(BaseModel):
    price: float
    quantity: int

class SellerProductCreate(SellerProductBase):
    product_id: int

class SellerProduct(SellerProductBase):
    id: int
    seller_id: int
    product_id: int

    class Config:
        from_attributes = True

# Products
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    sellers: List[SellerProduct] = []

    class Config:
        from_attributes = True

# Users
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    user_type: str

class User(UserBase):
    id: int
    is_active: bool
    user_type: str
    selling_products: List[SellerProduct] = []

    class Config:
        from_attributes = True

# OrderItem
class OrderItemBase(BaseModel):
    seller_product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    price_at_purchase: float

    class Config:
        from_attributes = True

# Order
class OrderBase(BaseModel):
    seller_id: int
    items: List[OrderItemCreate]

class OrderCreate(OrderBase):
    pass

class Order(BaseModel):
    id: int
    buyer_id: int
    seller_id: int
    total_price: float
    status: str
    items: List[OrderItem]

    class Config:
        from_attributes = True
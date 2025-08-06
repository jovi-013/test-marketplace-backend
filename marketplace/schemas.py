from pydantic import BaseModel, EmailStr
from typing import List

# Simple Schemas for Nesting, to prevent circular loops
class ProductSimple(BaseModel):
    id: int
    name: str
    description: str | None = None
    
    class Config:
        from_attributes = True

# Base Schemas
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None

class SellerProductBase(BaseModel):
    price: float
    quantity: int

class UserBase(BaseModel):
    email: EmailStr

class OrderItemBase(BaseModel):
    seller_product_id: int
    quantity: int

# Schemas for creating or input
class ProductCreate(ProductBase):
    pass

class SellerProductCreate(SellerProductBase):
    product_id: int

class UserCreate(UserBase):
    password: str
    user_type: str

class OrderItemCreate(OrderItemBase):
    pass

class OrderCreate(BaseModel):
    seller_id: int
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: str

# Schemas for reading or output

class Token(BaseModel):
    access_token: str
    token_type: str

class SellerProduct(SellerProductBase):
    id: int
    seller_id: int
    product_id: int
    product: ProductSimple

    class Config:
        from_attributes = True

class Product(ProductBase):
    id: int
    sellers: List[SellerProduct] = []

    class Config:
        from_attributes = True

class OrderItem(OrderItemBase):
    id: int
    price_at_purchase: float
    product_item: SellerProduct

    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    buyer_id: int
    seller_id: int
    total_price: float
    status: str
    items: List[OrderItem]

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    is_active: bool
    user_type: str
    selling_products: List[SellerProduct] = []
    purchase_orders: List[Order] = []
    sale_orders: List[Order] = []

    class Config:
        from_attributes = True
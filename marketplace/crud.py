from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user_by_email(db: AsyncSession, email: str):
    query = select(models.User).options(selectinload(models.User.selling_products)).filter(models.User.email == email)
    result = await db.execute(query)
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password, 
        user_type=user.user_type
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    query = (
        select(models.User)
        .options(selectinload(models.User.selling_products))
        .filter(models.User.id == db_user.id)
    )
    result = await db.execute(query)
    return result.scalars().first()

# Product CRUD Functions
async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    
    query = select(models.Product).options(selectinload(models.Product.sellers)).filter(models.Product.id == db_product.id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(models.Product).options(selectinload(models.Product.sellers)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Seller-Product CRUD Functions
async def add_product_to_seller_inventory(db: AsyncSession, seller_product: schemas.SellerProductCreate, seller_id: int):
    existing_entry = await db.execute(
        select(models.SellerProduct).filter(
            models.SellerProduct.seller_id == seller_id,
            models.SellerProduct.product_id == seller_product.product_id
        )
    )
    if existing_entry.scalars().first():
        raise HTTPException(status_code=400, detail="Seller is already selling this product.")

    master_product = await db.get(models.Product, seller_product.product_id)
    if not master_product:
        raise HTTPException(status_code=404, detail="Master product not found.")

    db_seller_product = models.SellerProduct(
        price=seller_product.price,
        quantity=seller_product.quantity,
        product_id=seller_product.product_id,
        seller_id=seller_id
    )
    db.add(db_seller_product)
    await db.commit()
    await db.refresh(db_seller_product)

    query = (
        select(models.SellerProduct)
        .options(selectinload(models.SellerProduct.product))
        .filter(models.SellerProduct.id == db_seller_product.id)
    )
    result = await db.execute(query)
    return result.scalars().first()

async def get_seller_inventory(db: AsyncSession, seller_id: int):
    query = (
        select(models.SellerProduct)
        .options(selectinload(models.SellerProduct.product))
        .filter(models.SellerProduct.seller_id == seller_id)
    )
    result = await db.execute(query)
    return result.scalars().all()

async def get_product(db: AsyncSession, product_id: int):
    query = (
        select(models.Product)
        .options(selectinload(models.Product.sellers))
        .filter(models.Product.id == product_id)
    )
    result = await db.execute(query)
    return result.scalars().first()

# Order CRUD Functions
async def create_order(db: AsyncSession, order_data: schemas.OrderCreate, buyer_id: int):
    total_price = 0
    items_to_process = []

    for item_data in order_data.items:
        seller_product = await db.get(models.SellerProduct, item_data.seller_product_id)

        if not seller_product or seller_product.seller_id != order_data.seller_id:
            raise HTTPException(status_code=404, detail=f"Product item with id {item_data.seller_product_id} not found for this seller.")

        if seller_product.quantity < item_data.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product id {seller_product.product_id}. Available: {seller_product.quantity}, Requested: {item_data.quantity}")

        total_price += seller_product.price * item_data.quantity
        items_to_process.append((seller_product, item_data.quantity))

    new_order = models.Order(
        buyer_id=buyer_id,
        seller_id=order_data.seller_id,
        total_price=total_price
    )
    db.add(new_order)
    
    await db.flush()

    order_id_for_query = new_order.id

    for product, quantity_ordered in items_to_process:
        order_item = models.OrderItem(
            order_id=new_order.id,
            seller_product_id=product.id,
            quantity=quantity_ordered,
            price_at_purchase=product.price
        )
        db.add(order_item)
        product.quantity -= quantity_ordered

    await db.commit()

    query = (
        select(models.Order)
        .options(selectinload(models.Order.items).options(selectinload(models.OrderItem.product_item).options(selectinload(models.SellerProduct.product))))
        .filter(models.Order.id == order_id_for_query)
    )
    result = await db.execute(query)
    final_order = result.scalars().first()
    
    return final_order

async def get_orders_for_seller(db: AsyncSession, seller_id: int):
    query = (
        select(models.Order)
        .options(selectinload(models.Order.items))
        .filter(models.Order.seller_id == seller_id)
    )
    result = await db.execute(query)
    return result.scalars().all()

async def get_orders_for_buyer(db: AsyncSession, buyer_id: int):
    query = (
        select(models.Order)
        .options(selectinload(models.Order.items))
        .filter(models.Order.buyer_id == buyer_id)
    )
    result = await db.execute(query)
    return result.scalars().all()
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from .. import crud, schemas, models
from ..database import get_db
from ..dependencies import get_current_seller_user

router = APIRouter(
    prefix="/seller",
    tags=["seller"],
    dependencies=[Depends(get_current_seller_user)]
)

@router.post("/inventory", response_model=schemas.SellerProduct)
async def add_product_to_inventory(
    seller_product: schemas.SellerProductCreate,
    db: AsyncSession = Depends(get_db),
    current_seller: schemas.User = Depends(get_current_seller_user)
):
    """
    Allows a seller to add a MASTER product to their personal inventory,
    setting their own price and quantity.
    """
    return await crud.add_product_to_seller_inventory(
        db=db, seller_product=seller_product, seller_id=current_seller.id
    )

@router.get("/inventory", response_model=List[schemas.SellerProduct])
async def read_seller_inventory(
    db: AsyncSession = Depends(get_db),
    current_seller: schemas.User = Depends(get_current_seller_user)
):
    """
    Get the inventory for the currently logged-in seller.
    """
    return await crud.get_seller_inventory(db=db, seller_id=current_seller.id)

@router.get("/orders", response_model=List[schemas.Order])
async def read_seller_orders(
    db: AsyncSession = Depends(get_db),
    current_seller: schemas.User = Depends(get_current_seller_user)
):
    """
    Get all orders received by the currently logged-in seller.
    """
    return await crud.get_orders_for_seller(db=db, seller_id=current_seller.id)

@router.put("/orders/{order_id}", response_model=schemas.Order)
async def manage_order_status(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_seller: schemas.User = Depends(get_current_seller_user)
):
    """
    Allows a seller to update the status of one of their orders.
    """
    updated_order = await crud.update_order_status(
        db=db, order_id=order_id, seller_id=current_seller.id, new_status=order_update.status
    )
    
    query = (
        select(models.Order)
        .options(selectinload(models.Order.items))
        .filter(models.Order.id == updated_order.id)
    )
    result = await db.execute(query)
    return result.scalars().first()
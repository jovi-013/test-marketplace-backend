from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .. import crud, schemas
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

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .. import crud, schemas
from ..database import get_db
from ..dependencies import get_current_buyer_user

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("/", response_model=schemas.Order)
async def create_new_order(
    order: schemas.OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_buyer: schemas.User = Depends(get_current_buyer_user)
):
    """
    Create a new order. Buyer must login.
    Order contains items from a single seller.
    """
    return await crud.create_order(db=db, order_data=order, buyer_id=current_buyer.id)

@router.get("/my-history", response_model=List[schemas.Order])
async def read_buyer_order_history(
    db: AsyncSession = Depends(get_db),
    current_buyer: schemas.User = Depends(get_current_buyer_user)
):
    """
    Get order history for the currently logged-in buyer.
    """
    return await crud.get_orders_for_buyer(db=db, buyer_id=current_buyer.id)
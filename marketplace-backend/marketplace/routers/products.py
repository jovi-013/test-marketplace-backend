from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .. import crud, schemas
from ..database import get_db
from ..dependencies import get_current_admin_user

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.post("/", response_model=schemas.Product, dependencies=[Depends(get_current_admin_user)])
async def create_new_product(product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new master product. Admin only.
    """
    return await crud.create_product(db=db, product=product)

@router.get("/", response_model=List[schemas.Product])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all master products. Public can access.
    """
    products = await crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single master product by ID, including all sellers.
    Public can access.
    """
    db_product = await crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
"""
Routes pour la gestion des items
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter()

@router.get("/items", response_model=List[ItemResponse])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Récupère la liste des items"""
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Crée un nouvel item"""
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

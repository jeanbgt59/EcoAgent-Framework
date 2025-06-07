"""
Schémas Pydantic pour les items
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    owner_id: int

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ItemResponse(ItemBase):
    id: int
    is_active: bool
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

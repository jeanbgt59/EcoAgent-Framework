"""
Modèles de données
"""

from .user import User
from .item import Item

# Ajout des relations manquantes
from sqlalchemy.orm import relationship

# Relation items pour User
User.items = relationship("Item", back_populates="owner")

__all__ = ["User", "Item"]

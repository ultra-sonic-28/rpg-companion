import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeMeta

from rpg_companion.db.base import Base

def test_base_is_declarative_meta():
    """Vérifie que Base est bien une instance de DeclarativeMeta."""
    from sqlalchemy.orm import DeclarativeMeta
    assert isinstance(Base, DeclarativeMeta)


def test_inherited_class_can_define_columns():
    """Vérifie qu'on peut créer une classe héritée de Base avec colonnes et __tablename__."""
    class User(Base):
        __tablename__ = "user"
        id = Column(Integer, primary_key=True)
        name = Column(String)

    # Vérifie que User hérite bien de Base
    assert issubclass(User, Base)
    # Vérifie que User a un __tablename__ correct
    assert User.__tablename__ == "user"
    # Vérifie que les colonnes existent
    assert hasattr(User, "id")
    assert hasattr(User, "name")

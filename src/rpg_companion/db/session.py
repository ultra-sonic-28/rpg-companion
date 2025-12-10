from pathlib import Path
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Iterator, Optional
from contextlib import contextmanager

# ----------------------------------------------------------------------
# Déterminer l'emplacement de la base SQLite (dev + PyInstaller)
# ----------------------------------------------------------------------
if getattr(sys, 'frozen', False):
    # PyInstaller : extraction dans _MEIPASS
    BASE_DIR = Path(sys._MEIPASS) / "rpg_companion" / "data"
else:
    # Mode dev : src/rpg_companion/data
    BASE_DIR = Path(__file__).parent.parent / "data"

BASE_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_FILE = BASE_DIR / "d100.sqlite3"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

_engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=False,  # True pour debug SQL
    pool_pre_ping=True,
)

_SessionFactory = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)
Session = scoped_session(_SessionFactory)

@contextmanager
def get_session() -> Iterator[_SessionFactory]: # type: ignore
    """Context manager simple pour scope des sessions"""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

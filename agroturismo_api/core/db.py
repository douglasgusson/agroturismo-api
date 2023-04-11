from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from .config import DB_URI

engine = create_engine(
    DB_URI,
    connect_args={"check_same_thread": False},
    echo=True,
)


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


ActiveSession = Depends(get_session)

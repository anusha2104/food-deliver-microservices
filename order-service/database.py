
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://gather_user:gather_dev_password@localhost:5432/gather",
)

engine = create_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1),
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

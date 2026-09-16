import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite for the prototype. Swap DATABASE_URL to a Postgres URL (e.g. from
# Render/Supabase) in production -- no code changes needed elsewhere since
# SQLAlchemy abstracts the dialect.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./h2s_sentinel.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

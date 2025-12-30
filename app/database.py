# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For SQLite (creates a file named 'sql_app.db' in the backend folder)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# If you want to use PostgreSQL later, you would uncomment this:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the DB session in API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# WHY: Creates the database engine and session factory
# CONCEPT: SQLAlchemy is an ORM — it lets you write Python classes instead of raw SQL
# The engine is your connection to SQL Server
# SessionLocal is a factory that creates individual DB sessions per request

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# connect_args is not needed for SQL Server (unlike SQLite which needs check_same_thread)
engine = create_engine(DATABASE_URL, echo=True)
# echo=True logs all SQL queries — great for debugging, set False in production

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all your models will inherit from
Base = declarative_base()

# DEPENDENCY FUNCTION — FastAPI injects this into every route that needs DB
# It opens a session, yields it to the route, then ALWAYS closes it (finally block)
# This prevents connection leaks
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
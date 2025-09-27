from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.services.logger import agent_logger as logger

SQLALCHEMY_DATABASE_URL = 'sqlite:///./newsarticles.db'
#POSTGRES_DATABASE_URL = 'postgresql://postgres:postgres@localhost/TodoApplicationDatabase'


# Creating our enginer, needs database path, connect_args allows to define some kind of connection to a database.
# We have false for check_same_thread to prevent accident sharing of the same connection
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# The sessionLocal is an instance of the database 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating database object we can interact with
Base = declarative_base()

# FastAPI dependency to get the database session. Do not use this function directly if you are not using FastAPI, use SessionLocal instead.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
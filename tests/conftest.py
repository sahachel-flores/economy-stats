# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base

@pytest.fixture
def db_connection():
    """Create a fresh in-memory database for each test"""
    # In-memory database
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create session
    TestSessionLocal = sessionmaker(bind=engine)
    db = TestSessionLocal()
    
    yield db  # Test uses this db

    # Cleanup
    db.close()
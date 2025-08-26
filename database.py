from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL, SQLALCHEMY_ECHO

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=SQLALCHEMY_ECHO
)

# Create session factory
async_session_factory = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

def get_session_factory():
    """Get the session factory for dependency injection"""
    return async_session_factory

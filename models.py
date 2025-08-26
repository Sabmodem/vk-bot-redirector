import uuid
import datetime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Uuid, String, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

class Link(Base):
    __tablename__ = 'link'
    
    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True,default=lambda: uuid.uuid4())
    url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)    
    
class Mailing(Base):
    __tablename__ = 'mailing'
    
    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True,default=lambda: uuid.uuid4())
    text: Mapped[str] = mapped_column(String, nullable=False)
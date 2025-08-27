import uuid
from typing import List
import models

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_users(
    session: AsyncSession, 
    users: List[models.User] = []
) -> List[models.User]:
    session.add_all(users)
    await session.commit()
    return users

async def read_users(
    session: AsyncSession, 
    user_ids: List[uuid.UUID] = []
) -> List[models.User]:
    stmt = select(models.User).filter(models.User.id.in_(user_ids))
    result = await session.execute(stmt)
    return result.scalars().all()

async def read_mailings(
    session: AsyncSession, 
    mailing_ids: List[str] = []
) -> List[models.Mailing]:
    stmt = select(models.Mailing)
    if len(mailing_ids) > 0:
        stmt = stmt.filter(models.Mailing.id.in_(mailing_ids))
    result = await session.execute(stmt)
    return result.scalars().all()

async def read_links(
    session: AsyncSession, 
    link_ids: List[str] = []
) -> List[models.Link]:
    stmt = select(models.Link)
    if len(link_ids) > 0:
        stmt = stmt.filter(models.Link.id.in_(link_ids))
    result = await session.execute(stmt)
    return result.scalars().all()

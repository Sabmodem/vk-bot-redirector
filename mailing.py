from sqlalchemy.ext.asyncio import AsyncSession
from vkbottle import Bot
import crud, models
from vkbottle import Keyboard, KeyboardButtonColor, OpenLink
from typing import List
import random
from database import get_session_factory
import logging
import asyncio
from config import MAILING_INTERVAL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def mailing(bots: List[Bot]):
    session: AsyncSession = get_session_factory()
    users: List[models.User] = await crud.read_users(session)
    links: List[models.Link] = await crud.read_links(session)
    mailings: List[models.Mailing] = await crud.read_mailings(session)
    kb = Keyboard(inline=True)
    for link in links:
        kb.add(OpenLink(link.url, link.title), color=KeyboardButtonColor.POSITIVE).row()
    kb_json = kb.get_json()
    for user in users:
        text = random.choice(mailings).text.format(first_name=user.name)
        for bot in bots:
            try:
                await bot.api.messages.send(user_id=user.id, message=text, keyboard=kb_json)
            except Exception as e:
                logger.error('Error sending message to user', exc_info=True)
                
async def mailing_task(bots: List[Bot]):
    """A background task that monitors the database and manages bot lifecycles."""
    while True:
        try:
            await mailing(bots)
        except Exception as e:
            logger.error(f"Error in mailing task: {e}", exc_info=True)

        await asyncio.sleep(MAILING_INTERVAL)
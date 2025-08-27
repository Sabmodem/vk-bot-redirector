import logging
from typing import List
from vkbottle import API, Keyboard, KeyboardButtonColor, OpenLink
from vkbottle.bot import Bot, Message
from vkbottle.callback import BotCallback
from database import async_session_factory
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import models
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def get_user_name(
    message: Message,
    bot: Bot
) -> str:
    try:
        user_info = await bot.api.users.get(user_ids=message.peer_id)
        user = user_info[0]
        return user.first_name
    except Exception as e:
        logger.error('Error getting user name, returning default', exc_info=True)
        return 'Красавчик'

def create_bot(
    token: str, 
    webhook_url: str = None, 
    webhook_title: str = None
):
    vk_api = API(token)
    if webhook_title and webhook_url:
        callback = BotCallback(webhook_url, webhook_title)
        bot = Bot(api=vk_api, callback=callback)
    else:
        bot = Bot(api=vk_api)

    @bot.on.message()
    async def handle_start(message: Message):
        session: AsyncSession
        async with async_session_factory() as session:        
            user_name = await get_user_name(message, bot)
            try:
                await crud.create_users(session, [models.User(id=message.peer_id, name=user_name)])
            except Exception as e:
                logger.error('Error creating user', exc_info=True)
                
            links: List[models.Link] = await crud.read_links(session)
            mailings: List[models.Mailing] = await crud.read_mailings(session)
            kb = Keyboard(inline=True)
            for link in links:
                kb.add(OpenLink(link.url, link.title), color=KeyboardButtonColor.POSITIVE).row()
            text = random.choice(mailings).text
            await message.answer(text.format(first_name=user_name), keyboard=kb.get_json())

    return bot
import logging
from typing import List
from vkbottle import API, Keyboard, KeyboardButtonColor, OpenLink
from vkbottle.bot import Bot, Message
from vkbottle.callback import BotCallback
from .database import get_session_factory
import crud
import models
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

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
        await crud.create_users(get_session_factory(), [models.User(id=message.peer_id)])
        links: List[models.Link] = await crud.read_links(get_session_factory())
        mailings: List[models.Mailing] = await crud.read_mailings(get_session_factory())
        kb = Keyboard(inline=True)
        for link in links:
            kb.add(OpenLink(link.url, link.title), color=KeyboardButtonColor.POSITIVE).row()
        text = random.choice(mailings).text
        await message.answer(text, keyboard=kb.get_json())
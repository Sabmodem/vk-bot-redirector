from fastapi import FastAPI, Request, Response, BackgroundTasks
import json
import uvicorn
import logging
from vkbottle import Bot
from typing import Dict
import config
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class BotManager:
    """
    Manages multiple VK bots with their webhook configurations
    """
    def __init__(self):
        self.bots: Dict[str, Bot] = {}
        self.confirmation_codes: Dict[str, str] = {}
        self.secret_keys: Dict[str, str] = {}

    def add_bot(self, name: str, bot_instance: Bot):
        """Register a new bot instance"""
        self.bots[name] = bot_instance

    async def setup_webhooks(self):
        """Setup webhooks for all registered bots"""
        for name, bot in self.bots.items():
            try:
                code, key = await bot.setup_webhook()
                self.confirmation_codes[name] = code
                self.secret_keys[name] = key
                logger.info(f"Webhook setup for {name}: confirmation_code={code}")
            except Exception as e:
                logger.error(f"Error setting up webhook for {name}: {e}", exc_info=True)
                raise

class WebhookServer:
    """
    FastAPI server to handle multiple VK bots webhooks
    """
    def __init__(self, bot_manager: BotManager):
        self.app = FastAPI()
        self.bot_manager = bot_manager
        self._setup_routes()

    def _setup_routes(self):
        """Configure FastAPI routes for each bot"""
        self.app.on_event("startup")(self.startup_event)
        
        # Add route for each bot
        for bot_name in self.bot_manager.bots.keys():
            path = f"{config.WEBHOOK_PATH}{bot_name}"
            self.app.post(path)(self.create_webhook_handler(bot_name))

    def create_webhook_handler(self, bot_name: str):
        """Create a webhook handler for a specific bot"""
        async def handler(req: Request, background_task: BackgroundTasks):
            try:
                data = await req.json()
                logger.debug(f"Received VK event for {bot_name}: {data}")
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON in request for {bot_name}")
                return Response("Bad Request", status_code=400)
            except Exception as e:
                logger.warning(f"Error reading request for {bot_name}: {e}")
                return Response("Internal Server Error", status_code=500)

            if data.get("type") == "confirmation":
                logger.info(f"Sending confirmation token for {bot_name}")
                return Response(self.bot_manager.confirmation_codes.get(bot_name, ""))

            if data.get("secret") == self.bot_manager.secret_keys.get(bot_name):
                background_task.add_task(self.bot_manager.bots[bot_name].process_event, data)
            else:
                logger.warning(f"Invalid secret key for {bot_name}")
                return Response("Forbidden", status_code=403)

            return Response("ok")
        
        return handler

    async def startup_event(self):
        """Setup webhooks on application startup"""
        logger.info("Setting up webhooks for all bots...")
        await self.bot_manager.setup_webhooks()

def main():
    bot_manager = BotManager()
    from .bot import create_bot
    for bot_name, bot_config in config.BOTS_SETTINGS['bots'].items():
        bot_token = bot_config['token']
        bot_id = bot_config['id']
        bot_instance = create_bot(
            token=bot_token,
            webhook_url=f'{config.WEBHOOK_URL}{config.WEBHOOK_PATH}{bot_id}', 
            webhook_title=bot_id
        )
        bot_manager.add_bot(bot_name, bot_instance)
        
    from mailing import mailing_task
    asyncio.create_task(mailing_task(bot_manager.bots.values()))

    webhook_server = WebhookServer(bot_manager=bot_manager)
    uvicorn.run(
        webhook_server.app,
        host='0.0.0.0',
        port=8000
    )
            
if __name__ == "main":
    main()
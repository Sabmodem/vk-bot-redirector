# VK Bot Redirector

A multi-bot VK messenger application with webhook support and scheduled mailings.

## Setup

1. **Environment variables**:
   ```bash
   export DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/dbname"
   export WEBHOOK_URL="https://your-domain.com"
   export WEBHOOK_PATH="/webhook"
   export CONFIG_PATH="/app/bots.yaml"
   ```

2. **Create bots config** (`bots.yaml`):
   ```yaml
   bots:
     bot1:
       token: "your_token"
       id: "bot1"
     bot2:
       token: "your_token"
       id: "bot2"
   ```

3. **Database migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Run the app**:
   ```bash
   python app_multiple.py
   ```

## Docker

```bash
docker build -t vk-bot-redirector .
docker run -e DATABASE_URL="..." -e WEBHOOK_URL="..." -e CONFIG_PATH="/app/bots.yaml" vk-bot-redirector
```

## Components

- **`app_multiple.py`**: FastAPI server with multi-bot webhook handling
- **`bot.py`**: VK bot handler with message routing
- **`mailing.py`**: Background task for scheduled broadcasts
- **`models.py`**: User, Link, Mailing database models
- **`crud.py`**: Async database operations

## Webhooks

Webhooks are automatically configured on startup. Each bot gets a unique endpoint at `{WEBHOOK_URL}{WEBHOOK_PATH}{bot_id}`.

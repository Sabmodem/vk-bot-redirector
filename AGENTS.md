# Agents Instructions

## Running the App

- **Start the application**: `python app_multiple.py` or `python -c "from app_multiple import main; main()"`
- **Docker**: Build and run with the provided Dockerfile. Migrations run automatically on startup.

## Database Migrations

- **Run migrations**: `alembic upgrade head`
- **Create new migration**: `alembic revision --autogenerate -m "description"`

## Environment Setup

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string (asyncpg dialect)
- `CONFIG_PATH` - Path to bots YAML config (default: `/app/bots.yaml`)
- `WEBHOOK_URL` - Base URL for VK webhooks
- `WEBHOOK_PATH` - Path prefix for webhook endpoints
- `MAILING_INTERVAL` - Seconds between mailings (default: 43200)

## Architecture

- **Entrypoint**: `app_multiple.py` - Main async application using FastAPI + uvicorn
- **Bot handler**: `bot.py` - VK bot with webhook support via `create_bot()`
- **Models**: `models.py` - SQLAlchemy async models (User, Link, Mailing)
- **CRUD**: `crud.py` - Async database operations
- **Mailing**: `mailing.py` - Background task for scheduled mailings

## Key Conventions

- Bots configured via YAML file loaded by `config.py`
- Multiple bots supported through `BotManager` in `app_multiple.py`
- Webhook confirmation handled automatically on startup
- `main()` is the sync entry point; `main_async()` is the async entry point

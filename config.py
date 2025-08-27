import os
DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", False)
BOT_CONFIG_PATH = os.getenv("CONFIG_PATH", '/app/bots.yaml')
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
MAILING_INTERVAL = int(os.getenv("MAILING_INTERVAL", 43200))

import yaml
def read_file(filename: str) -> str:
    with open(filename, 'r') as infile:
        return infile.read()

def read_config():
    file = read_file(BOT_CONFIG_PATH)
    return yaml.safe_load(file)

BOTS_SETTINGS = read_config()
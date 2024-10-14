#devggn


import asyncio
import logging
from pyromod import listen
from pyrogram import Client, utils as pyroutils
from config import API_ID, API_HASH, BOT_TOKEN
from telethon.sync import TelegramClient

loop = asyncio.get_event_loop()

pyroutils.MIN_CHAT_ID = -999999999999
pyroutils.MIN_CHANNEL_ID = -100999999999999

logging.basicConfig(
    level=logging.ERROR,  # Global level for root logger
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # You control

sex = TelegramClient('test', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

app = Client(
    ":RestrictBot:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    sleep_threshold=20,
)



async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await app.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


loop.run_until_complete(restrict_bot())



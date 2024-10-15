import sys
import asyncio
import logging
from pyromod import listen
from pyrogram import Client utils as pyroutils
from config import API_ID, API_HASH, BOT_TOKEN, DEFAULT_SESSION
from telethon.sync import TelegramClient
import logging
import asyncio

stream_links = {}

pyroutils.MIN_CHAT_ID = -999999999999
pyroutils.MIN_CHANNEL_ID = -100999999999999


logging.basicConfig(
    level=logging.ERROR, 
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 


loop = asyncio.get_event_loop()

sex = TelegramClient('sexrepo', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
gnbot = Client('babysss', api_id=API_ID, api_hash=API_HASH, session_string=DEFAULT_SESSION)
try:
    gnbot.start()
except Exception as e:
    print("Default is not working re create or try again")
    sys.exit(1)

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



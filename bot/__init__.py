import sys
import asyncio
import logging
from pyromod import listen
from pyrogram import Client, utils as pyroutils
from config import API_ID, API_HASH, BOT_TOKEN, DEFAULT_SESSION
from telethon.sync import TelegramClient

pyroutils.MIN_CHAT_ID = -999999999999
pyroutils.MIN_CHANNEL_ID = -100999999999999


logging.basicConfig(
    level=logging.ERROR, 
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 

global_lock = asyncio.Lock()
user_locks = {}
loop = asyncio.get_event_loop()

teleBot = TelegramClient('telebotrepo', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
user_bot = Client('UserBot', api_id=API_ID, api_hash=API_HASH, session_string=DEFAULT_SESSION, no_updates=True)
try:
    user_bot.start()
except Exception as e:
    print("Default is not working re create or try again")
    sys.exit(1)

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    sleep_threshold=20,
)

async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await bot.start()
    getme = await bot.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


loop.run_until_complete(restrict_bot())



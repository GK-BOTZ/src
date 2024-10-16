from pyrogram import filters, Client
from bot.core import script
from bot.core.func import handle_force_sub, srm
from config import OWNER_ID, CHANNEL_LINK, OWNER
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot import user_locks, global_lock


@bot.on_message(filters.command("start"))
async def start(c, m):
    uid = m.from_user.id
   async with global_lock:
      if uid not in user_locks:
         user_locks[uid] = asyncio.Lock()
            
   async with user_locks[uid]:
      if Config.FSUB_CHANNELS:
         text, buttons = await handle_force_sub(c, m)
         if buttons:
            return await srm(c, m, text, markup=buttons, dt=100, photo="https://envs.sh/s/8w3GxIy7MKqojoEKWLu1IQ/SI1.jpg") 
         await srm(c, m, photo="https://envs.sh/s/8w3GxIy7MKqojoEKWLu1IQ/SI1.jpg", text=script.START_TXT.format(m.from_user.mention), markup=buttons)

import time
import asyncio
from pyrogram import filters, Client
from bot import bot, user_bot
from config import API_ID, API_HASH
from bot.core.get_func import get_msg
from bot.core.func import *
from bot.core.mongo import db
from pyrogram.errors import FloodWait
import config 

@bot.on_message(filters.regex(r'https?://[^\s]+'))
async def single_link(client, message):
    user_id = message.chat.id
    link = get_link(message.text) 
    
    try:
        if config.FSUB_CHANNELS:
           text, buttons = await handle_force_sub(client, message)
           if buttons:
              return await srm(client, message, text, markup=buttons, dt=100, photo=config.START_PIC) 
            
        msg = await srm(client, message, "Processing...", dt=0)
        data = await db.get_data(user_id)
        
        if data and data.get("session"):
            session = data.get("session")
            try:
                userbot = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=session)
                await userbot.start()                
            except:
                return await msg.edit_text("Login expired /login again...")
        else:
            userbot = user_bot
        try:
            if 't.me/+' in link:
                q = await userbot_join(userbot, link)
                await msg.edit_text(q)
                return
                                        
            elif 't.me/' in link:
                await get_msg(userbot, user_id, msg.id, link, 0, message)
        except Exception as e:
            await msg.edit_text(f"Link: `{link}`\n\n**Error:** {str(e)}")
                    
    except FloodWait as fw:
        await msg.edit_text(f'Try again after {fw.x} seconds due to floodwait from telegram.')
    except Exception as e:
        await msg.edit_text(f"Link: `{link}`\n\n**Error:** {str(e)}")


users_loop = {}

@bot.on_message(filters.command("batch"))
async def batch_link(_, message):
    user_id = message.chat.id    
    lol = await chk_user(message, user_id)
    if lol == 1:
        return    
        
    start = await bot.ask(message.chat.id, text="Please send the start link.")
    start_id = start.text
    s = start_id.split("/")[-1]
    cs = int(s)
    
    last = await bot.ask(message.chat.id, text="Please send the end link.")
    last_id = last.text
    l = last_id.split("/")[-1]
    cl = int(l)

    # if cl - cs > 10:
        # await bot.send_message(message.chat.id, "Only 10 messages allowed in batch size... Purchase premium to fly 💸")
        # return
    
    try:     
        data = await db.get_data(user_id)
        
        if data and data.get("session"):
            session = data.get("session")
            try:
                userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session)
                await userbot.start()                
            except:
                return await bot.send_message(message.chat.id, "Your login expired ... /login again")
        else:
            userbot = user_bot

        try:
            users_loop[user_id] = True
            
            for i in range(int(s), int(l)):
                if user_id in users_loop and users_loop[user_id]:
                    msg = await bot.send_message(message.chat.id, "Processing!")
                    try:
                        x = start_id.split('/')
                        y = x[:-1]
                        result = '/'.join(y)
                        url = f"{result}/{i}"
                        link = get_link(url)
                        await get_msg(userbot, user_id, msg.id, link, 0, message)
                        sleep_msg = await bot.send_message(message.chat.id, "Sleeping for 10 seconds to avoid flood...")
                        await asyncio.sleep(8)
                        await sleep_msg.delete()
                        await asyncio.sleep(2)                                                
                    except Exception as e:
                        print(f"Error processing link {url}: {e}")
                        continue
                else:
                    break
        except Exception as e:
            await bot.send_message(message.chat.id, f"Error: {str(e)}")
                    
    except FloodWait as fw:
        await bot.send_message(message.chat.id, f'Try again after {fw.x} seconds due to floodwait from Telegram.')
    except Exception as e:
        await bot.send_message(message.chat.id, f"Error: {str(e)}")


@bot.on_message(filters.command("cancel"))
async def stop_batch(_, message):
    user_id = message.chat.id
    if user_id in users_loop:
        users_loop[user_id] = False
        await bot.send_message(message.chat.id, "Batch processing stopped.")
    else:
        await bot.send_message(message.chat.id, "No active batch processing to stop.")


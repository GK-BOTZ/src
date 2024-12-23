import math
import time , re
from pyrogram import enums
from config import CHANNEL_ID, OWNER_ID 
import config
from bot.core import script
from bot.core.mongo.plans_db import premium_users
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import cv2
from pyrogram.errors import FloodWait, InviteHashInvalid, InviteHashExpired, UserAlreadyParticipant, UserNotParticipant
from datetime import datetime as dt
import asyncio, subprocess, re, os, time
from pyrogram.errors import UserNotParticipant
from bot import logger
import config

async def srm(c, m, text, photo=None, video=None, markup=None, reply_id=None, dt=20, **kwargs):
 try:
   replyid = reply_id if reply_id else m.id
   mid = m.message.id if hasattr(m, 'message') else replyid
   tosend = m.message.chat.id if hasattr(m, 'message') else m.chat.id
   if photo:
      my = await c.send_photo(
          chat_id=tosend,
          photo=photo,
          caption=text,
          reply_to_message_id=mid,
          reply_markup=markup,
          **kwargs
      )
   elif video:
       pass
       
   else:
       my = await c.send_message(
          chat_id=tosend,
          text=text,
          reply_to_message_id=mid,
          reply_markup=markup,
          **kwargs
      )
   if dt:
      await delete_msg([my, m], dt=dt)
   return my
 except:
   logger.error('srm', exc_info=True)

async def delete_msg(msg_list: list, dt=10):
   async def _delete_messages():
      await asyncio.sleep(dt)
      for msg in msg_list:
         try:
            await msg.delete()
            #logger.info("Message Deleted Succefully...")
         except Exception as e:
             pass 
   asyncio.create_task(_delete_messages())
     
invite_links = {}
async def handle_force_sub(client, message):
    try:
        if not hasattr(message, 'from_user'):
           return None, None
        uid = message.from_user.id
        buttons = []
        text = "**🔒 Join The Channels Below To Use Me 🔒**\n"
        if uid in config.PREMIUM_USER:
           return text, None
        for channel in config.FSUB_CHANNELS:
            chat = await client.get_chat(channel)
            try:
                await client.get_chat_member(chat_id=channel, user_id=uid)
            except UserNotParticipant:
                if channel not in invite_links:
                   invite_link = await client.export_chat_invite_link(chat_id=channel)
                   invite_links[channel] = invite_link  # Store the link in the dictionary
                else:
                   invite_link = invite_links[channel]  # Retrieve the existing link
                buttons.append([InlineKeyboardButton(f"Join {chat.title}", url=invite_link)])

        if buttons:
            buttons.append([InlineKeyboardButton('🔄 Rᴇғʀᴇsʜ 🔄', callback_data='genrl_fsub')])
        return text, InlineKeyboardMarkup(buttons) if buttons else None

    except Exception as e:
        logger.error('fsub', exc_info=True)
        return await message.reply(f"Got An Error - {str(e)}")

async def chk_user(message, user_id):
    user = await premium_users()
    if user_id in user or user_id in OWNER_ID:
        return 0
  ##  else:
      #  await message.reply_text("Purchase premium to do the tasks...")
       # return 1


async def gen_link(bot,chat_id):
   link = await bot.export_chat_invite_link(chat_id)
   return link

async def subscribe(bot, message):
   update_channel = CHANNEL_ID
   url = await gen_link(bot, update_channel)
   if update_channel:
      try:
         user = await bot.get_chat_member(update_channel, message.from_user.id)
         if user.status == "kicked":
            await message.reply_text("You are Banned. Contact -- @gk")
            return 1
      except UserNotParticipant:
         await message.reply_photo(photo="https://graph.org/file/d44f024a08ded19452152.jpg",caption=script.FORCE_MSG.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now...", url=f"{url}")]]))
         return 1
      except Exception:
         await message.reply_text("Something Went Wrong. Contact us @gk...")
         return 1



async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        unit = ""

        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1

        unit = ts[index:].lstrip()

        if value:
            value = int(value)

        return value, unit

    value, unit = extract_value_and_unit(time_string)

    if unit == 's':
        return value
    elif unit == 'min':
        return value * 60
    elif unit == 'hour':
        return value * 3600
    elif unit == 'day':
        return value * 86400
    elif unit == 'month':
        return value * 86400 * 30
    elif unit == 'year':
        return value * 86400 * 365
    else:
        return 0

PROGRESS_BAR = """\n
**• Total 🗃 :** `{1}`
**• Done ✅ :** `{0}`
**• Speed 📊 :** `{2}/s`
**• ETA 🔃 : ** `{3}`"""
                   

async def progress_bar(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % float(config.EDIT_SLEEP_TIME_OUT)) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "\n<code>[{0}{1}] {2}%</code>\n".format(
            ''.join([config.FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 5))]),
            ''.join([config.UN_FINISHED_PROGRESS_STR for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )
        tmp = progress + PROGRESS_BAR.format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="{}\n\n{}".format(ud_type, tmp),
            )             
                
        except:
            pass

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2] 



def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)




async def userbot_join(userbot, invite_link):
    try:
        await userbot.join_chat(invite_link)
        return "Successfully joined the Channel"
    except UserAlreadyParticipant:
        return "User is already a participant."
    except (InviteHashInvalid, InviteHashExpired):
        return "Could not join. Maybe your link is expired or Invalid."
    except FloodWait:
        return "Too many requests, try again later."
    except Exception as e:
        print(e)
        return "Could not join, try joining manually."
    


def get_link(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)   
    try:
        link = [x[0] for x in url][0]
        if link:
            return link
        else:
            return False
    except Exception:
        return False


def video_metadata(file):
    default_values = {'width': 1, 'height': 1, 'duration': 1}
    try:
        vcap = cv2.VideoCapture(file)
        if not vcap.isOpened():
            return default_values  # Return defaults if video cannot be opened

        width = round(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = round(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = vcap.get(cv2.CAP_PROP_FPS)
        frame_count = vcap.get(cv2.CAP_PROP_FRAME_COUNT)

        if fps <= 0:
            return default_values  # Return defaults if FPS value is zero or negative

        duration = round(frame_count / fps)
        if duration <= 0:
            return default_values  # Return defaults if duration is zero or negative

        vcap.release()
        return {'width': width, 'height': height, 'duration': duration}

    except Exception as e:
        print(f"Error in video_metadata: {e}")
        return default_values
    
def hhmmss(seconds):
    return time.strftime('%H:%M:%S',time.gmtime(seconds))

async def screenshot(video, duration, sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    time_stamp = hhmmss(int(duration)/2)
    out = dt.now().isoformat("_", "seconds") + ".jpg"
    cmd = ["ffmpeg",
           "-ss",
           f"{time_stamp}", 
           "-i",
           f"{video}",
           "-frames:v",
           "1", 
           f"{out}",
           "-y"
          ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    x = stderr.decode().strip()
    y = stdout.decode().strip()
    if os.path.isfile(out):
        return out
    else:
        None  

from pyrogram import filters, Client
from bot import bot, logger
import random
import os
import string
from bot.core.mongo import db
from bot.core.func import subscribe, chk_user
from config import API_ID as api_id, API_HASH as api_hash
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    FloodWait
)
from pyromod.exceptions import ListenerTimeout

def generate_random_name(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))  # Editted ... 

async def delete_session_files(user_id):
    session_file = f"session_{user_id}.session"
    memory_file = f"session_{user_id}.session-journal"

    session_file_exists = os.path.exists(session_file)
    memory_file_exists = os.path.exists(memory_file)

    if session_file_exists:
        os.remove(session_file)
    
    if memory_file_exists:
        os.remove(memory_file)

    # Delete session from the database
    if session_file_exists or memory_file_exists:
        await db.delete_session(user_id)
        return True  # Files were deleted
    return False  # No files found

@bot.on_message(filters.command("logout"))
async def clear_db(client, message):
    user_id = message.chat.id
    files_deleted = await delete_session_files(user_id)

    if files_deleted:
        await message.reply("✅ Your session data and files have been cleared from memory and disk.")
    else:
        await message.reply("⚠️ You are not logged in, no session data found.")
        
    
@bot.on_message(filters.command("login"))
async def generate_session(c, m):
 tout_msg = "**||Pʀᴏᴄᴇss Hᴀs Bᴇᴇɴ Cᴀɴᴄᴇʟʟᴇᴅ ❌, Bᴇᴄᴀᴜsᴇ Tɪᴍᴇ ⌛ Hᴀs Rᴀɴ Oᴜᴛ 🏃, \n\nBᴛᴡ Yᴏᴜ Cᴀɴ /login Aɢᴀɪɴ||**"
 try:
    uid = m.from_user.id
    cid = m.chat.id
    try:
        msg = await c.send_message(chat_id=cid, text="**» Sᴇɴᴅ Yᴏᴜʀ ||Pʜᴏɴᴇ Nᴜᴍʙᴇʀ|| Wɪᴛʜ Cᴏᴜɴᴛʀʏ Cᴏᴅᴇ, Tᴏ Lᴏɢɪɴ Vɪᴀ Usᴇʀ Bᴏᴛ. \nExᴀᴍᴩʟᴇ : ||+918713820405|| \n\n/cancel - Tᴏ Cᴀɴᴄᴇʟ Lᴏɢɪɴ Pʀᴏᴄᴇss**",  reply_to_message_id=m.id)
        ask_number = await c.listen(chat_id=cid, user_id=uid, filters=filters.text, timeout=300)
        if await cancelled(msg, ask_number):
           return
    except ListenerTimeout:
        await msg.edit(tout_msg)
        return
    phone_number = ask_number.text
    await ask_number.delete()
    try:
        await msg.edit(f"**» Sᴇɴᴅɪɴɢ OTP Tᴏ -> ||{phone_number}||**")
        client = Client(f"session_{uid}", api_id, api_hash)
        await client.connect()
        code = await client.send_code(phone_number)
    except PhoneNumberInvalid:
        await msg.edit(f"**» Tʜᴇ Pʜᴏɴᴇ Nᴜᴍʙᴇʀ ||{phone_number}||, Dᴏᴇs Noᴛ Bᴇʟᴏɴɢ Tᴏ Aɴʏ Tᴇʟᴇɢʀᴀᴍ Aᴄᴄᴏᴜɴᴛ.\n\nCʜᴇᴄᴋ Yᴏᴜʀ Nᴜᴍʙᴇʀ Aɴᴅ /login Aɢᴀɪɴ...**")
        return
    try:
        await msg.edit("**» Eɴᴛᴇʀ Tʜᴇ OTP Yᴏᴜʀ Rᴇᴄᴇɪᴠᴇᴅ Fʀᴏᴍ [Tᴇʟᴇɢʀᴀᴍ](ᴛ.ᴍᴇ/+𝟺𝟸𝟽𝟽𝟽).\n\nFᴏʀᴍᴀᴛ:- Iғ OTP Is 𝟷𝟸𝟹𝟺𝟻, Eɴᴛᴇʀ As 𝟷 𝟸 𝟹 𝟺 𝟻 (Wɪᴛʜ Oɴᴇ Wʜɪᴛᴇ ' ' Sᴘᴀᴄᴇ)\n\n/cancel - Tᴏ Cᴀɴᴄᴇʟ Lᴏɢɪɴ Pʀᴏᴄᴇss**")
        ask_otp = await c.listen(chat_id=cid, user_id=uid, filters=filters.text, timeout=300)
        if await cancelled(msg, ask_otp):
           return
    except TimeoutError:
        await msg.edit(tout_msg)
        return
    phone_code = ask_otp.text.replace(" ", "")
    await ask_otp.delete()
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await msg.edit("**» Yᴏᴜ Sᴇɴᴛ ||Wʀᴏɴɢ OTP||. \n\nTʀʏ /login Aɢᴀɪɴ**")
        return
    except PhoneCodeExpired:
        await msg.edit("**» Yᴏᴜʀ Aʀᴇ Lᴀᴛᴇ, ||OTP Exᴘɪʀᴇᴅ||.\n\nTʀʏ /login Aɢᴀɪɴ**")
        return
    except SessionPasswordNeeded:
        try:
            await msg.edit("**» Tᴡᴏ Sᴛᴇᴘ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Eɴᴀʙʟᴇᴅ Iɴ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ, Eɴᴛᴇʀ Yᴏᴜʀ ||𝟸FA Pᴀssᴡᴏʀᴅ 🔑|| To Cᴏɴᴛɪɴᴜᴇ...**")
            ask_2fa = await c.listen(chat_id=cid, user_id=uid, filters=filters.text, timeout=300)
        except ListenerTimeout:
            await msg.edit(tout_msg)
            return
        try:
            password = ask_2fa.text
            await client.check_password(password=password)
            if await cancelled(msg, ask_2fa):
               return
        except PasswordHashInvalid:
            await msg.edit("**» Wʀᴏɴɢ ||𝟸FA Pᴀssᴡᴏʀᴅ 🔑.||\n\nCʜᴇᴄᴋ Yᴏᴜʀ Pᴀssᴡᴏʀᴅ Aɴᴅ /login Aɢᴀɪɴ...** ")
            return
    await client.sign_in_bot(phone_number)
    string_session = await client.export_session_string()
    await db.set_session(uid, string_session)
    await client.disconnect()
    await m.reply("Sᴜᴄᴄᴇғᴜʟʟʏ Lᴏɢɢᴇᴅ Iɴ ✅...")
    text = f"**Tʜɪs Is Yᴏᴜʀ Pʏʀᴏɢʀᴀᴍ Sᴇssɪᴏɴ Sᴛʀɪɴɢ** \n\n||{string_session}|| \n\n**ɴᴏᴛᴇ ⚠️:** ᴅᴏɴ'ᴛ sʜᴀʀᴇ ᴛʜɪs ᴡɪᴛʜ ᴀɴʏᴏɴᴇ** "
    await c.send_message(msg.from_user.id, text)
 except:
    logger.error('login', exc_info=True)
    
async def cancelled(msg, m):
    cnc_msg = "**Sᴜᴄᴄᴇғᴜʟʟʏ Cᴀɴᴄᴇʟʟᴇᴅ Tʜᴇ Lᴏɢɪɴ Pʀᴏᴄᴇss. \n\nBᴛᴡ Yᴏᴜ Cᴀɴ /login Aɢᴀɪɴ...**"
    if "/cancel" in m.text:
        await msg.edit(cnc_msg)
        await m.delete()
        return True
    elif m.text.startswith("/"):  # Bot Commands
        await msg.edit(cnc_msg)
        await m.delete()
        return True
    else:
        return False

# devggn
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", 20747302))
API_HASH = getenv("API_HASH", "6e086ad99a197709af10425d7c7c1b65")
BOT_TOKEN = getenv("BOT_TOKEN", "7944884364:AAF23zcZ2EokJeSkVL_roMNN9duJqVCLryk")
OWNER_ID = list(map(int, getenv("OWNER_ID", "6805001741").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://gautamkumar83226:NHKzaiNLlzzedv69@cluster0.mbaodme.mongodb.net/?retryWrites=true&w=majority")
LOG_GROUP = getenv("LOG_GROUP", "-1002156222847")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002156222847"))

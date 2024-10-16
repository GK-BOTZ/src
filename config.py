
from os import getenv


API_ID = int(getenv("API_ID", 20747302))
API_HASH = getenv("API_HASH", "6e086ad99a197709af10425d7c7c1b65")
BOT_TOKEN = getenv("BOT_TOKEN", "6935328388:AAFIdCx2548DBKZphKO4ou9r8m48wUSJvRc")
OWNER_ID = list(map(int, getenv("OWNER_ID", "6805001741").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://gautamkumar83226:NHKzaiNLlzzedv69@cluster0.mbaodme.mongodb.net/?retryWrites=true&w=majority")
LOG_GROUP = getenv("LOG_GROUP", "-1002156222847")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002254851900"))
DEFAULT_SESSION = getenv("DEFAULT_SESSION", "BAGh3EsAa6X2HupHVV3M15U_MvjUeIfi50O2wuMnIkb6xyzbcdl7Hqwq4ZMWJox-5YMArmBa09BHu9suWpW0BNkcTDoC8V_1PegQlfazTMHaSYuqt3QwxcMDLiV6yPgzXmYXkGMjalhn_MAw1srNfXCd1LeVKKvKIHhlGxHXkmVSkTEf35_qdW9ulTwsxkHwjUReELdWRk61yT56M4wVtCMKCScEJEpdVNwI14kKEQouSsBBJjfCFeRHWbIA7bwkfdOLtdbQA12qOudaYal4WClGfI0CHeOCVfQxWdIURPMUzfw8iZUObbNVqlH4yYpX08y4-yMz6H3wcCYzTTrOIaMSFBO6dwAAAAGXX92zAA")
CHANNEL_LINK = getenv('CHANNEL_LINK', 'GKBotz')
OWNER = getenv('OWNER', 'Talk2Smile_Bot')
PREMIUM_USER = getenv('PREMIUM_USER', [5811080171, 6177970139])
FSUB_CHANNELS = getenv('FSUB_CHANNEL', [-1002254851900])
START_PIC = getenv('START_PIC', 'https://envs.sh/s/SDNpX44mayxsxJSNKNdyBw/S71.png')
  

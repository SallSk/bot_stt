import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TG_TOKEN')

FOLDER_ID = os.getenv('FOLDERID')
IAMTOKEN = ()

MAX_VOICE_DURATION = 30
MAX_USER_STT_BLOCKS = 12
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SAVEIG_API = "https://api.saveig.app/api/instagram"
INSTAGRAM_SESSION_USERNAME = os.getenv("INSTAGRAM_SESSION_USERNAME")
INSTAGRAM_SESSION_FILE = os.getenv("INSTAGRAM_SESSION_FILE")
BOT_LINK = os.getenv("BOT_LINK")
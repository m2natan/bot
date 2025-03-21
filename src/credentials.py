import os
from dotenv import load_dotenv

load_dotenv()

# Check if the .env file exists in the parent directory
env_path = ".env"

if os.path.exists(env_path):
    load_dotenv(env_path)  # Explicitly load from parent directory

# Fetch environment variables
_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")

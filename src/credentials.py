import os
from dotenv import load_dotenv
from pathlib import Path

# Construct the path to the parent directory
parent_dir = Path(__file__).resolve().parent.parent  # Go up two levels to the parent directory
env_path = parent_dir / ".env"  # Path to the .env file in the parent directory

# Check if the .env file exists in the parent directory
if env_path.exists():
    load_dotenv(env_path)  # Load environment variables from the .env file in the parent directory
else:
    print(f".env file not found at {env_path}")

# Fetch environment variables
_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")

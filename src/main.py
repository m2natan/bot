from flask import Flask
import threading
from telegram.ext import Application
from credentials import _TOKEN

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)  # Dummy server on port 10000

def main():
    thread = threading.Thread(target=run_flask)  # Run Flask in a separate thread
    thread.start()

if __name__ == '__main__':
    main()

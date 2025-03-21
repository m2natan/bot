import asyncio
from fastapi import FastAPI
from threading import Thread
from telegram.ext import Application
from src.app import main
# FastAPI app
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Run the FastAPI app in a separate thread
def run_fastapi():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Telegram bot function
async def run_bot():
    main()
if __name__ == "__main__":
    # Start FastAPI in a separate thread
    fastapi_thread = Thread(target=run_fastapi)
    fastapi_thread.start()

    # Run the bot in the main thread
    asyncio.run(run_bot())

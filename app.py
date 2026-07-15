from flask import Flask
from threading import Thread
import os
import asyncio
from panel import main as bot_main

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    print("🚀 Starting Bot...")
    Thread(target=run_flask, daemon=True).start()
    asyncio.run(bot_main())

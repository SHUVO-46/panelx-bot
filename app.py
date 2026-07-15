from flask import Flask
from threading import Thread
import os
import asyncio
import sys
import logging
import time

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# আপনার মূল বট ইম্পোর্ট - panelx.py থেকে
try:
    from panelx import main as bot_main
    logger.info("✅ Successfully imported bot_main from panelx")
except ImportError as e:
    logger.error(f"❌ Failed to import panelx: {e}")
    sys.exit(1)

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Panel X Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    """Render-এর জন্য Flask সার্ভার"""
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_bot_with_retry():
    """বট চালান এবং Error হলে রিট্রাই করুন"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"🚀 Starting Telegram Bot (Attempt {attempt + 1})...")
            asyncio.run(bot_main())
            break  # সফল হলে লুপ থেকে বেরিয়ে আসুন
        except Exception as e:
            logger.error(f"❌ Bot attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # ৫ সেকেন্ড পর আবার চেষ্টা
            else:
                logger.error("❌ All attempts failed. Exiting...")
                sys.exit(1)

if __name__ == '__main__':
    logger.info("🚀 Starting Panel X Bot Service...")
    
    # Flask আলাদা থ্রেডে চালান
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("✅ Flask server started on port 10000")
    
    # বট চালান (মেইন থ্রেডে)
    run_bot_with_retry()

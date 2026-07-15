from flask import Flask
from threading import Thread
import os
import asyncio
import sys
import logging
import time
import traceback

# লগিং সেটআপ - বিস্তারিত লগের জন্য
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Panel X Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/debug')
def debug():
    """ডিবাগ করার জন্য - Environment Variables চেক"""
    return {
        "BOT_TOKEN": "✅ Set" if os.environ.get("BOT_TOKEN") else "❌ Missing",
        "API_KEY": "✅ Set" if os.environ.get("API_KEY") else "❌ Missing", 
        "BASE_URL": os.environ.get("BASE_URL", "Not Set")
    }

def run_flask():
    """Render-এর জন্য Flask সার্ভার"""
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_bot_with_error_logging():
    """বট চালান এবং প্রতিটি Error ডিটেইলস সহ লগ করুন"""
    try:
        logger.info("=" * 50)
        logger.info("🚀 ATTEMPTING TO START TELEGRAM BOT")
        logger.info("=" * 50)
        
        # Environment Variables চেক
        logger.info(f"🔍 BOT_TOKEN: {'✅ Set' if os.environ.get('BOT_TOKEN') else '❌ Missing'}")
        logger.info(f"🔍 API_KEY: {'✅ Set' if os.environ.get('API_KEY') else '❌ Missing'}")
        logger.info(f"🔍 BASE_URL: {os.environ.get('BASE_URL', 'Not Set')}")
        
        # panelx থেকে main ইম্পোর্ট
        logger.info("📦 Importing bot_main from panelx...")
        from panelx import main as bot_main
        logger.info("✅ Successfully imported bot_main")
        
        # বট স্টার্ট করার আগে
        logger.info("🔥🔥🔥 CALLING bot_main() NOW 🔥🔥🔥")
        
        # main() কল করুন
        bot_main()
        
        logger.info("✅ Bot main() completed (this may not show if it's running)")
        
    except ImportError as e:
        logger.error(f"❌ Import Error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Bot crashed with error: {e}")
        logger.error("=" * 50)
        logger.error("FULL TRACEBACK:")
        logger.error(traceback.format_exc())
        logger.error("=" * 50)
        sys.exit(1)

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("🚀 STARTING PANEL X BOT SERVICE")
    logger.info("=" * 50)
    
    # Flask আলাদা থ্রেডে চালান
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("✅ Flask server thread started")
    
    # বট চালান (মেইন থ্রেডে)
    run_bot_with_error_logging()

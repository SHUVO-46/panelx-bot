from flask import Flask
from threading import Thread
import os
import sys
import logging
import time
import traceback

# --- ১. লগিং সেটআপ (বিস্তারিত) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- ২. Flask অ্যাপ ---
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Panel X Bot is running!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/debug')
def debug():
    """ডিবাগ করার জন্য - Environment Variables ও ইম্পোর্ট চেক"""
    import importlib
    status = {
        "ENV_VARS": {
            "BOT_TOKEN": "✅ Set" if os.environ.get("BOT_TOKEN") else "❌ Missing",
            "API_KEY": "✅ Set" if os.environ.get("API_KEY") else "❌ Missing",
            "BASE_URL": os.environ.get("BASE_URL", "Not Set"),
        },
        "IMPORT_STATUS": "Unknown"
    }
    try:
        # panelx মডিউল ইম্পোর্ট করার চেষ্টা
        panelx_module = importlib.import_module('panelx')
        status["IMPORT_STATUS"] = "✅ Success"
        status["HAS_MAIN"] = hasattr(panelx_module, 'main')
    except Exception as e:
        status["IMPORT_STATUS"] = f"❌ Failed: {e}"
    return status

# --- ৩. Flask সার্ভার চালানোর ফাংশন ---
def run_flask():
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# --- ৪. বট চালানোর ফাংশন (সবচেয়ে গুরুত্বপূর্ণ) ---
def run_bot():
    logger.info("=" * 60)
    logger.info("🚀 ATTEMPTING TO START TELEGRAM BOT")
    logger.info("=" * 60)

    # Environment Variables চেক
    logger.info(f"🔍 BOT_TOKEN: {'✅ Set' if os.environ.get('BOT_TOKEN') else '❌ Missing'}")
    logger.info(f"🔍 API_KEY: {'✅ Set' if os.environ.get('API_KEY') else '❌ Missing'}")
    logger.info(f"🔍 BASE_URL: {os.environ.get('BASE_URL', 'Not Set')}")

    try:
        # panelx মডিউল ইম্পোর্ট করার চেষ্টা
        logger.info("📦 Importing bot_main from panelx...")
        from panelx import main as bot_main
        logger.info("✅ Successfully imported bot_main")

        # main() ফাংশন কল করার ঠিক আগে লগ
        logger.info("🔥🔥🔥 CALLING bot_main() NOW 🔥🔥🔥")
        
        # --- এখানেই বট স্টার্ট হয় ---
        bot_main()
        
        # main() ফাংশন রিটার্ন করলে (যা সাধারণত হয় না)
        logger.info("⚠️ bot_main() returned unexpectedly. Bot might have stopped.")

    except ImportError as e:
        logger.error(f"❌ IMPORT ERROR: Could not import 'panelx' module.")
        logger.error(f"❌ Error Details: {e}")
        logger.error(traceback.format_exc())
    except Exception as e:
        logger.error(f"❌ BOT CRASHED with error: {e}")
        logger.error("=" * 60)
        logger.error("FULL TRACEBACK:")
        logger.error(traceback.format_exc())
        logger.error("=" * 60)

# --- ৫. মেইন ফাংশন ---
if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🚀 STARTING PANEL X BOT SERVICE (NEW VERSION)")
    logger.info("=" * 60)

    # Flask সার্ভার আলাদা থ্রেডে চালান
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("✅ Flask server thread started. Waiting 2 seconds for it to initialize...")
    time.sleep(2)  # Flask সার্ভার শুরু হতে একটু সময় দিন

    # বট চালান (মেইন থ্রেডে)
    run_bot()

    # যদি কোনো কারণে run_bot() ফাংশন থেকে রিটার্ন আসে, তাহলে এই লগ দেখাবে
    logger.warning("⚠️ run_bot() function returned. The main thread is exiting.")
    # Gunicorn-কে জানান যে থ্রেড শেষ হয়ে গেছে, কিন্তু Flask চালু থাকবে

from flask import Flask
from threading import Thread
import os
import sys
import logging
import time
import traceback

# লগিং সেটআপ
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
    import importlib
    status = {
        "ENV_VARS": {
            "BOT_TOKEN": "✅ Set" if os.environ.get("BOT_TOKEN") else "❌ Missing",
            "API_KEY": "✅ Set" if os.environ.get("API_KEY") else "❌ Missing",
            "BASE_URL": os.environ.get("BASE_URL", "Not Set"),
        }
    }
    try:
        panelx_module = importlib.import_module('panelx')
        status["IMPORT_STATUS"] = "✅ Success"
        status["HAS_START_BOT"] = hasattr(panelx_module, 'start_bot')
    except Exception as e:
        status["IMPORT_STATUS"] = f"❌ Failed: {e}"
    return status

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_bot():
    logger.info("=" * 50)
    logger.info("🚀 ATTEMPTING TO START TELEGRAM BOT")
    logger.info("=" * 50)
    
    # এই লাইন পরিবর্তন করা হয়েছে
    from panelx import start_bot as bot_main  # 👈 এখানে start_bot
    logger.info("✅ Successfully imported start_bot")
    
    logger.info("🔥 CALLING bot_main() NOW")
    bot_main()
    logger.info("⚠️ bot_main() returned unexpectedly")

if __name__ == '__main__':
    logger.info("🚀 STARTING PANEL X BOT SERVICE")
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("✅ Flask server started")
    run_bot()

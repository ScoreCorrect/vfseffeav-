"""
Main entry point for the Telegram Quiz Bot
Handles plugin loading, bot initialization, and dispatcher setup
"""

import logging
import os
import sys
from pathlib import Path
import importlib.util

from telegram.ext import Application, ContextTypes
from config import BOT_TOKEN, DEBUG, POLLING_INTERVAL
from db.mongo import MongoDB

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if DEBUG else logging.INFO
)
logger = logging.getLogger(__name__)

# Global MongoDB instance
db = MongoDB()


def load_plugins(app: Application) -> None:
    """
    Dynamically load all plugins from the plugins directory.
    Each plugin should have a 'setup' or 'register' function.
    
    Args:
        app: The Telegram Application instance
    """
    plugins_dir = Path(__file__).parent / 'plugins'
    
    if not plugins_dir.exists():
        logger.warning(f"Plugins directory not found: {plugins_dir}")
        return
    
    # Iterate through all .py files in plugins directory
    for plugin_file in plugins_dir.glob('*.py'):
        if plugin_file.name.startswith('_'):
            continue  # Skip __init__.py and other special files
        
        try:
            # Dynamically load the module
            spec = importlib.util.spec_from_file_location(
                f"plugins.{plugin_file.stem}", 
                plugin_file
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"plugins.{plugin_file.stem}"] = module
            spec.loader.exec_module(module)
            
            # Look for setup/register function in the plugin
            if hasattr(module, 'setup'):
                module.setup(app)
                logger.info(f"✓ Loaded plugin: {plugin_file.stem}")
            elif hasattr(module, 'register'):
                module.register(app)
                logger.info(f"✓ Loaded plugin: {plugin_file.stem}")
            else:
                logger.warning(f"⚠ Plugin {plugin_file.stem} has no 'setup' or 'register' function")
        
        except Exception as e:
            logger.error(f"✗ Failed to load plugin {plugin_file.stem}: {e}")


async def post_init(app: Application) -> None:
    """
    Called after the bot has been started.
    Initialize databases and perform startup tasks.
    """
    logger.info("🤖 Quiz Bot initialized successfully!")
    logger.info(f"📊 Connected to MongoDB: {db.db_name}")


def main() -> None:
    """
    Start the bot application
    """
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not found in environment variables!")
        logger.error("Please set BOT_TOKEN in your .env file")
        sys.exit(1)
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add post_init callback
    application.post_init = post_init
    
    # Load all plugins
    logger.info("📦 Loading plugins...")
    load_plugins(application)
    
    # Start the bot
    logger.info("🚀 Starting bot polling...")
    application.run_polling(
        poll_interval=POLLING_INTERVAL,
        allowed_updates=['message', 'callback_query', 'poll', 'poll_answer']
    )


if __name__ == '__main__':
    main()
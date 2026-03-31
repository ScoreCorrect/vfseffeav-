"""
Configuration file for Telegram Quiz Bot
All sensitive data should be stored in .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'quiz_bot')

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'quiz_bot_db')

# Admin/Verified Users (Telegram User IDs)
# Add verified user IDs here who can create quizzes and topics
VERIFIED_USERS = [
    int(user_id) for user_id in os.getenv('VERIFIED_USERS', '').split(',') 
    if user_id.strip()
]

# Admin user IDs
ADMIN_USERS = [
    int(user_id) for user_id in os.getenv('ADMIN_USERS', '').split(',') 
    if user_id.strip()
]

# Application Settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
POLLING_INTERVAL = int(os.getenv('POLLING_INTERVAL', '3'))

# Bot messages and constants
BOT_WELCOME_MESSAGE = """
🎯 Welcome to Quiz Master Bot! 🎯

Prepare for your competitive exams with our comprehensive quiz system.

Choose an option below to get started:
"""

BACK_BUTTON_TEXT = "⬅️ Back"
MAIN_MENU_TEXT = "📋 Main Menu"
"""
==========================================================
LEARN-AI MOBILE
Configuration File
==========================================================
"""

from pathlib import Path

# ======================================================
# APPLICATION INFORMATION
# ======================================================

APP_NAME = "LEARN-AI Mobile"

APP_VERSION = "1.0.0"

APP_ICON = "📱"

APP_DESCRIPTION = (
    "AI-Powered Inclusive ICT Learning Platform"
)

# ======================================================
# PROJECT DIRECTORIES
# ======================================================

BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"

IMAGE_DIR = ASSETS_DIR / "images"

ICON_DIR = ASSETS_DIR / "icons"

AUDIO_DIR = ASSETS_DIR / "audio"

DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_FILE = DATABASE_DIR / "learn_ai.db"

# ======================================================
# USER ROLES
# ======================================================

ROLES = [

    "Student",

    "Teacher",

    "Administrator"

]

# ======================================================
# LESSON SETTINGS
# ======================================================

TOTAL_LESSONS = 8

PASS_MARK = 50

MAX_QUIZ_QUESTIONS = 20

# ======================================================
# GAMIFICATION
# ======================================================

XP_PER_LESSON = 50

XP_PER_QUIZ = 20

DAILY_LOGIN_REWARD = 5

STREAK_REWARD = 10

# ======================================================
# BADGES
# ======================================================

BADGES = {

    "Beginner": 100,

    "Intermediate": 300,

    "Advanced": 700,

    "Expert": 1200,

    "Master": 2000

}

# ======================================================
# DASHBOARD COLOURS
# ======================================================

PRIMARY_COLOR = "#2563EB"

SECONDARY_COLOR = "#14B8A6"

SUCCESS_COLOR = "#22C55E"

WARNING_COLOR = "#F59E0B"

ERROR_COLOR = "#EF4444"

BACKGROUND_COLOR = "#F5F7FB"

SIDEBAR_COLOR = "#1F2937"

TEXT_COLOR = "#111827"

# ======================================================
# CHART COLOURS
# ======================================================

CHART_COLORS = [

    "#2563EB",

    "#22C55E",

    "#F59E0B",

    "#EF4444",

    "#9333EA"

]

# ======================================================
# ACCESSIBILITY
# ======================================================

FONT_SIZES = [

    "Small",

    "Medium",

    "Large",

    "Extra Large"

]

DEFAULT_FONT = "Medium"

HIGH_CONTRAST = False

TEXT_TO_SPEECH = True

# ======================================================
# AI SETTINGS
# ======================================================

AI_MODEL = "gpt-5.5"

MAX_AI_RESPONSE = 500

TEMPERATURE = 0.5

# ======================================================
# ACHIEVEMENTS
# ======================================================

ACHIEVEMENTS = [

    "Completed First Lesson",

    "Completed First Quiz",

    "5-Day Study Streak",

    "10-Day Study Streak",

    "Completed All Lessons",

    "Quiz Champion"

]

# ======================================================
# SETTINGS MENU
# ======================================================

SETTINGS_MENU = [

    "Profile",

    "Notifications",

    "Theme",

    "Accessibility",

    "Language",

    "Security",

    "About"

]

# ======================================================
# SUPPORTED LANGUAGES
# ======================================================

LANGUAGES = [

    "English",

    "French"

]

# Add this to your existing config.py file
import os

APP_NAME = "LEARN-AI Mobile"
APP_ICON = "📱"

# Replace 'YOUR_GEMINI_API_KEY_HERE' with your actual key from Google AI Studio
GEMINI_API_KEY = os.getenv("")


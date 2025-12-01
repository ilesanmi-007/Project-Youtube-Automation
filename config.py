import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')

# Content Settings
VIDEO_LENGTH_MIN = 45
VIDEO_LENGTH_MAX = 120
UPLOAD_FREQUENCY = 'daily'  # daily, twice_daily, weekly
BEST_UPLOAD_TIMES = ['09:00', '15:00', '19:00']

# Video Settings
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 60

# Paths
OUTPUT_DIR = 'output'
SCRIPTS_DIR = f'{OUTPUT_DIR}/scripts'
AUDIO_DIR = f'{OUTPUT_DIR}/audio'
VIDEO_DIR = f'{OUTPUT_DIR}/videos'
THUMBNAILS_DIR = f'{OUTPUT_DIR}/thumbnails'

# Database
DB_PATH = 'automation.db'

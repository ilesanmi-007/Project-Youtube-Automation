# Developer Handoff Guide

## Quick Start

Welcome! This project is a YouTube automation system that creates videos from idea to upload with minimal human input. Here's everything you need to know to continue development.

---

## 1. First Steps (15 minutes)

### Clone & Setup
```bash
cd youtube-automation
pip install -r requirements.txt
cp .env.example .env
```

### Add Your API Keys to `.env`
```bash
OPENAI_API_KEY=sk-...        # Required - Get from platform.openai.com
ELEVENLABS_API_KEY=...       # Optional - Better voice quality
PEXELS_API_KEY=...           # Optional - Stock footage
```

### Test the System
```bash
python demo.py
```

This will create a sample video and show you the entire pipeline in action.

### Launch Dashboard
```bash
python dashboard.py
```

Visit http://localhost:5000 to see the web interface.

---

## 2. Project Structure

```
youtube-automation/
│
├── config.py                 # All settings (video length, upload schedule, etc.)
├── database.py               # SQLite database setup
├── pipeline.py               # Main orchestrator - connects all modules
│
├── content_sourcer.py        # Finds trending topics
├── script_generator.py       # Creates original scripts
├── audio_generator.py        # Generates voiceovers
├── video_generator.py        # Assembles final video
├── seo_generator.py          # Creates titles/descriptions/tags
├── youtube_uploader.py       # Handles uploads (needs OAuth setup)
│
├── dashboard.py              # Flask web interface
├── dashboard_simple.py       # Simplified dashboard version
├── demo.py                   # Quick test script
├── test.py                   # Unit tests
│
├── templates/
│   └── dashboard.html        # Dashboard UI
│
├── output/                   # Generated content
│   ├── scripts/
│   ├── audio/
│   ├── videos/
│   └── thumbnails/
│
└── automation.db             # SQLite database
```

---

## 3. How the Pipeline Works

### Flow Diagram
```
Idea/Topic → Script → Audio → Video → SEO → Upload → YouTube
```

### Detailed Steps

1. **Content Sourcing** (`content_sourcer.py`)
   - Analyzes trending topics
   - Returns topic + angle for video

2. **Script Generation** (`script_generator.py`)
   - Takes topic as input
   - Uses OpenAI to write original script
   - Saves to `output/scripts/`

3. **Audio Generation** (`audio_generator.py`)
   - Converts script to speech
   - Uses ElevenLabs (premium) or OpenAI TTS (fallback)
   - Saves to `output/audio/`

4. **Video Generation** (`video_generator.py`)
   - Downloads stock footage from Pexels
   - Adds subtitles with timing
   - Combines audio + visuals
   - Saves to `output/videos/`

5. **SEO Generation** (`seo_generator.py`)
   - Creates optimized title
   - Writes description with keywords
   - Generates relevant tags

6. **Upload** (`youtube_uploader.py`)
   - Schedules video for optimal time
   - Uploads to YouTube (requires OAuth)

### Run Full Pipeline
```bash
python pipeline.py
```

---

## 4. Database Schema

The system uses SQLite to track everything:

```sql
CREATE TABLE videos (
    id INTEGER PRIMARY KEY,
    topic TEXT,
    script_path TEXT,
    audio_path TEXT,
    video_path TEXT,
    title TEXT,
    description TEXT,
    tags TEXT,
    status TEXT,              -- 'pending', 'processing', 'completed', 'uploaded'
    created_at TIMESTAMP,
    uploaded_at TIMESTAMP
);
```

Access via:
```python
from database import get_db_connection
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM videos")
```

---

## 5. Configuration (`config.py`)

Key settings you can adjust:

```python
# Video Settings
VIDEO_LENGTH = (45, 120)      # Min/max seconds
VIDEO_RESOLUTION = (1080, 1920)  # Portrait for Shorts/TikTok

# Upload Schedule
UPLOAD_FREQUENCY = "daily"    # daily, twice_daily, weekly
BEST_UPLOAD_TIMES = ["09:00", "15:00", "20:00"]

# AI Settings
OPENAI_MODEL = "gpt-4"
VOICE_ID = "..."              # ElevenLabs voice ID
```

---

## 6. Current Status

### ✅ Working
- Script generation
- Audio generation (both OpenAI TTS and ElevenLabs)
- Video assembly with subtitles
- SEO metadata generation
- Web dashboard
- Database tracking

### ⚠️ Needs Setup
- **YouTube OAuth** - Required for automated uploads
  - Follow `API_KEYS_GUIDE.md` section on YouTube API
  - Run OAuth flow once to get credentials
  - System will auto-upload after that

### 🚧 Incomplete / TODO
- Multi-channel management (currently single channel)
- Thumbnail generation (placeholder exists)
- Performance analytics integration
- Book-to-video converter
- Advanced visual generation (currently stock footage only)

---

## 7. Development Workflow

### To Add a New Feature

1. **Create module** (e.g., `thumbnail_generator.py`)
2. **Add to pipeline** (`pipeline.py`)
3. **Update database** if needed (`database.py`)
4. **Add to dashboard** (`dashboard.html`)
5. **Test** with `demo.py` or `test.py`

### Example: Adding Thumbnail Generation

```python
# thumbnail_generator.py
def generate_thumbnail(video_id, title):
    # Your logic here
    thumbnail_path = f"output/thumbnails/{video_id}.jpg"
    # Save thumbnail
    return thumbnail_path

# Add to pipeline.py
from thumbnail_generator import generate_thumbnail

def run_pipeline(topic):
    # ... existing code ...
    thumbnail_path = generate_thumbnail(video_id, title)
    # Update database
```

---

## 8. Testing

### Quick Test
```bash
python demo.py
```

### Full Pipeline Test
```bash
python test.py
```

### Manual Testing
```python
# Test script generation
from script_generator import generate_script
script = generate_script("productivity tips")
print(script)

# Test audio generation
from audio_generator import generate_audio
audio_path = generate_audio(script, "test_audio")
print(f"Audio saved: {audio_path}")
```

---

## 9. Common Issues & Solutions

### "No API key found"
- Check `.env` file exists
- Verify key format (no quotes, no spaces)
- Restart terminal after adding keys

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "FFmpeg not found" (video generation fails)
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from ffmpeg.org
```

### "Database locked"
- Close dashboard before running pipeline
- Or use separate database connections

### YouTube upload fails
- Complete OAuth setup (see `API_KEYS_GUIDE.md`)
- Check quota limits (YouTube API has daily limits)

---

## 10. Next Development Priorities

Based on the project vision, here's what to build next:

### Priority 1: YouTube OAuth Integration
- Complete `youtube_uploader.py`
- Test automated uploads
- Handle quota limits gracefully

### Priority 2: Multi-Channel Management
- Add `channels` table to database
- Update pipeline to support channel selection
- Add channel switcher to dashboard

### Priority 3: Thumbnail Generation
- Use AI to generate custom thumbnails
- A/B test different styles
- Track CTR by thumbnail type

### Priority 4: Analytics Integration
- Pull YouTube Analytics API data
- Display views, watch time, CTR in dashboard
- Auto-optimize based on performance

### Priority 5: Book-to-Video Converter
- Parse book chapters
- Generate series of videos
- Auto-schedule releases

---

## 11. Resources

### Documentation
- `README.md` - Setup and usage
- `PROJECT_VISION.md` - Big picture strategy
- `API_KEYS_GUIDE.md` - API setup instructions

### APIs Used
- OpenAI: https://platform.openai.com/docs
- ElevenLabs: https://elevenlabs.io/docs
- Pexels: https://www.pexels.com/api/documentation
- YouTube Data API: https://developers.google.com/youtube/v3

### Libraries
- `openai` - AI text and audio generation
- `moviepy` - Video editing
- `flask` - Web dashboard
- `requests` - API calls
- `sqlite3` - Database

---

## 12. Contact & Questions

If you get stuck:

1. Check existing code comments
2. Review `demo.py` for working examples
3. Test individual modules in isolation
4. Check API documentation for rate limits

The codebase is designed to be modular - each component works independently and can be tested separately.

---

## Final Notes

This project is about **automation, not perfection**. The goal is to create a system that produces good-enough content consistently, not perfect content occasionally.

Focus on:
- **Reliability** - Does it run without breaking?
- **Speed** - Can it produce videos daily?
- **Quality** - Is the output monetizable?

Everything else is optimization.

Good luck! 🚀

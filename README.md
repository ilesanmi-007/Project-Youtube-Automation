# YouTube Automation System

Fully autonomous YouTube content creation pipeline for motivational/self-development content.

## Features

✅ **Autonomous Pipeline**
- Content sourcing from trending topics
- Original script generation (AI-powered)
- Voiceover generation (ElevenLabs or OpenAI TTS)
- Video creation with stock footage and subtitles
- SEO metadata generation
- Automated scheduling and upload

✅ **Web Dashboard**
- Real-time pipeline monitoring
- Video status tracking
- Performance analytics
- Manual override controls

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Required:
- `OPENAI_API_KEY` - For content generation and TTS

Optional:
- `ELEVENLABS_API_KEY` - For better voice quality
- `PEXELS_API_KEY` - For stock footage
- YouTube API credentials - For automated uploads

### 3. Run the Dashboard

```bash
python dashboard.py
```

Visit: http://localhost:5000

### 4. Create Your First Video

Click "Create New Video" in the dashboard or run:

```bash
python pipeline.py
```

## Pipeline Stages

1. **Content Sourcing** - AI identifies trending topics
2. **Script Generation** - Creates original 45-120s script
3. **Audio Generation** - Generates voiceover
4. **Video Generation** - Combines footage, audio, subtitles
5. **Metadata Generation** - Creates SEO-optimized title/description
6. **Scheduling** - Queues for optimal upload time

## Project Structure

```
youtube-automation/
├── config.py              # Configuration
├── database.py            # SQLite database
├── pipeline.py            # Main automation pipeline
├── content_sourcer.py     # Trend analysis
├── script_generator.py    # Script creation
├── audio_generator.py     # Voiceover generation
├── video_generator.py     # Video assembly
├── seo_generator.py       # Metadata creation
├── youtube_uploader.py    # Upload scheduling
├── dashboard.py           # Web interface
└── templates/
    └── dashboard.html     # Dashboard UI

output/
├── scripts/               # Generated scripts
├── audio/                 # Voiceovers
├── videos/                # Final videos
└── thumbnails/            # Video thumbnails
```

## API Keys Setup

### OpenAI
1. Visit https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env`

### ElevenLabs (Optional)
1. Visit https://elevenlabs.io
2. Get API key from profile
3. Add to `.env`

### Pexels (Optional)
1. Visit https://www.pexels.com/api/
2. Create free account
3. Get API key
4. Add to `.env`

### YouTube API
1. Visit https://console.cloud.google.com
2. Create project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Add credentials to `.env`

## Automation Schedule

Edit `config.py` to set:
- Upload frequency (daily, twice_daily, weekly)
- Best upload times
- Video length preferences

## Dashboard Features

- **Pipeline View** - See all videos and their stages
- **Stats** - Total videos, views, retention, CTR
- **Recent Activity** - Latest created videos
- **Manual Controls** - Edit, approve, or pause automation

## Safety & Compliance

- All scripts are original (no copying)
- Content is monetization-safe
- Copyright-free stock footage
- SEO-optimized metadata

## Troubleshooting

**No API key errors**: Check `.env` file has correct keys

**Video generation fails**: Ensure moviepy dependencies installed:
```bash
brew install ffmpeg  # macOS
```

**Upload fails**: Complete YouTube OAuth setup

## Next Steps

1. Set up API keys
2. Run first video creation
3. Review output in dashboard
4. Configure automation schedule
5. Set up YouTube OAuth for uploads

## License

MIT

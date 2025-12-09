# Quick Start Checklist

Use this checklist to get the project running in under 30 minutes.

---

## ☐ Step 1: Install Dependencies (5 min)

```bash
cd youtube-automation
pip install -r requirements.txt
```

**macOS users also need FFmpeg:**
```bash
brew install ffmpeg
```

---

## ☐ Step 2: Get OpenAI API Key (5 min)

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

---

## ☐ Step 3: Configure Environment (2 min)

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI key:
```
OPENAI_API_KEY=sk-your-key-here
```

---

## ☐ Step 4: Test the System (5 min)

```bash
python demo.py
```

This will:
- Generate a sample script
- Create voiceover audio
- Assemble a video with subtitles
- Save everything to `output/` folder

**Expected output:**
```
✓ Script generated
✓ Audio generated
✓ Video generated
✓ Video saved to: output/videos/demo_video.mp4
```

---

## ☐ Step 5: Launch Dashboard (2 min)

```bash
python dashboard.py
```

Open browser: http://localhost:5000

You should see:
- Video pipeline status
- Recent videos created
- Stats dashboard

---

## ☐ Step 6: Create Your First Real Video (5 min)

In the dashboard, click **"Create New Video"** or run:

```bash
python pipeline.py
```

This runs the full automation:
1. Sources trending topic
2. Generates script
3. Creates voiceover
4. Assembles video
5. Generates SEO metadata

Check `output/videos/` for your finished video!

---

## ☐ Step 7: Review the Output (5 min)

Open the generated video and check:
- ✓ Audio quality (clear voiceover)
- ✓ Subtitles (properly timed)
- ✓ Visuals (stock footage matches content)
- ✓ Length (45-120 seconds)

---

## 🎉 You're Done!

The system is working. Now you can:

### Next Steps:
1. **Read `PROJECT_VISION.md`** - Understand the big picture
2. **Read `HANDOFF_GUIDE.md`** - Learn the codebase
3. **Set up YouTube OAuth** - Enable automated uploads (see `API_KEYS_GUIDE.md`)
4. **Customize settings** - Edit `config.py` for your preferences

---

## Troubleshooting

### "No module named 'openai'"
```bash
pip install -r requirements.txt
```

### "FFmpeg not found"
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

### "Invalid API key"
- Check `.env` file has correct key
- No quotes around the key
- No extra spaces

### "Permission denied"
```bash
chmod +x *.py
```

### Still stuck?
Check `HANDOFF_GUIDE.md` section 9: "Common Issues & Solutions"

---

## File Structure After Setup

```
youtube-automation/
├── .env                    ← Your API keys (DO NOT COMMIT)
├── automation.db           ← Database (auto-created)
├── output/
│   ├── scripts/           ← Generated scripts
│   ├── audio/             ← Voiceovers
│   └── videos/            ← Final videos ✨
└── [all other files]
```

---

## What to Read Next

1. **Just want to use it?** → Read `README.md`
2. **Want to understand the vision?** → Read `PROJECT_VISION.md`
3. **Want to develop features?** → Read `HANDOFF_GUIDE.md`
4. **Need API setup help?** → Read `API_KEYS_GUIDE.md`

---

**Time to first video: ~30 minutes** ⏱️

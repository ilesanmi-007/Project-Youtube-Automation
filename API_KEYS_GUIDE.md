# API Keys Setup Guide

## 1. OpenAI API Key (REQUIRED)

### Step 1: Create OpenAI Account
1. Go to: https://platform.openai.com/signup
2. Sign up with email or Google account
3. Verify your email

### Step 2: Add Payment Method
1. Go to: https://platform.openai.com/account/billing
2. Click "Add payment method"
3. Add credit/debit card
4. Add $5-10 credit (enough for ~100 videos)

### Step 3: Get API Key
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it: "YouTube Automation"
4. Copy the key (starts with `sk-proj-...`)
5. **IMPORTANT**: Save it immediately - you can't see it again!

### Step 4: Add to .env File
```bash
OPENAI_API_KEY=sk-proj-your-key-here
```

**Cost**: ~$0.05-0.10 per video (script + metadata + audio)

---

## 2. ElevenLabs API Key (OPTIONAL - Better Voice Quality)

### Step 1: Create Account
1. Go to: https://elevenlabs.io
2. Sign up (free tier available)
3. Verify email

### Step 2: Get API Key
1. Click your profile icon (top right)
2. Go to "Profile Settings"
3. Find "API Key" section
4. Copy your API key

### Step 3: Add to .env
```bash
ELEVENLABS_API_KEY=your-elevenlabs-key-here
```

**Free Tier**: 10,000 characters/month (~10 videos)
**Paid**: $5/month for 30,000 characters (~30 videos)

**Note**: If not set, system uses OpenAI TTS (included in OpenAI costs)

---

## 3. Pexels API Key (OPTIONAL - Stock Footage)

### Step 1: Create Account
1. Go to: https://www.pexels.com/api/
2. Click "Get Started"
3. Sign up (completely free)

### Step 2: Get API Key
1. After signup, you'll see your API key immediately
2. Or go to: https://www.pexels.com/api/
3. Click "Your API Key"

### Step 3: Add to .env
```bash
PEXELS_API_KEY=your-pexels-key-here
```

**Free**: Unlimited requests
**Note**: If not set, system uses colored backgrounds

---

## 4. YouTube API (OPTIONAL - For Auto-Upload)

### Step 1: Create Google Cloud Project
1. Go to: https://console.cloud.google.com
2. Click "Select a project" → "New Project"
3. Name it: "YouTube Automation"
4. Click "Create"

### Step 2: Enable YouTube Data API
1. In your project, go to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click it and press "Enable"

### Step 3: Create OAuth Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: YouTube Automation
   - User support email: your email
   - Developer contact: your email
   - Save and continue through all steps
4. Back to "Create OAuth client ID":
   - Application type: Desktop app
   - Name: YouTube Automation
   - Click "Create"
5. Download the JSON file
6. Copy Client ID and Client Secret

### Step 4: Add to .env
```bash
YOUTUBE_CLIENT_ID=your-client-id.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=your-client-secret
```

**Note**: First time you upload, you'll need to authorize the app in browser

---

## Quick Start (Minimum Setup)

**To test the system, you only need:**

1. **OpenAI API Key** (required)
   - Cost: ~$0.05-0.10 per video
   - Get it: https://platform.openai.com/api-keys

**Optional for better quality:**
- ElevenLabs (better voice)
- Pexels (real stock footage)
- YouTube API (auto-upload)

---

## Your .env File Should Look Like:

```bash
# Required
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Optional
ELEVENLABS_API_KEY=
PEXELS_API_KEY=
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
```

---

## Cost Breakdown

### Minimum (OpenAI only):
- **Per video**: $0.05-0.10
- **100 videos**: ~$5-10
- **Monthly (daily uploads)**: ~$1.50-3.00

### With ElevenLabs:
- **Per video**: $0.15-0.20
- **100 videos**: ~$15-20
- **Monthly**: ~$4.50-6.00

### All Free Options:
- OpenAI: Pay as you go
- Pexels: Free forever
- YouTube: Free

---

## Testing Without API Keys

Run demo mode (no API keys needed):
```bash
python3 demo.py
```

This simulates the full pipeline without making API calls.

---

## Troubleshooting

**"Invalid API key"**
- Check for extra spaces in .env file
- Make sure key starts with `sk-proj-` or `sk-`
- Verify billing is set up on OpenAI

**"Insufficient credits"**
- Add funds to OpenAI account
- Check: https://platform.openai.com/account/billing

**"Rate limit exceeded"**
- Wait a few minutes
- Upgrade OpenAI tier if needed

---

## Next Steps

1. Get OpenAI API key (5 minutes)
2. Add to .env file
3. Run: `python3 pipeline.py`
4. Watch your first video get created!

Need help? Check the main README.md

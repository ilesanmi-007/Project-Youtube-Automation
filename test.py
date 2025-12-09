#!/usr/bin/env python3
"""Quick test to verify setup"""

import os
from dotenv import load_dotenv

load_dotenv()

print("🧪 Testing YouTube Automation Setup\n")
print("="*50)

# Check API key
api_key = os.getenv('OPENAI_API_KEY')
if api_key and len(api_key) > 10:
    print("✅ OpenAI API key found")
else:
    print("❌ OpenAI API key missing")
    print("\n📝 To add your API key:")
    print("1. Open .env file")
    print("2. Add: OPENAI_API_KEY=your_key_here")
    print("3. Get key from: https://platform.openai.com/api-keys")
    exit(1)

# Check dependencies
print("\n📦 Checking dependencies...")
try:
    import openai
    print("✅ openai")
except ImportError:
    print("❌ openai - Run: pip install openai")

try:
    import flask
    print("✅ flask")
except ImportError:
    print("❌ flask - Run: pip install flask")

try:
    import requests
    print("✅ requests")
except ImportError:
    print("❌ requests - Run: pip install requests")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv")
except ImportError:
    print("❌ python-dotenv - Run: pip install python-dotenv")

print("\n" + "="*50)
print("✅ Setup complete! Ready to test.\n")
print("Next steps:")
print("1. Run dashboard: python3 dashboard.py")
print("2. Visit: http://localhost:5000")
print("3. Click 'Create New Video'")
print("\nOr test pipeline directly: python3 pipeline.py")

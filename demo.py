#!/usr/bin/env python3
"""Demo mode - simulates pipeline without API calls"""

import time
import os
import database

def demo_pipeline():
    """Simulate the full pipeline"""
    
    print("\n" + "="*50)
    print("🎬 YOUTUBE AUTOMATION DEMO")
    print("="*50)
    
    # Initialize database
    database.init_db()
    
    # Stage 1: Content Sourcing
    print("\n📍 STAGE 1: CONTENT SOURCING")
    print("🔍 Scanning trending topics...")
    time.sleep(1)
    topic = "Why most people fail at building habits (and how to fix it)"
    print(f"✅ Selected topic: {topic}")
    
    video_id = database.add_video(topic, stage='sourcing')
    
    # Stage 2: Script Generation
    print("\n📍 STAGE 2: SCRIPT GENERATION")
    print("📝 Generating original script...")
    time.sleep(1)
    script = """You wake up motivated. You promise yourself: today is different.
But by noon, the old patterns return. The habits you swore you'd break.

Here's what nobody tells you: willpower is a myth.
Your brain doesn't run on motivation. It runs on systems.

Every habit you have exists because it solved a problem once.
The cigarette calmed your nerves. The scroll numbed the boredom.
Your brain remembers. And it will choose comfort over change. Every time.

So stop fighting your brain. Redesign your environment instead.
Make the good choice the easy choice. Make the bad choice harder.

Want to read more? Put the book on your pillow.
Want to stop scrolling? Delete the app.

You don't need more discipline. You need better design.
Your future self will thank you."""
    
    print(f"✅ Script created ({len(script.split())} words)")
    database.update_video(video_id, script=script, stage='audio_generation')
    
    # Stage 3: Audio Generation
    print("\n📍 STAGE 3: AUDIO GENERATION")
    print("🎙️  Generating voiceover...")
    time.sleep(1)
    
    os.makedirs('output/audio', exist_ok=True)
    audio_path = f"output/audio/video_{video_id}.mp3"
    
    # Create dummy audio file
    with open(audio_path, 'w') as f:
        f.write("(Audio file placeholder)")
    
    print(f"✅ Audio created: {audio_path}")
    database.update_video(video_id, audio_path=audio_path, stage='video_generation')
    
    # Stage 4: Video Generation
    print("\n📍 STAGE 4: VIDEO GENERATION")
    print("🎬 Creating video with footage and subtitles...")
    time.sleep(2)
    
    os.makedirs('output/videos', exist_ok=True)
    video_path = f"output/videos/video_{video_id}.mp4"
    
    # Create dummy video file
    with open(video_path, 'w') as f:
        f.write("(Video file placeholder)")
    
    print(f"✅ Video created: {video_path}")
    database.update_video(video_id, video_path=video_path, stage='metadata_generation')
    
    # Stage 5: SEO Metadata
    print("\n📍 STAGE 5: METADATA GENERATION")
    print("🏷️  Generating SEO metadata...")
    time.sleep(1)
    
    metadata = {
        "title": "Why You Can't Stick to Habits (The Real Reason)",
        "description": "Discover why willpower fails and how to build lasting habits...",
        "tags": ["habits", "self-improvement", "productivity", "motivation"],
        "hashtags": ["#habits", "#selfimprovement", "#productivity"]
    }
    
    print(f"✅ Metadata created")
    print(f"   Title: {metadata['title']}")
    database.update_video(video_id, description=str(metadata), stage='scheduling')
    
    # Stage 6: Scheduling
    print("\n📍 STAGE 6: SCHEDULING")
    print("📅 Scheduling upload...")
    time.sleep(1)
    
    from datetime import datetime, timedelta
    scheduled_time = datetime.now() + timedelta(hours=2)
    
    print(f"✅ Scheduled for: {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    database.update_video(
        video_id,
        scheduled_time=scheduled_time.isoformat(),
        stage='scheduled',
        status='ready'
    )
    
    # Summary
    print("\n" + "="*50)
    print("✅ PIPELINE COMPLETE!")
    print("="*50)
    print(f"Video ID: {video_id}")
    print(f"Topic: {topic}")
    print(f"Script: {len(script.split())} words")
    print(f"Status: Ready for upload")
    print(f"Scheduled: {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    print("\n💡 In production mode, this would:")
    print("   - Use real AI for content generation")
    print("   - Generate actual voiceover audio")
    print("   - Create real video with stock footage")
    print("   - Upload to YouTube automatically")
    print("\n📊 View in dashboard: python3 dashboard.py")
    
    return video_id

if __name__ == "__main__":
    demo_pipeline()

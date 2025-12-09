#!/usr/bin/env python3
"""Demo pipeline that simulates video creation without requiring API keys"""

import database
import time
from datetime import datetime

def simulate_pipeline():
    """Simulate the full pipeline with demo data"""
    
    print("\n" + "="*60)
    print("🎬 YOUTUBE AUTOMATION - DEMO MODE")
    print("="*60)
    print("Simulating video creation without API keys...\n")
    
    # Initialize database
    database.init_db()
    
    # Create demo video
    topic = "5 Morning Habits That Will Transform Your Productivity"
    print(f"📝 Topic: {topic}\n")
    
    # Stage 1: Content Sourcing
    print("="*60)
    print("STAGE 1: CONTENT SOURCING (0%)")
    print("="*60)
    video_id = database.add_video(topic, 1, 'custom', 'sourcing')
    database.update_video(video_id, stage_progress=0)
    print(f"✅ Video ID {video_id} created")
    time.sleep(1)
    
    # Stage 2: Script Generation
    print("\n" + "="*60)
    print("STAGE 2: SCRIPT GENERATION (20%)")
    print("="*60)
    script = f"""Welcome to today's video about {topic}.

In this video, we'll explore five powerful morning habits that successful people use to maximize their productivity.

Habit 1: Wake up early and start with meditation
Habit 2: Exercise for at least 30 minutes
Habit 3: Plan your day with clear priorities
Habit 4: Eat a healthy breakfast
Habit 5: Review your goals and visualize success

These habits, when practiced consistently, can transform your entire day and boost your productivity significantly.

Thanks for watching! Don't forget to like and subscribe for more productivity tips."""
    
    database.update_video(video_id, script=script, stage='script_generation', stage_progress=20)
    database.log_stage(video_id, 'script_generation', 'completed', f'Script generated ({len(script)} chars)')
    print(f"✅ Script generated ({len(script)} characters)")
    time.sleep(1)
    
    # Stage 3: Audio Generation
    print("\n" + "="*60)
    print("STAGE 3: AUDIO GENERATION (40%)")
    print("="*60)
    audio_path = f"output/audio/audio_{video_id}_demo.mp3"
    database.update_video(video_id, audio_path=audio_path, stage='audio_generation', stage_progress=40)
    database.log_stage(video_id, 'audio_generation', 'completed', f'Audio saved: {audio_path}')
    print(f"✅ Audio generated: {audio_path}")
    time.sleep(1)
    
    # Stage 4: Video Generation
    print("\n" + "="*60)
    print("STAGE 4: VIDEO GENERATION (60%)")
    print("="*60)
    video_path = f"output/videos/video_{video_id}_demo.mp4"
    database.update_video(video_id, video_path=video_path, stage='video_generation', stage_progress=60)
    database.log_stage(video_id, 'video_generation', 'completed', f'Video saved: {video_path}')
    print(f"✅ Video generated: {video_path}")
    time.sleep(1)
    
    # Stage 5: Metadata Generation
    print("\n" + "="*60)
    print("STAGE 5: METADATA GENERATION (80%)")
    print("="*60)
    title = "5 Morning Habits That Will Transform Your Productivity | Productivity Tips 2024"
    description = """Discover the 5 powerful morning habits that successful entrepreneurs use to maximize their productivity every single day.

🔥 In this video, you'll learn:
• How to start your day with intention
• The importance of morning exercise
• Planning techniques that actually work
• Nutrition tips for peak performance
• Goal visualization strategies

💡 These habits have been proven to increase productivity by up to 40%!

👉 Subscribe for more productivity tips and life hacks!

#productivity #morningroutine #success #habits #entrepreneur"""
    
    tags = "productivity,morning routine,success habits,entrepreneur,self improvement,motivation"
    
    database.update_video(
        video_id,
        title=title,
        description=description,
        tags=tags,
        stage='metadata_generation',
        stage_progress=80
    )
    database.log_stage(video_id, 'metadata_generation', 'completed', f'Title: {title}')
    print(f"✅ Metadata generated")
    print(f"   Title: {title[:50]}...")
    time.sleep(1)
    
    # Stage 6: Scheduling
    print("\n" + "="*60)
    print("STAGE 6: SCHEDULING (90%)")
    print("="*60)
    scheduled_time = datetime.now().isoformat()
    database.update_video(
        video_id,
        scheduled_time=scheduled_time,
        stage='scheduling',
        stage_progress=90
    )
    database.log_stage(video_id, 'scheduling', 'completed', f'Scheduled: {scheduled_time}')
    print(f"✅ Video scheduled for upload")
    time.sleep(1)
    
    # Stage 7: Completed
    print("\n" + "="*60)
    print("STAGE 7: COMPLETED (100%)")
    print("="*60)
    database.update_video(
        video_id,
        stage='completed',
        stage_progress=100,
        status='ready'
    )
    database.log_stage(video_id, 'completed', 'completed', 'Pipeline completed successfully')
    print(f"✅ Pipeline completed!")
    
    print("\n" + "="*60)
    print("🎉 DEMO COMPLETE!")
    print("="*60)
    print(f"Video ID: {video_id}")
    print(f"Status: Ready for upload")
    print(f"Title: {title}")
    print("\n💡 Open the dashboard to see the results:")
    print("   http://localhost:5000")
    print("="*60 + "\n")
    
    return video_id

if __name__ == "__main__":
    simulate_pipeline()

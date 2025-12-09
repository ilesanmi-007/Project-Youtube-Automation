import config
import os

def create_video(audio_path, script, video_id, topic):
    """Simplified video generator - creates placeholder"""
    video_path = f"{config.VIDEO_DIR}/video_{video_id}.mp4"
    
    print(f"  📹 Video generation simulated")
    print(f"  Audio: {audio_path}")
    print(f"  Script length: {len(script)} chars")
    print(f"  Topic: {topic}")
    
    # Create placeholder file
    with open(video_path, 'w') as f:
        f.write("placeholder video")
    
    print(f"  ✅ Video placeholder created: {video_path}")
    return video_path

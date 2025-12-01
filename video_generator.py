import requests
import os
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import config

def download_stock_footage(topic, count=3):
    """Download relevant stock footage from Pexels"""
    if not config.PEXELS_API_KEY:
        print("⚠️  Pexels API key not set, using placeholder")
        return []
    
    headers = {"Authorization": config.PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={topic}&per_page={count}&orientation=landscape"
    
    response = requests.get(url, headers=headers)
    videos = response.json().get('videos', [])
    
    footage_paths = []
    for i, video in enumerate(videos):
        video_file = video['video_files'][0]
        video_url = video_file['link']
        
        output_path = f"temp/footage_{i}.mp4"
        os.makedirs('temp', exist_ok=True)
        
        vid_response = requests.get(video_url)
        with open(output_path, 'wb') as f:
            f.write(vid_response.content)
        
        footage_paths.append(output_path)
    
    return footage_paths

def create_subtitles(script):
    """Generate subtitle file from script"""
    words = script.split()
    subs = []
    words_per_sub = 5
    time_per_word = 0.4
    
    for i in range(0, len(words), words_per_sub):
        chunk = ' '.join(words[i:i+words_per_sub])
        start = i * time_per_word
        end = (i + words_per_sub) * time_per_word
        subs.append(((start, end), chunk))
    
    return subs

def create_video(audio_path, script, video_id, topic):
    """Main function to create video with footage and subtitles"""
    print("🎬 Creating video...")
    
    os.makedirs(config.VIDEO_DIR, exist_ok=True)
    output_path = f"{config.VIDEO_DIR}/video_{video_id}.mp4"
    
    # Load audio
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    # Download footage
    footage_paths = download_stock_footage(topic.replace(' ', '+'))
    
    if footage_paths:
        clips = [VideoFileClip(f).resize((config.VIDEO_WIDTH, config.VIDEO_HEIGHT)) 
                 for f in footage_paths]
        
        # Loop clips to match audio duration
        video_clip = concatenate_videoclips(clips * int(duration / sum(c.duration for c in clips) + 1))
        video_clip = video_clip.subclip(0, duration)
    else:
        # Fallback: colored background
        video_clip = ColorClip(size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT), 
                               color=(20, 20, 40), duration=duration)
    
    # Add subtitles
    subs = create_subtitles(script)
    generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=70, 
                                     color='white', stroke_color='black', 
                                     stroke_width=2, method='caption', 
                                     size=(config.VIDEO_WIDTH-100, None))
    subtitles = SubtitlesClip(subs, generator)
    
    # Combine
    final = CompositeVideoClip([video_clip, subtitles.set_position(('center', 'bottom'))])
    final = final.set_audio(audio)
    
    # Export
    final.write_videofile(output_path, fps=config.VIDEO_FPS, codec='libx264', 
                          audio_codec='aac', threads=4, preset='medium')
    
    print(f"✓ Video created: {output_path}")
    return output_path

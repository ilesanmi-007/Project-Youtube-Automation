import database
import content_sourcer
import script_generator
import audio_generator
try:
    import video_generator
except:
    import video_generator_simple as video_generator
import seo_generator
import youtube_uploader
import traceback
from datetime import datetime

STAGES = [
    ('sourcing', 'Content Sourcing', 0),
    ('script_generation', 'Script Generation', 20),
    ('audio_generation', 'Audio Generation', 40),
    ('video_generation', 'Video Generation', 60),
    ('metadata_generation', 'Metadata Generation', 80),
    ('scheduling', 'Scheduling Upload', 90),
    ('completed', 'Completed', 100)
]

def update_stage(video_id, stage_key, status='in_progress', message=''):
    stage_info = next((s for s in STAGES if s[0] == stage_key), None)
    if stage_info:
        database.update_video(video_id, stage=stage_key, stage_progress=stage_info[2])
        database.log_stage(video_id, stage_key, status, message)
        print(f"  [{stage_info[2]}%] {stage_info[1]}: {message}")

def run_pipeline(channel_id=1, content_source='trending', custom_topic=None):
    """Execute full content creation pipeline with stage tracking"""
    video_id = None
    
    try:
        database.init_db()
        
        # Stage 1: Content Sourcing
        print("\n" + "="*60)
        print("STAGE 1: CONTENT SOURCING")
        print("="*60)
        
        if custom_topic:
            topic = custom_topic
            update_stage(video_id, 'sourcing', 'completed', f'Using custom topic: {topic}')
        else:
            topic = content_sourcer.source_content()
            update_stage(video_id, 'sourcing', 'completed', f'Sourced topic: {topic}')
        
        video_id = database.add_video(topic, channel_id, content_source, 'sourcing')
        update_stage(video_id, 'sourcing', 'completed', f'Topic: {topic}')
        
        # Stage 2: Script Generation
        print("\n" + "="*60)
        print("STAGE 2: SCRIPT GENERATION")
        print("="*60)
        update_stage(video_id, 'script_generation', 'in_progress', 'Generating script...')
        
        script, duration = script_generator.create_script(topic)
        database.update_video(video_id, script=script)
        update_stage(video_id, 'script_generation', 'completed', f'Script generated ({duration}s)')
        
        # Stage 3: Audio Generation
        print("\n" + "="*60)
        print("STAGE 3: AUDIO GENERATION")
        print("="*60)
        update_stage(video_id, 'audio_generation', 'in_progress', 'Generating voiceover...')
        
        audio_path = audio_generator.create_audio(script, video_id)
        database.update_video(video_id, audio_path=audio_path)
        update_stage(video_id, 'audio_generation', 'completed', f'Audio saved: {audio_path}')
        
        # Stage 4: Video Generation
        print("\n" + "="*60)
        print("STAGE 4: VIDEO GENERATION")
        print("="*60)
        update_stage(video_id, 'video_generation', 'in_progress', 'Assembling video...')
        
        video_path = video_generator.create_video(audio_path, script, video_id, topic)
        database.update_video(video_id, video_path=video_path)
        update_stage(video_id, 'video_generation', 'completed', f'Video saved: {video_path}')
        
        # Stage 5: SEO Metadata
        print("\n" + "="*60)
        print("STAGE 5: METADATA GENERATION")
        print("="*60)
        update_stage(video_id, 'metadata_generation', 'in_progress', 'Creating SEO metadata...')
        
        metadata = seo_generator.create_metadata(topic, script)
        database.update_video(
            video_id, 
            title=metadata.get('title', topic),
            description=metadata.get('description', ''),
            tags=str(metadata.get('tags', []))
        )
        update_stage(video_id, 'metadata_generation', 'completed', f'Title: {metadata.get("title")}')
        
        # Stage 6: Schedule Upload
        print("\n" + "="*60)
        print("STAGE 6: SCHEDULING UPLOAD")
        print("="*60)
        update_stage(video_id, 'scheduling', 'in_progress', 'Scheduling upload...')
        
        upload_data = youtube_uploader.upload_to_youtube(video_path, metadata)
        database.update_video(
            video_id, 
            scheduled_time=str(upload_data['scheduled_time']),
            status='ready'
        )
        update_stage(video_id, 'scheduling', 'completed', f'Scheduled: {upload_data["scheduled_time"]}')
        update_stage(video_id, 'completed', 'completed', 'Pipeline completed successfully')
        
        print("\n" + "="*60)
        print("✅ PIPELINE COMPLETE")
        print("="*60)
        print(f"Video ID: {video_id}")
        print(f"Topic: {topic}")
        print(f"Video: {video_path}")
        print(f"Scheduled: {upload_data['scheduled_time']}")
        
        return video_id
        
    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"\n❌ ERROR: {str(e)}")
        print(error_msg)
        
        if video_id:
            database.update_video(video_id, status='failed', error_log=error_msg)
            database.log_stage(video_id, 'error', 'failed', str(e))
        
        return None

if __name__ == "__main__":
    run_pipeline()

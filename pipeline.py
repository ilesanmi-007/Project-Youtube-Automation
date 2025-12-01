import database
import content_sourcer
import script_generator
import audio_generator
import video_generator
import seo_generator
import youtube_uploader
import traceback
from datetime import datetime

def run_pipeline():
    """Execute full content creation pipeline"""
    video_id = None
    
    try:
        # Initialize database
        database.init_db()
        
        # Stage 1: Content Sourcing
        print("\n" + "="*50)
        print("STAGE 1: CONTENT SOURCING")
        print("="*50)
        topic = content_sourcer.source_content()
        video_id = database.add_video(topic, stage='sourcing')
        database.update_video(video_id, stage='script_generation')
        
        # Stage 2: Script Generation
        print("\n" + "="*50)
        print("STAGE 2: SCRIPT GENERATION")
        print("="*50)
        script, duration = script_generator.create_script(topic)
        database.update_video(video_id, script=script, stage='audio_generation')
        
        # Stage 3: Audio Generation
        print("\n" + "="*50)
        print("STAGE 3: AUDIO GENERATION")
        print("="*50)
        audio_path = audio_generator.create_audio(script, video_id)
        database.update_video(video_id, audio_path=audio_path, stage='video_generation')
        
        # Stage 4: Video Generation
        print("\n" + "="*50)
        print("STAGE 4: VIDEO GENERATION")
        print("="*50)
        video_path = video_generator.create_video(audio_path, script, video_id, topic)
        database.update_video(video_id, video_path=video_path, stage='metadata_generation')
        
        # Stage 5: SEO Metadata
        print("\n" + "="*50)
        print("STAGE 5: METADATA GENERATION")
        print("="*50)
        metadata = seo_generator.create_metadata(topic, script)
        database.update_video(video_id, description=metadata, stage='scheduling')
        
        # Stage 6: Schedule Upload
        print("\n" + "="*50)
        print("STAGE 6: SCHEDULING UPLOAD")
        print("="*50)
        upload_data = youtube_uploader.upload_to_youtube(video_path, metadata)
        database.update_video(
            video_id, 
            scheduled_time=str(upload_data['scheduled_time']),
            stage='scheduled',
            status='ready'
        )
        
        print("\n" + "="*50)
        print("✅ PIPELINE COMPLETE")
        print("="*50)
        print(f"Video ID: {video_id}")
        print(f"Topic: {topic}")
        print(f"Scheduled: {upload_data['scheduled_time']}")
        
        return video_id
        
    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"\n❌ ERROR: {str(e)}")
        print(error_msg)
        
        if video_id:
            database.update_video(video_id, status='failed', error_log=error_msg)
        
        return None

if __name__ == "__main__":
    run_pipeline()

from flask import Flask, render_template, jsonify, request
import database
import pipeline
import threading
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/videos')
def get_videos():
    videos = database.get_all_videos()
    columns = ['id', 'channel_id', 'topic', 'content_source', 'script', 'audio_path', 'video_path', 
               'thumbnail_path', 'title', 'description', 'tags', 'status', 'stage', 'stage_progress',
               'requires_review', 'approved', 'scheduled_time', 'youtube_id', 'views', 'ctr', 
               'retention', 'created_at', 'uploaded_at', 'error_log']
    
    videos_list = []
    for video in videos:
        video_dict = dict(zip(columns, video))
        videos_list.append(video_dict)
    
    return jsonify(videos_list)

@app.route('/api/video/<int:video_id>')
def get_video(video_id):
    video = database.get_video(video_id)
    if video:
        columns = ['id', 'channel_id', 'topic', 'content_source', 'script', 'audio_path', 'video_path',
                   'thumbnail_path', 'title', 'description', 'tags', 'status', 'stage', 'stage_progress',
                   'requires_review', 'approved', 'scheduled_time', 'youtube_id', 'views', 'ctr',
                   'retention', 'created_at', 'uploaded_at', 'error_log']
        return jsonify(dict(zip(columns, video)))
    return jsonify({'error': 'Video not found'}), 404

@app.route('/api/video/<int:video_id>/logs')
def get_video_logs(video_id):
    logs = database.get_stage_logs(video_id)
    columns = ['id', 'video_id', 'stage', 'status', 'message', 'timestamp']
    logs_list = [dict(zip(columns, log)) for log in logs]
    return jsonify(logs_list)

@app.route('/api/create', methods=['POST'])
def create_video():
    data = request.json or {}
    channel_id = data.get('channel_id', 1)
    content_source = data.get('content_source', 'trending')
    custom_topic = data.get('topic')
    
    def run_async():
        pipeline.run_pipeline(channel_id, content_source, custom_topic)
    
    thread = threading.Thread(target=run_async)
    thread.start()
    
    return jsonify({'status': 'started', 'message': 'Video creation pipeline started'})

@app.route('/api/update/<int:video_id>', methods=['POST'])
def update_video(video_id):
    data = request.json
    database.update_video(video_id, **data)
    return jsonify({'status': 'updated'})

@app.route('/api/approve/<int:video_id>', methods=['POST'])
def approve_video(video_id):
    database.update_video(video_id, approved=1, requires_review=0)
    return jsonify({'status': 'approved'})

@app.route('/api/stats')
def get_stats():
    videos = database.get_all_videos()
    
    # Column indices: 0=id, 1=channel_id, 2=topic, 3=content_source, 4=script, 5=audio_path, 
    # 6=video_path, 7=thumbnail_path, 8=title, 9=description, 10=tags, 11=status, 12=stage, 
    # 13=stage_progress, 14=requires_review, 15=approved, 16=scheduled_time, 17=youtube_id, 
    # 18=views, 19=ctr, 20=retention, 21=created_at, 22=uploaded_at, 23=error_log
    
    stats = {
        'total_videos': len(videos),
        'pending': len([v for v in videos if v[11] == 'pending']),
        'ready': len([v for v in videos if v[11] == 'ready']),
        'uploaded': len([v for v in videos if v[11] == 'uploaded']),
        'failed': len([v for v in videos if v[11] == 'failed']),
        'total_views': sum([v[18] or 0 for v in videos]),
        'avg_ctr': sum([v[19] or 0 for v in videos]) / len(videos) if videos else 0,
        'avg_retention': sum([v[20] or 0 for v in videos]) / len(videos) if videos else 0
    }
    
    return jsonify(stats)

@app.route('/api/channels')
def get_channels():
    channels = database.get_all_channels()
    columns = ['id', 'name', 'niche', 'youtube_channel_id', 'upload_frequency', 'status', 'created_at']
    channels_list = [dict(zip(columns, channel)) for channel in channels]
    return jsonify(channels_list)

@app.route('/api/channels/create', methods=['POST'])
def create_channel():
    data = request.json
    channel_id = database.add_channel(data['name'], data['niche'])
    return jsonify({'status': 'created', 'channel_id': channel_id})

if __name__ == '__main__':
    database.init_db()
    print("\n" + "="*60)
    print("🎬 YouTube Automation Dashboard")
    print("="*60)
    print("Dashboard running at: http://localhost:5000")
    print("Press CTRL+C to stop")
    print("="*60 + "\n")
    app.run(debug=True, port=5000, use_reloader=False)

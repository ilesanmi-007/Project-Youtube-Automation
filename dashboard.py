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
    columns = ['id', 'topic', 'script', 'audio_path', 'video_path', 'thumbnail_path',
               'title', 'description', 'tags', 'status', 'stage', 'scheduled_time',
               'youtube_id', 'views', 'ctr', 'retention', 'created_at', 'uploaded_at', 'error_log']
    
    videos_list = []
    for video in videos:
        video_dict = dict(zip(columns, video))
        videos_list.append(video_dict)
    
    return jsonify(videos_list)

@app.route('/api/video/<int:video_id>')
def get_video(video_id):
    video = database.get_video(video_id)
    if video:
        columns = ['id', 'topic', 'script', 'audio_path', 'video_path', 'thumbnail_path',
                   'title', 'description', 'tags', 'status', 'stage', 'scheduled_time',
                   'youtube_id', 'views', 'ctr', 'retention', 'created_at', 'uploaded_at', 'error_log']
        return jsonify(dict(zip(columns, video)))
    return jsonify({'error': 'Video not found'}), 404

@app.route('/api/create', methods=['POST'])
def create_video():
    def run_async():
        pipeline.run_pipeline()
    
    thread = threading.Thread(target=run_async)
    thread.start()
    
    return jsonify({'status': 'started', 'message': 'Video creation pipeline started'})

@app.route('/api/update/<int:video_id>', methods=['POST'])
def update_video(video_id):
    data = request.json
    database.update_video(video_id, **data)
    return jsonify({'status': 'updated'})

@app.route('/api/stats')
def get_stats():
    videos = database.get_all_videos()
    
    stats = {
        'total_videos': len(videos),
        'pending': len([v for v in videos if v[9] == 'pending']),
        'ready': len([v for v in videos if v[9] == 'ready']),
        'uploaded': len([v for v in videos if v[9] == 'uploaded']),
        'failed': len([v for v in videos if v[9] == 'failed']),
        'total_views': sum([v[13] or 0 for v in videos]),
        'avg_ctr': sum([v[14] or 0 for v in videos]) / len(videos) if videos else 0,
        'avg_retention': sum([v[15] or 0 for v in videos]) / len(videos) if videos else 0
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True, port=5000)

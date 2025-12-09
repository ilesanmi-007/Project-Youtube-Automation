from flask import Flask, render_template, jsonify, request
import database
import demo

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

@app.route('/api/create', methods=['POST'])
def create_video():
    video_id = demo.demo_pipeline()
    return jsonify({'status': 'completed', 'video_id': video_id})

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
    print("\n" + "="*50)
    print("🎬 YouTube Automation Dashboard")
    print("="*50)
    print("\n✅ Dashboard starting...")
    print("📊 Open: http://localhost:5000")
    print("\n💡 Click 'Create New Video' to run demo pipeline")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)

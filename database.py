import sqlite3
from datetime import datetime
import config

def init_db():
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    
    # Channels table
    c.execute('''CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        niche TEXT,
        youtube_channel_id TEXT,
        upload_frequency TEXT DEFAULT 'daily',
        status TEXT DEFAULT 'active',
        created_at TEXT
    )''')
    
    # Videos table with enhanced tracking
    c.execute('''CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id INTEGER DEFAULT 1,
        topic TEXT,
        content_source TEXT,
        script TEXT,
        audio_path TEXT,
        video_path TEXT,
        thumbnail_path TEXT,
        title TEXT,
        description TEXT,
        tags TEXT,
        status TEXT DEFAULT 'pending',
        stage TEXT DEFAULT 'sourcing',
        stage_progress INTEGER DEFAULT 0,
        requires_review BOOLEAN DEFAULT 0,
        approved BOOLEAN DEFAULT 0,
        scheduled_time TEXT,
        youtube_id TEXT,
        views INTEGER DEFAULT 0,
        ctr REAL DEFAULT 0,
        retention REAL DEFAULT 0,
        created_at TEXT,
        uploaded_at TEXT,
        error_log TEXT,
        FOREIGN KEY (channel_id) REFERENCES channels(id)
    )''')
    
    # Stage logs for detailed tracking
    c.execute('''CREATE TABLE IF NOT EXISTS stage_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id INTEGER,
        stage TEXT,
        status TEXT,
        message TEXT,
        timestamp TEXT,
        FOREIGN KEY (video_id) REFERENCES videos(id)
    )''')
    
    # Insert default channel if none exists
    c.execute('SELECT COUNT(*) FROM channels')
    if c.fetchone()[0] == 0:
        c.execute('''INSERT INTO channels (name, niche, status, created_at) 
                     VALUES (?, ?, ?, ?)''', 
                  ('Main Channel', 'General', 'active', datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def add_video(topic, channel_id=1, content_source='trending', stage='sourcing'):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO videos (channel_id, topic, content_source, stage, status, created_at) 
                 VALUES (?, ?, ?, ?, 'pending', ?)''', 
              (channel_id, topic, content_source, stage, datetime.now().isoformat()))
    video_id = c.lastrowid
    conn.commit()
    conn.close()
    
    # Log after committing
    log_stage(video_id, stage, 'started', f'Video creation started with topic: {topic}')
    return video_id

def update_video(video_id, **kwargs):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    fields = ', '.join([f'{k}=?' for k in kwargs.keys()])
    values = list(kwargs.values()) + [video_id]
    c.execute(f'UPDATE videos SET {fields} WHERE id=?', values)
    conn.commit()
    conn.close()

def get_video(video_id):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM videos WHERE id=?', (video_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_all_videos():
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM videos ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def log_stage(video_id, stage, status, message):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO stage_logs (video_id, stage, status, message, timestamp)
                 VALUES (?, ?, ?, ?, ?)''',
              (video_id, stage, status, message, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_stage_logs(video_id):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM stage_logs WHERE video_id=? ORDER BY timestamp DESC', (video_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def add_channel(name, niche):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO channels (name, niche, status, created_at)
                 VALUES (?, ?, 'active', ?)''',
              (name, niche, datetime.now().isoformat()))
    channel_id = c.lastrowid
    conn.commit()
    conn.close()
    return channel_id

def get_all_channels():
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM channels ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_channel(channel_id):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM channels WHERE id=?', (channel_id,))
    row = c.fetchone()
    conn.close()
    return row

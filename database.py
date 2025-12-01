import sqlite3
from datetime import datetime
import config

def init_db():
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        script TEXT,
        audio_path TEXT,
        video_path TEXT,
        thumbnail_path TEXT,
        title TEXT,
        description TEXT,
        tags TEXT,
        status TEXT,
        stage TEXT,
        scheduled_time TEXT,
        youtube_id TEXT,
        views INTEGER DEFAULT 0,
        ctr REAL DEFAULT 0,
        retention REAL DEFAULT 0,
        created_at TEXT,
        uploaded_at TEXT,
        error_log TEXT
    )''')
    
    conn.commit()
    conn.close()

def add_video(topic, stage='sourcing'):
    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO videos (topic, stage, status, created_at) 
                 VALUES (?, ?, 'pending', ?)''', 
              (topic, stage, datetime.now().isoformat()))
    video_id = c.lastrowid
    conn.commit()
    conn.close()
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

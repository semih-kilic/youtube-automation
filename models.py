# /home/semih/youtube-automation/models.py - TAM KODU
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import pytz

db = SQLAlchemy()
TORONTO_TZ = pytz.timezone('America/Toronto')

def get_toronto_time():
    return datetime.datetime.now(TORONTO_TZ)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- YENİ KANAL MODELİ ---
class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    youtube_channel_id = db.Column(db.String(100), unique=True, nullable=False)
    # Gerçek YouTube API anahtarlarını saklamak için (şimdilik boş)
    credentials_json = db.Column(db.Text, nullable=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('channels', lazy=True))

# --- STRATEJİ MODELİ GÜNCELLENDİ ---
class Strategy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_path = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100), nullable=True) # <-- Kategori alanı eklendi
    status = db.Column(db.String(50), default='Beklemede')
    created_at = db.Column(db.DateTime(timezone=True), default=get_toronto_time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # --- Stratejiye kanal bağlantısı eklendi ---
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    channel = db.relationship('Channel', backref=db.backref('strategies', lazy=True))
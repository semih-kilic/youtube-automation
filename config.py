import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cok-gizli-bir-anahtar'
    # --- VERİTABANI YOLU SABİTLENDİ ---
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'cok-daha-gizli-bir-jwt-anahtari'
    
    # --- CELERY KONFİGÜRASYONU ---
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # --- ZAMAN AYARLARI ---
    CELERY_TIMEZONE = 'America/Toronto'
    CELERY_ENABLE_UTC = False
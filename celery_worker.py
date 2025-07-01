# /home/semih/youtube-automation/celery_worker.py - TAM KODU
from app import create_app
from celery import Celery
from celery.schedules import crontab
import time
import datetime
from pytrends.request import TrendReq
import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
import subprocess

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Celery app configuration
def make_celery():
    app = create_app()
    celery = Celery(app.import_name)
    celery.conf.update(
        broker_url='redis://redis:6379/0',
        result_backend='redis://redis:6379/0',
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='America/Toronto',
        enable_utc=True,
    )
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

celery_app = make_celery()

# --- YENİ GÖREV 1: TREND BULMA ---
@celery_app.task
def fetch_trends_task(keyword="Science & Technology"):
    """
    Belirtilen anahtar kelime için Google Trends'den ilgili sorguları çeker.
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe='now 1-d', geo='', gprop='')
        related_queries = pytrends.related_queries()
        
        # 'rising' (yükselen) sorguları alıyoruz
        rising_queries = related_queries[keyword]['rising']
        if rising_queries is not None and not rising_queries.empty:
            # En çok yükselen sorguyu seçiyoruz
            trend_topic = rising_queries.iloc[0]['query']
            print(f"Trend Bulundu: '{keyword}' kategorisi için en popüler konu: '{trend_topic}'")
            return trend_topic
        else:
            print(f"Trend Bulunamadı: '{keyword}' için yükselen sorgu yok.")
            return f"Default Topic for {keyword}"
    except Exception as e:
        print(f"Google Trends'den veri çekerken hata oluştu: {e}")
        # Hata durumunda varsayılan bir konu döndür
        return f"Default Topic for {keyword}"


# --- GÖREV 2: OTOMATİK STRATEJİ OLUŞTURMA (GÜNCELLENDİ) ---
@celery_app.task
def create_daily_strategy_task(channel_id, category, user_id):
    from models import db, Strategy
    
    # Önce trendi bul
    trend_topic = fetch_trends_task.s(keyword=category).apply().get()

    # Trendi kullanarak başlık oluştur
    title = f"{trend_topic} | Chimera Otomasyonu"
    description = f"Bu videoda, {trend_topic} konusunu inceliyoruz. #shorts #{category.replace(' ', '').replace('&', '')}"
    video_path = f"/videos/auto/{category.lower().replace(' ', '_')}.mp4"

    new_strategy = Strategy(
        title=title,
        description=description,
        video_path=video_path,
        category=category,
        channel_id=channel_id,
        user_id=user_id
    )
    db.session.add(new_strategy)
    db.session.commit()
    
    print(f"Otonom Görev: '{title}' başlıklı yeni strateji oluşturuldu (ID: {new_strategy.id}).")
    upload_video_task.delay(new_strategy.id)


# --- GÖREV 3: VİDEO YÜKLEME ---
@celery_app.task(bind=True)
def upload_video_task(self, strategy_id):
    """
    Belirtilen strateji ID'si için YouTube'a video yükler
    """
    try:
        from models import db, Strategy
        
        strategy = Strategy.query.get(strategy_id)
        if not strategy:
            logger.error(f"Strategy with ID {strategy_id} not found")
            return False
        
        logger.info(f"Starting video upload for strategy: {strategy.title}")
        
        # Video yolu kontrolü
        if not os.path.exists(strategy.video_path):
            logger.warning(f"Video file not found: {strategy.video_path}")
            # Demo için basit bir video dosyası oluştur
            demo_video_path = create_demo_video(strategy)
            strategy.video_path = demo_video_path
        
        # Durumu güncelle
        strategy.status = 'Yükleniyor'
        db.session.commit()
        
        # YouTube API ile video yükleme (şimdilik simulasyon)
        upload_result = simulate_youtube_upload(strategy)
        
        if upload_result['success']:
            strategy.status = 'Yayında'
            logger.info(f"Video uploaded successfully: {strategy.title}")
        else:
            strategy.status = 'Hata'
            logger.error(f"Video upload failed: {upload_result['error']}")
        
        db.session.commit()
        return upload_result['success']
        
    except Exception as e:
        logger.error(f"Error in upload_video_task: {str(e)}")
        if 'strategy' in locals():
            strategy.status = 'Hata'
            db.session.commit()
        return False

def create_demo_video(strategy):
    """
    Demo amaçlı basit video dosyası oluşturur
    """
    try:
        # Output klasörünü oluştur
        os.makedirs('/app/output', exist_ok=True)
        
        # Basit text-to-video (FFmpeg ile)
        output_path = f"/app/output/{strategy.id}_demo.mp4"
        
        # FFmpeg ile basit bir video oluştur (metin overlay ile)
        import subprocess
        
        cmd = [
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', f'color=c=blue:size=1280x720:duration=10',
            '-vf', f"drawtext=text='{strategy.title}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2",
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            logger.info(f"Demo video created: {output_path}")
            return output_path
        else:
            logger.error(f"FFmpeg error: {result.stderr}")
            return strategy.video_path
            
    except Exception as e:
        logger.error(f"Error creating demo video: {str(e)}")
        return strategy.video_path

def simulate_youtube_upload(strategy):
    """
    YouTube yükleme simulasyonu (gerçek API bağlantısı sonra eklenecek)
    """
    try:
        # Simulasyon: 5-10 saniye bekleme
        import random
        time.sleep(random.randint(5, 10))
        
        # %90 başarı oranı
        success = random.random() > 0.1
        
        if success:
            return {
                'success': True,
                'video_id': f'demo_{strategy.id}_{int(time.time())}',
                'url': f'https://youtube.com/watch?v=demo_{strategy.id}'
            }
        else:
            return {
                'success': False,
                'error': 'Simulated upload failure'
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# --- YENİ GÖREV 4: SPEECH-TO-TEXT İŞLEME ---
@celery_app.task
def transcribe_audio_task(audio_file_path, language='tr-TR'):
    """
    Ses dosyasını metne çevirir (CPU tabanlı, hafif)
    """
    try:
        logger.info(f"Transcribing audio file: {audio_file_path}")
        
        # Ses dosyasını WAV formatına çevir (eğer değilse)
        wav_path = convert_to_wav(audio_file_path)
        
        # SpeechRecognition ile transkripsiyon
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(wav_path) as source:
            # Gürültü filtreleme
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio_data = recognizer.record(source)
            
        # Google Speech Recognition kullan (ücretsiz, CPU tabanlı)
        try:
            # Türkçe için
            text = recognizer.recognize_google(audio_data, language=language)
            logger.info(f"Transcription successful: {text[:100]}...")
            
            # Geçici WAV dosyasını sil
            if wav_path != audio_file_path:
                os.remove(wav_path)
                
            return {
                'success': True,
                'text': text,
                'language': language
            }
            
        except sr.UnknownValueError:
            logger.warning("Speech Recognition could not understand audio")
            return {
                'success': False,
                'error': 'Could not understand audio'
            }
        except sr.RequestError as e:
            logger.error(f"Could not request results; {e}")
            return {
                'success': False,
                'error': f'Request error: {e}'
            }
            
    except Exception as e:
        logger.error(f"Error in transcribe_audio_task: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def convert_to_wav(audio_file_path):
    """
    Ses dosyasını WAV formatına çevirir
    """
    try:
        # Dosya uzantısını kontrol et
        if audio_file_path.lower().endswith('.wav'):
            return audio_file_path
            
        # pydub ile dönüştür
        audio = AudioSegment.from_file(audio_file_path)
        wav_path = audio_file_path.rsplit('.', 1)[0] + '_converted.wav'
        
        # Mono, 16kHz (speech recognition için optimal)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(wav_path, format="wav")
        
        logger.info(f"Audio converted to WAV: {wav_path}")
        return wav_path
        
    except Exception as e:
        logger.error(f"Error converting audio to WAV: {str(e)}")
        return audio_file_path

# --- GÖREV 5: VİDEODAN SES ÇIKARMA + TRANSKRİPSİYON ---
@celery_app.task
def extract_and_transcribe_task(video_file_path, language='tr-TR'):
    """
    Video dosyasından ses çıkarır ve metne çevirir
    """
    try:
        logger.info(f"Extracting audio from video: {video_file_path}")
        
        # Geçici ses dosyası yolu
        audio_file_path = video_file_path.rsplit('.', 1)[0] + '_audio.wav'
        
        # FFmpeg ile ses çıkar
        cmd = [
            'ffmpeg', '-y',
            '-i', video_file_path,
            '-vn',  # Video'yu dahil etme
            '-acodec', 'pcm_s16le',  # WAV codec
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',  # Mono
            audio_file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            logger.error(f"FFmpeg audio extraction failed: {result.stderr}")
            return {
                'success': False,
                'error': f'Audio extraction failed: {result.stderr}'
            }
        
        # Ses dosyasını transkribe et
        transcription_result = transcribe_audio_task.s(audio_file_path, language).apply().get()
        
        # Geçici ses dosyasını sil
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)
        
        return transcription_result
        
    except Exception as e:
        logger.error(f"Error in extract_and_transcribe_task: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


# --- ZAMANLAYICI ---
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Her gün sabah 8:00'da video oluştur (Türkiye saati)
    sender.add_periodic_task(
        crontab(hour=8, minute=0),  # Sabah 8:00'da çalış
        create_daily_strategy_task.s(channel_id=1, category='Bilim & Teknoloji', user_id=1),
        name='Her gün sabah 8:00da Bilim & Teknoloji videosu oluştur'
    )
    
    # Test için: Her 10 dakikada bir (geliştirme için)
    # sender.add_periodic_task(
    #     crontab(minute='*/10'),
    #     create_daily_strategy_task.s(channel_id=1, category='Test', user_id=1),
    #     name='Test: Her 10 dakikada bir video oluştur'
    # )
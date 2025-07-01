#!/usr/bin/env python3
"""
İlk kullanıcı ve kanal verilerini oluşturan script
Para kazanmaya hızlı başlamak için gerekli
"""
from app import create_app
from models import db, User, Channel

def setup_initial_data():
    app = create_app()
    
    with app.app_context():
        # Veritabanı tablolarını oluştur
        db.create_all()
        
        # Varsayılan kullanıcı oluştur
        existing_user = User.query.filter_by(username='admin').first()
        if not existing_user:
            user = User(username='admin')
            user.set_password('admin123')  # Güvenlik için sonra değiştirin!
            db.session.add(user)
            db.session.commit()
            print("✅ Varsayılan kullanıcı oluşturuldu: admin/admin123")
        else:
            user = existing_user
            print("ℹ️  Varsayılan kullanıcı zaten mevcut")
        
        # Varsayılan kanal oluştur
        existing_channel = Channel.query.filter_by(user_id=user.id).first()
        if not existing_channel:
            channel = Channel(
                name='Chimera Otomasyonu',
                youtube_channel_id='demo_channel_123',
                user_id=user.id
            )
            db.session.add(channel)
            db.session.commit()
            print("✅ Varsayılan kanal oluşturuldu: Chimera Otomasyonu")
        else:
            print("ℹ️  Varsayılan kanal zaten mevcut")
        
        print("\n🚀 Sistem hazır! Para kazanmaya başlayabilirsiniz!")
        print("📝 Giriş bilgileri: admin / admin123")
        print("🌐 Frontend: http://localhost:5173")
        print("📚 API Docs: http://localhost:5001")

if __name__ == '__main__':
    setup_initial_data()

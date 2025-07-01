#!/bin/bash
# Para kazanma sistemi hızlı başlatma scripti

echo "💰 YouTube Otomasyonu Para Kazanma Sistemi Başlatılıyor..."

# Eski container'ları temizle
echo "🧹 Eski container'lar temizleniyor..."
docker-compose down
docker container prune -f

# İmajları yeniden oluştur (requirements.txt değişti)
echo "🔨 Yeni Docker imajları oluşturuluyor..."
docker-compose build --no-cache

# Sistemi başlat
echo "🚀 Sistem başlatılıyor..."
docker-compose up -d

# Sistemin hazır olmasını bekle
echo "⏳ Sistem hazır olana kadar bekleniyor..."
sleep 10

# İlk verileri oluştur
echo "📋 İlk veriler oluşturuluyor..."
docker-compose exec backend python3 setup_initial_data.py

echo ""
echo "✅ SİSTEM HAZIR! PARA KAZANMAYA BAŞLAYABILIRSINIZ!"
echo ""
echo "🌐 Frontend: http://localhost:5173"
echo "📚 API Docs: http://localhost:5001"
echo "📝 Giriş: admin / admin123"
echo ""
echo "💡 Hızlı başlatmak için Dashboard'daki 'Hızlı Video Başlat' butonunu kullanın!"
echo ""

# Sistem durumunu göster
echo "📊 Container durumu:"
docker-compose ps

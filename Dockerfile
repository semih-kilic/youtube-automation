# Python'un hafif bir versiyonunu temel alıyoruz
FROM python:3.11-slim

# Çalışma dizinini /app olarak ayarlıyoruz
WORKDIR /app

# Sistem bağımlılıklarını kuruyoruz (FFmpeg, Whisper için)
RUN apt-get update && apt-get install -y ffmpeg libass-dev && rm -rf /var/lib/apt/lists/*

# Önce bağımlılık listesini kopyalayıp kuruyoruz. Bu, build sürecini hızlandırır.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Projenin geri kalan tüm dosyalarını kopyalıyoruz
COPY . .

# Flask uygulamasının çalışacağı portu belirtiyoruz
EXPOSE 5000

# Konteyner başladığında çalıştırılacak komut
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--forwarded-allow-ips=*", "app:app"]
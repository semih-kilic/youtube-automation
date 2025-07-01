# /home/semih/youtube-automation/app.py - NİHAİ VE TAM KOD
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from api import auth_ns, health_ns
from strategy_api import strategy_ns
from channel_api import channel_ns

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt = JWTManager(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'https://benimotomasyonum.com')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # --- DOKÜMANTASYONU GERİ GETİREN DEĞİŞİKLİK ---
    # API'yi 'doc' parametresiyle başlatıyoruz.
    api = Api(app,
              version='1.0',
              title='Chimera API',
              description='API for YouTube Automation Factory',
              doc='/') # <-- Ana dizini dokümantasyon sayfası yap
    # ---------------------------------------------

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(health_ns, path='/health')
    api.add_namespace(strategy_ns, path='/strategies')
    api.add_namespace(channel_ns, path='/channels')

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
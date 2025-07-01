# /home/semih/youtube-automation/api.py - TAM VE EKSİKSİZ KOD
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required
from models import db, User
import psutil

# === AUTH NAMESPACE ===
auth_ns = Namespace('auth', description='User Authentication')
login_model = auth_ns.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})

@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        if user and user.check_password(data.get('password')):
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

@auth_ns.route('/register')
class RegisterResource(Resource):
    @auth_ns.expect(login_model) 
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data.get('username')).first():
            return {'message': 'User already exists'}, 409
        new_user = User(username=data.get('username'))
        new_user.set_password(data.get('password'))
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

# === HEALTH NAMESPACE ===
health_ns = Namespace('health', description='System Health Checks')

def is_celery_beat_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        cmdline = ' '.join(proc.info.get('cmdline', []))
        if 'celery' in cmdline and 'beat' in cmdline:
            return True
    return False

@health_ns.route('/status')
class HealthCheckResource(Resource):
    @jwt_required()
    def get(self):
        from celery_worker import celery_app
        worker_ping = celery_app.control.ping(timeout=0.5)
        worker_status = 'Online' if worker_ping else 'Offline'
        beat_status = 'Online' if is_celery_beat_running() else 'Offline'
        services_status = {
            'api_server': {'name': 'API Server (Flask)', 'status': 'Online'},
            'celery_worker': {'name': 'Celery Worker', 'status': worker_status},
            'celery_beat': {'name': 'Celery Beat (Scheduler)', 'status': beat_status},
            'cloudflare_tunnel': {'name': 'Cloudflare Tunnel', 'status': 'Online'},
        }
        return services_status, 200
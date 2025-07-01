# /home/semih/youtube-automation/strategy_api.py - TAM KODU
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Strategy

strategy_ns = Namespace('strategies', description='Strategy operations')

strategy_input_model = strategy_ns.model('StrategyInput', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'video_path': fields.String(required=True),
    'category': fields.String(),
    'channel_id': fields.Integer(required=True),
})

@strategy_ns.route('/')
class StrategyList(Resource):
    @jwt_required()
    def get(self):
        """List all strategies for the current user"""
        user_id = get_jwt_identity()
        strategies = Strategy.query.filter_by(user_id=user_id).order_by(Strategy.created_at.desc()).all()
        output = []
        for s in strategies:
            output.append({
                'id': s.id,
                'title': s.title,
                'description': s.description,
                'video_path': s.video_path,
                'category': s.category,
                'status': s.status,
                'created_at': s.created_at.isoformat(),
                'channel': {
                    'id': s.channel.id,
                    'name': s.channel.name
                } if s.channel else None
            })
        return jsonify(output)
    
    @jwt_required()
    @strategy_ns.expect(strategy_input_model)
    def post(self):
        """Create a new strategy and trigger the upload task"""
        from celery_worker import upload_video_task
        user_id = get_jwt_identity()
        data = strategy_ns.payload
        new_strategy = Strategy(
            title=data['title'],
            description=data.get('description'),
            video_path=data['video_path'],
            category=data.get('category'),
            channel_id=data['channel_id'],
            user_id=user_id
        )
        db.session.add(new_strategy)
        db.session.commit()
        upload_video_task.delay(new_strategy.id)
        return {'message': 'Strategy created and task started.', 'strategy_id': new_strategy.id}, 201
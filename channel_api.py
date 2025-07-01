# /home/semih/youtube-automation/channel_api.py - TAM KODU
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Channel

channel_ns = Namespace('channels', description='Channel management operations')

channel_input_model = channel_ns.model('ChannelInput', {
    'name': fields.String(required=True, description='Your custom name for the channel'),
    'youtube_channel_id': fields.String(required=True, description='The actual YouTube channel ID'),
})

@channel_ns.route('/')
class ChannelList(Resource):
    @jwt_required()
    def get(self):
        """List all channels for the current user"""
        user_id = get_jwt_identity()
        channels = Channel.query.filter_by(user_id=user_id).all()
        output = [{'id': c.id, 'name': c.name, 'youtube_channel_id': c.youtube_channel_id} for c in channels]
        return jsonify(output)

    @jwt_required()
    @channel_ns.expect(channel_input_model)
    def post(self):
        """Add a new channel"""
        user_id = get_jwt_identity()
        data = channel_ns.payload
        new_channel = Channel(name=data['name'], youtube_channel_id=data['youtube_channel_id'], user_id=user_id)
        db.session.add(new_channel)
        db.session.commit()
        return jsonify({'id': new_channel.id, 'name': new_channel.name, 'youtube_channel_id': new_channel.youtube_channel_id}), 201
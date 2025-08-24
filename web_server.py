import os
import asyncio
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request
from livekit import api
from livekit.api import AccessToken, VideoGrants
import jwt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

# LiveKit configuration from environment variables
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "APITMKfqYVjk79h")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "gCkm5chxksS9KKIUrWVDhf7TDVRVeqleZHf49SFPLBMA")  
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://sr-fa31r2za.livekit.cloud")

# Default room name for Alex agent
DEFAULT_ROOM_NAME = "alex-voice-chat"


@app.route('/')
def index():
    """Serve the main web interface"""
    try:
        # Try to serve from static folder first
        with open('static/index.html', 'r') as f:
            return render_template_string(f.read())
    except FileNotFoundError:
        # Fall back to root directory for Render deployment
        with open('index.html', 'r') as f:
            return render_template_string(f.read())


@app.route('/api/token')
def get_token():
    """Generate a LiveKit access token for the user"""
    try:
        # Get participant identity from query params or generate one
        identity = request.args.get('identity', f'user_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        # Generate unique private room for each user (no shared rooms)
        room_name = request.args.get('room', f'alex-private-{identity}')
        
        # Create access token
        token = AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        token.with_identity(identity)
        token.with_name(identity)
        
        # Grant permissions for audio communication
        grant = VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
            can_publish_data=True,
        )
        token.with_grants(grant)
        
        # Token expires in 6 hours
        token.with_ttl(timedelta(hours=6))
        
        jwt_token = token.to_jwt()
        
        logger.info(f"Generated token for {identity} in room {room_name}")
        
        return jsonify({
            'token': jwt_token,
            'url': LIVEKIT_URL,
            'room': room_name,
            'identity': identity
        })
        
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        return jsonify({'error': 'Failed to generate token'}), 500


@app.route('/api/create-room')
def create_room():
    """Create a new LiveKit room for the Alex agent"""
    try:
        # For now, just return success - room creation will happen automatically
        # when users connect. This simplifies the setup.
        logger.info(f"Room endpoint called for: {DEFAULT_ROOM_NAME}")
        
        return jsonify({
            'room': DEFAULT_ROOM_NAME,
            'created': True
        })
        
    except Exception as e:
        logger.error(f"Error with room endpoint: {e}")
        return jsonify({'error': 'Failed to create room', 'room': DEFAULT_ROOM_NAME}), 200


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'alex-voice-agent',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    logger.info("Starting Alex Voice Agent Web Server...")
    logger.info(f"LiveKit URL: {LIVEKIT_URL}")
    logger.info(f"Default Room: {DEFAULT_ROOM_NAME}")
    
    # Get port from environment variable for Render compatibility
    port = int(os.getenv("PORT", 5000))
    
    # Run the Flask application
    app.run(host='0.0.0.0', port=port, debug=False)

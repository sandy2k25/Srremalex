import os
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request
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
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alex - Stremini AI Voice Assistant</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <div class="status-bar">
            <div class="connection-status" id="connectionStatus">
                <span class="status-dot"></span>
                <span class="status-text">Connecting...</span>
            </div>
        </div>

        <div class="main-content">
            <div class="header">
                <h1>Alex</h1>
                <p class="subtitle">AI Voice Agent of<br>Stremini AI</p>
                <p class="creator">Created by Sandy</p>
            </div>

            <div class="avatar-container">
                <div class="avatar-circle" id="avatarCircle">
                    <img src="{{ url_for('static', filename='stremini-logo.png') }}" alt="Stremini AI" class="avatar-logo" id="avatarLogo">
                </div>
                <div class="audio-visualizer" id="audioVisualizer"></div>
            </div>

            <div class="controls">
                <button class="control-btn" id="connectBtn">
                    <span class="btn-icon">🎤</span>
                    <span class="btn-text">Start Conversation</span>
                </button>
                
                <div class="secondary-controls" id="secondaryControls" style="display: none;">
                    <button class="control-btn secondary" id="micBtn">
                        <span class="btn-icon">🎤</span>
                        <span class="btn-text">Microphone</span>
                    </button>
                    <button class="control-btn secondary" id="speakerBtn">
                        <span class="btn-icon">🔊</span>
                        <span class="btn-text">Speaker</span>
                    </button>
                    <button class="control-btn danger" id="disconnectBtn">
                        <span class="btn-icon">❌</span>
                        <span class="btn-text">End Chat</span>
                    </button>
                </div>
            </div>

            <div class="info-panel">
                <div class="info-item">
                    <span class="info-label">Status:</span>
                    <span class="info-value" id="statusText">Ready to connect</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Room:</span>
                    <span class="info-value" id="roomText">Not connected</span>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>Powered by <a href="https://stremini.site" target="_blank" rel="noopener">Stremini.site</a></p>
            <p>Real-time voice conversations with Alex</p>
        </div>
    </div>

    <script src="{{ url_for('static', filename='livekit-client.umd.min.js') }}"></script>
    <script src="{{ url_for('static', filename='app.js') }}"></script>
</body>
</html>
    """
    return render_template_string(html_content)

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
    logger.info("Starting Alex Voice Agent Web Server on Docker...")
    logger.info(f"LiveKit URL: {LIVEKIT_URL}")
    logger.info(f"Default Room: {DEFAULT_ROOM_NAME}")
    
    # Run the Flask application (port 7860 for HF Spaces)
    app.run(host='0.0.0.0', port=7860, debug=False)
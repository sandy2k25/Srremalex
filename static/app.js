class AlexVoiceAgent {
    constructor() {
        this.room = null;
        this.localParticipant = null;
        this.isConnected = false;
        this.isMuted = false;
        this.isSpeakerEnabled = true;
        
        this.initializeElements();
        this.setupEventListeners();
    }

    initializeElements() {
        this.connectBtn = document.getElementById('connectBtn');
        this.micBtn = document.getElementById('micBtn');
        this.speakerBtn = document.getElementById('speakerBtn');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.statusText = document.getElementById('statusText');
        this.avatar = document.getElementById('avatar');
        this.audioVisualizer = document.getElementById('audioVisualizer');
        this.conversationInfo = document.getElementById('conversationInfo');
        this.chatTranscript = document.getElementById('chatTranscript');
        this.messages = document.getElementById('messages');
        this.remoteAudio = document.getElementById('remoteAudio');
    }

    setupEventListeners() {
        this.connectBtn.addEventListener('click', () => this.toggleConnection());
        this.micBtn.addEventListener('click', () => this.toggleMicrophone());
        this.speakerBtn.addEventListener('click', () => this.toggleSpeaker());
    }

    async toggleConnection() {
        if (this.isConnected) {
            await this.disconnect();
        } else {
            await this.connect();
        }
    }

    async connect() {
        let url = null;
        let token = null;
        
        try {
            this.updateStatus('Connecting...', false);
            this.connectBtn.disabled = true;

            // Wait for LiveKit library to be available
            if (!window.liveKitLoaded || typeof LiveKit === 'undefined') {
                this.updateStatus('Loading LiveKit library...', false);
                await this.waitForLiveKit();
            }

            // Get access token from server
            const tokenResponse = await fetch('/api/token');
            if (!tokenResponse.ok) {
                throw new Error('Failed to get access token');
            }

            const tokenData = await tokenResponse.json();
            token = tokenData.token;
            url = tokenData.url;
            const room = tokenData.room;
            const identity = tokenData.identity;

            // Initialize LiveKit room
            this.room = new LiveKit.Room({
                adaptiveStream: true,
                dynacast: true,
                publishDefaults: {
                    videoSimulcastLayers: [],
                },
            });

            // Set up room event listeners
            this.setupRoomEventListeners();

            console.log('Connecting to LiveKit with:', { url, identity, room });
            
            // Connect to the room
            await this.room.connect(url, token, {
                autoSubscribe: true,
            });
            
            // Enable microphone by default
            await this.enableMicrophone();
            
            this.isConnected = true;
            this.updateStatus('Connected to Alex', true);
            this.updateUI();
            
            console.log('Connected to room:', room);
            this.addMessage('System', 'Connected to Alex! Start speaking to begin your conversation.');

        } catch (error) {
            console.error('Connection failed:', error);
            console.error('Error details:', {
                name: error.name,
                message: error.message,
                code: error.code,
                reason: error.reason,
                stack: error.stack,
                url: url || 'URL not available',
                token: token ? 'Token received' : 'No token',
                errorType: typeof error,
                errorConstructor: error.constructor.name
            });
            
            let errorMessage = 'Unknown connection error';
            if (error.message) {
                errorMessage = error.message;
            } else if (error.reason) {
                errorMessage = error.reason;
            } else if (error.code) {
                errorMessage = `Error code: ${error.code}`;
            }
            
            this.updateStatus(`Connection failed: ${errorMessage}`, false);
            this.addMessage('System', `Connection failed: ${errorMessage}`);
        } finally {
            this.connectBtn.disabled = false;
        }
    }

    async disconnect() {
        try {
            this.updateStatus('Disconnecting...', false);
            
            if (this.room) {
                await this.room.disconnect();
                this.room = null;
            }
            
            this.isConnected = false;
            this.updateStatus('Disconnected', false);
            this.updateUI();
            this.addMessage('System', 'Disconnected from Alex.');
            
        } catch (error) {
            console.error('Disconnect error:', error);
        }
    }

    setupRoomEventListeners() {
        this.room.on('connected', () => {
            console.log('Room connected');
            this.localParticipant = this.room.localParticipant;
        });

        this.room.on('disconnected', () => {
            console.log('Room disconnected');
            this.isConnected = false;
            this.updateStatus('Disconnected', false);
            this.updateUI();
        });

        this.room.on('trackSubscribed', (track, publication, participant) => {
            console.log('Track subscribed:', track.kind, participant.identity);
            
            if (track.kind === 'audio') {
                // Alex's voice - attach to audio element
                const audioElement = track.attach();
                audioElement.autoplay = true;
                document.body.appendChild(audioElement);
                
                // Show that Alex is speaking
                this.showAlexSpeaking(true);
                
                // Hide speaking indicator when audio ends
                track.on('ended', () => {
                    this.showAlexSpeaking(false);
                });
            }
        });

        this.room.on('trackUnsubscribed', (track, publication, participant) => {
            console.log('Track unsubscribed:', track.kind, participant.identity);
            track.detach();
            this.showAlexSpeaking(false);
        });

        this.room.on('participantConnected', (participant) => {
            console.log('Participant connected:', participant.identity);
            if (participant.identity.includes('alex') || participant.identity.includes('agent')) {
                this.addMessage('System', 'Alex joined the conversation!');
            }
        });

        this.room.on('participantDisconnected', (participant) => {
            console.log('Participant disconnected:', participant.identity);
            if (participant.identity.includes('alex') || participant.identity.includes('agent')) {
                this.addMessage('System', 'Alex left the conversation.');
            }
        });

        // Handle audio level changes for visualization
        this.room.on('localTrackPublished', (publication, participant) => {
            if (publication.track && publication.track.kind === 'audio') {
                this.setupAudioLevelMonitoring(publication.track);
            }
        });
    }

    setupAudioLevelMonitoring(track) {
        // Monitor audio levels for visualization
        if (track.source === 'microphone') {
            // This would typically require additional audio processing
            // For now, we'll simulate based on speaking state
            this.startAudioVisualization();
        }
    }

    startAudioVisualization() {
        // Simple audio visualization simulation
        let isAnimating = false;
        
        const animate = () => {
            if (!this.isConnected) return;
            
            // Randomly animate bars to simulate audio levels
            const bars = this.audioVisualizer.querySelectorAll('.bar');
            bars.forEach(bar => {
                const height = Math.random() * 20 + 5;
                bar.style.height = `${height}px`;
            });
            
            if (isAnimating) {
                requestAnimationFrame(animate);
            }
        };

        // Start animation when speaking
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && this.isConnected && !isAnimating) {
                isAnimating = true;
                this.audioVisualizer.classList.add('active');
                animate();
            }
        });

        document.addEventListener('keyup', (e) => {
            if (e.code === 'Space') {
                isAnimating = false;
                this.audioVisualizer.classList.remove('active');
            }
        });
    }

    async enableMicrophone() {
        try {
            await this.room.localParticipant.setMicrophoneEnabled(true);
            this.isMuted = false;
            this.micBtn.classList.add('active');
            console.log('Microphone enabled');
        } catch (error) {
            console.error('Failed to enable microphone:', error);
            this.addMessage('System', 'Failed to access microphone. Please check your permissions.');
        }
    }

    async toggleMicrophone() {
        if (!this.isConnected) return;

        try {
            const enabled = !this.isMuted;
            await this.room.localParticipant.setMicrophoneEnabled(enabled);
            this.isMuted = !enabled;
            
            if (enabled) {
                this.micBtn.classList.add('active');
                this.micBtn.innerHTML = '<i class="fas fa-microphone"></i> Microphone';
                this.addMessage('System', 'Microphone enabled');
            } else {
                this.micBtn.classList.remove('active');
                this.micBtn.innerHTML = '<i class="fas fa-microphone-slash"></i> Muted';
                this.addMessage('System', 'Microphone muted');
            }
        } catch (error) {
            console.error('Failed to toggle microphone:', error);
        }
    }

    toggleSpeaker() {
        this.isSpeakerEnabled = !this.isSpeakerEnabled;
        
        // Mute/unmute all remote audio elements
        const audioElements = document.querySelectorAll('audio');
        audioElements.forEach(audio => {
            audio.muted = !this.isSpeakerEnabled;
        });

        if (this.isSpeakerEnabled) {
            this.speakerBtn.classList.add('active');
            this.speakerBtn.innerHTML = '<i class="fas fa-volume-up"></i> Speaker';
        } else {
            this.speakerBtn.classList.remove('active');
            this.speakerBtn.innerHTML = '<i class="fas fa-volume-mute"></i> Muted';
        }
    }

    showAlexSpeaking(isSpeaking) {
        if (isSpeaking) {
            this.avatar.classList.add('talking');
            this.audioVisualizer.classList.add('active');
        } else {
            this.avatar.classList.remove('talking');
            this.audioVisualizer.classList.remove('active');
        }
    }

    updateStatus(text, isConnected) {
        this.statusText.textContent = text;
        if (isConnected) {
            this.statusIndicator.classList.add('connected');
        } else {
            this.statusIndicator.classList.remove('connected');
        }
    }

    async waitForLiveKit() {
        return new Promise((resolve, reject) => {
            // If LiveKit is already loaded, resolve immediately
            if (window.liveKitLoaded && typeof LiveKit !== 'undefined') {
                console.log('LiveKit library is already available');
                resolve();
                return;
            }
            
            // Add callback to be notified when LiveKit loads
            window.liveKitCallbacks.push(resolve);
            
            // Set a timeout as backup
            setTimeout(() => {
                if (!window.liveKitLoaded) {
                    reject(new Error('LiveKit library failed to load within timeout'));
                }
            }, 15000); // 15 second timeout
        });
    }

    updateUI() {
        if (this.isConnected) {
            this.connectBtn.innerHTML = '<i class="fas fa-phone-slash"></i> Disconnect';
            this.connectBtn.className = 'btn btn-danger';
            this.micBtn.disabled = false;
            this.speakerBtn.disabled = false;
            this.conversationInfo.style.display = 'none';
            this.chatTranscript.style.display = 'block';
        } else {
            this.connectBtn.innerHTML = '<i class="fas fa-phone"></i> Connect to Alex';
            this.connectBtn.className = 'btn btn-primary';
            this.micBtn.disabled = true;
            this.speakerBtn.disabled = true;
            this.micBtn.classList.remove('active');
            this.speakerBtn.classList.add('active');
            this.conversationInfo.style.display = 'block';
            // Don't hide transcript to preserve conversation history
        }
    }

    addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender.toLowerCase()}`;
        
        const senderSpan = document.createElement('div');
        senderSpan.className = 'sender';
        senderSpan.textContent = sender;
        
        const textDiv = document.createElement('div');
        textDiv.textContent = text;
        
        messageDiv.appendChild(senderSpan);
        messageDiv.appendChild(textDiv);
        
        this.messages.appendChild(messageDiv);
        this.messages.scrollTop = this.messages.scrollHeight;
    }
}

// Initialize the Alex Voice Agent when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.alexAgent = new AlexVoiceAgent();
    
    // Add some helpful instructions
    const instructions = document.createElement('div');
    instructions.className = 'instructions';
    instructions.innerHTML = `
        <p><strong>How to use:</strong></p>
        <ul>
            <li>Click "Connect to Alex" to join the voice conversation</li>
            <li>Speak naturally - Alex will hear you and respond</li>
            <li>Use the microphone button to mute/unmute yourself</li>
            <li>Use the speaker button to control Alex's audio</li>
        </ul>
    `;
    
    // Add instructions to conversation info
    const conversationInfo = document.getElementById('conversationInfo');
    conversationInfo.appendChild(instructions);
});

// Add some CSS for instructions
const style = document.createElement('style');
style.textContent = `
    .btn-danger {
        background: linear-gradient(135deg, #dc3545, #c82333);
        color: white;
    }
    
    .btn-danger:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(220, 53, 69, 0.4);
    }
    
    .instructions {
        margin-top: 20px;
        padding: 20px;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 15px;
        text-align: left;
    }
    
    .instructions ul {
        margin-top: 10px;
        padding-left: 20px;
    }
    
    .instructions li {
        margin-bottom: 5px;
        color: #666;
    }
`;
document.head.appendChild(style);

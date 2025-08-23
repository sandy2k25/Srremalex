class AlexVoiceAgent {
    constructor() {
        this.room = null;
        this.localParticipant = null;
        this.isConnected = false;
        this.isMuted = false;
        this.isSpeakerEnabled = true;
        this.isAlexSpeaking = false;
        this.isUserSpeaking = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.initializeUI();
    }

    initializeElements() {
        this.connectBtn = document.getElementById('connectBtn');
        this.micBtn = document.getElementById('micBtn');
        this.speakerBtn = document.getElementById('speakerBtn');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.statusText = document.getElementById('statusText');
        this.avatar = document.getElementById('avatar');
        this.avatarRing = document.getElementById('avatarRing');
        this.pulseRing = document.getElementById('pulseRing');
        this.audioVisualizer = document.getElementById('audioVisualizer');
        this.agentStatusText = document.getElementById('agentStatusText');
        this.agentSubtitle = document.getElementById('agentSubtitle');
        this.conversationInfo = document.getElementById('conversationInfo');
        this.chatTranscript = document.getElementById('chatTranscript');
        this.messages = document.getElementById('messages');
        this.remoteAudio = document.getElementById('remoteAudio');
    }

    initializeUI() {
        // Set initial UI state
        this.updateAgentStatus('Ready to chat', 'Click to start conversation with Alex');
        this.speakerBtn.classList.add('active'); // Speaker enabled by default
    }

    setupEventListeners() {
        this.connectBtn.addEventListener('click', () => this.toggleConnection());
        this.micBtn.addEventListener('click', () => this.toggleMicrophone());
        this.speakerBtn.addEventListener('click', () => this.toggleSpeaker());
        
        // Avatar click to connect/disconnect
        this.avatar.addEventListener('click', () => this.toggleConnection());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && this.isConnected) {
                e.preventDefault();
                this.handleSpacePress(true);
            }
        });
        
        document.addEventListener('keyup', (e) => {
            if (e.code === 'Space' && this.isConnected) {
                e.preventDefault();
                this.handleSpacePress(false);
            }
        });
    }

    handleSpacePress(isPressed) {
        if (isPressed && !this.isUserSpeaking) {
            this.setUserSpeaking(true);
        } else if (!isPressed && this.isUserSpeaking) {
            this.setUserSpeaking(false);
        }
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
            this.updateAgentStatus('Connecting...', 'Establishing connection to Alex');
            this.connectBtn.disabled = true;

            // Wait for LiveKit library to be available
            if (!window.liveKitLoaded || typeof LiveKit === 'undefined') {
                this.updateStatus('Loading libraries...', false);
                this.updateAgentStatus('Loading...', 'Preparing voice system');
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
            try {
                await this.enableMicrophone();
            } catch (micError) {
                console.warn('Initial microphone setup failed:', micError);
                this.addMessage('System', '⚠️ Please click the microphone button to enable voice chat');
            }
            
            this.isConnected = true;
            this.updateStatus('Connected', true);
            this.updateAgentStatus('Connected', 'Alex is listening and ready to chat');
            this.updateUI();
            
            console.log('Connected to room:', room);
            this.addMessage('System', 'Connected to Alex! Start speaking naturally.');

        } catch (error) {
            console.error('Connection failed:', error);
            
            let errorMessage = 'Connection failed';
            if (error.message) {
                errorMessage = error.message;
            }
            
            this.updateStatus(errorMessage, false);
            this.updateAgentStatus('Connection failed', 'Please try again');
            this.addMessage('System', `Connection failed: ${errorMessage}`);
        } finally {
            this.connectBtn.disabled = false;
        }
    }

    async disconnect() {
        try {
            this.updateStatus('Disconnecting...', false);
            this.updateAgentStatus('Disconnecting...', 'Ending conversation');
            
            if (this.room) {
                await this.room.disconnect();
                this.room = null;
            }
            
            this.isConnected = false;
            this.setAlexSpeaking(false);
            this.setUserSpeaking(false);
            this.updateStatus('Disconnected', false);
            this.updateAgentStatus('Ready to chat', 'Click to start conversation with Alex');
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
            this.updateAgentStatus('Ready to chat', 'Click to start conversation with Alex');
            this.updateUI();
        });

        this.room.on('trackSubscribed', (track, publication, participant) => {
            console.log('Track subscribed:', track.kind, participant.identity);
            
            if (track.kind === 'audio') {
                // Alex's voice - attach to audio element
                const audioElement = track.attach();
                audioElement.autoplay = true;
                document.body.appendChild(audioElement);
                
                // Show Alex is speaking
                this.setAlexSpeaking(true);
                this.updateAgentStatus('Speaking', 'Alex is responding');
                
                // Monitor audio events
                audioElement.addEventListener('play', () => {
                    this.setAlexSpeaking(true);
                });
                
                audioElement.addEventListener('pause', () => {
                    this.setAlexSpeaking(false);
                });
                
                audioElement.addEventListener('ended', () => {
                    this.setAlexSpeaking(false);
                    this.updateAgentStatus('Listening', 'Waiting for your voice');
                });
                
                // Hide speaking indicator when track ends
                track.on('ended', () => {
                    this.setAlexSpeaking(false);
                    this.updateAgentStatus('Listening', 'Waiting for your voice');
                });
            }
        });

        this.room.on('trackUnsubscribed', (track, publication, participant) => {
            console.log('Track unsubscribed:', track.kind, participant.identity);
            track.detach();
            this.setAlexSpeaking(false);
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

        // Handle local audio
        this.room.on('localTrackPublished', (publication, participant) => {
            if (publication.track && publication.track.kind === 'audio') {
                this.setupAudioLevelMonitoring(publication.track);
            }
        });
    }

    setupAudioLevelMonitoring(track) {
        // Monitor microphone activity
        if (track.source === 'microphone') {
            console.log('Setting up audio monitoring for microphone');
        }
    }

    async enableMicrophone() {
        try {
            this.addMessage('System', 'Requesting microphone access...');
            
            // Request microphone permission
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                } 
            });
            console.log('Got microphone permission');
            
            // Stop the test stream
            stream.getTracks().forEach(track => track.stop());
            
            // Enable microphone through LiveKit
            await this.room.localParticipant.setMicrophoneEnabled(true);
            this.isMuted = false;
            this.micBtn.classList.add('active');
            this.micBtn.classList.remove('muted');
            console.log('Microphone enabled successfully');
            this.addMessage('System', '✓ Microphone enabled! Alex can now hear you.');
        } catch (error) {
            console.error('Failed to enable microphone:', error);
            
            if (error.name === 'NotAllowedError') {
                this.addMessage('System', '🎤 Please allow microphone access for voice chat with Alex');
            } else if (error.name === 'NotFoundError') {
                this.addMessage('System', '🎤 No microphone found. Please connect a microphone.');
            } else {
                this.addMessage('System', '🎤 Microphone access failed. Please check permissions.');
            }
            
            this.isMuted = true;
            this.micBtn.classList.remove('active');
            this.micBtn.classList.add('muted');
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
                this.micBtn.classList.remove('muted');
                this.addMessage('System', 'Microphone enabled');
            } else {
                this.micBtn.classList.remove('active');
                this.micBtn.classList.add('muted');
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
            this.speakerBtn.classList.remove('muted');
        } else {
            this.speakerBtn.classList.remove('active');
            this.speakerBtn.classList.add('muted');
        }
    }

    setAlexSpeaking(isSpeaking) {
        this.isAlexSpeaking = isSpeaking;
        
        if (isSpeaking) {
            this.avatar.classList.add('speaking');
            this.avatar.classList.remove('listening');
            this.audioVisualizer.classList.add('active');
        } else {
            this.avatar.classList.remove('speaking');
            if (this.isConnected) {
                this.avatar.classList.add('listening');
            }
            this.audioVisualizer.classList.remove('active');
        }
    }

    setUserSpeaking(isSpeaking) {
        this.isUserSpeaking = isSpeaking;
        
        if (isSpeaking) {
            this.updateAgentStatus('Listening', 'Processing your voice');
            this.audioVisualizer.classList.add('active');
        } else {
            if (!this.isAlexSpeaking) {
                this.updateAgentStatus('Thinking', 'Preparing response');
                this.audioVisualizer.classList.remove('active');
            }
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

    updateAgentStatus(title, subtitle) {
        this.agentStatusText.textContent = title;
        this.agentSubtitle.textContent = subtitle;
    }

    async waitForLiveKit() {
        return new Promise((resolve, reject) => {
            if (window.liveKitLoaded && typeof LiveKit !== 'undefined') {
                console.log('LiveKit library is already available');
                resolve();
                return;
            }
            
            window.liveKitCallbacks.push(resolve);
            
            setTimeout(() => {
                if (!window.liveKitLoaded) {
                    reject(new Error('LiveKit library failed to load'));
                }
            }, 15000);
        });
    }

    updateUI() {
        if (this.isConnected) {
            this.connectBtn.innerHTML = '<i class="fas fa-stop"></i><span>End Conversation</span>';
            this.connectBtn.classList.add('disconnect');
            this.micBtn.disabled = false;
            this.speakerBtn.disabled = false;
            this.conversationInfo.style.display = 'none';
            this.chatTranscript.style.display = 'block';
            this.avatar.classList.add('listening');
        } else {
            this.connectBtn.innerHTML = '<i class="fas fa-play"></i><span>Start Conversation</span>';
            this.connectBtn.classList.remove('disconnect');
            this.micBtn.disabled = true;
            this.speakerBtn.disabled = true;
            this.micBtn.classList.remove('active', 'muted');
            this.conversationInfo.style.display = 'block';
            this.avatar.classList.remove('speaking', 'listening');
        }
    }

    addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender.toLowerCase()}`;
        
        if (sender !== 'System') {
            const senderSpan = document.createElement('div');
            senderSpan.className = 'sender';
            senderSpan.textContent = sender;
            messageDiv.appendChild(senderSpan);
        }
        
        const textDiv = document.createElement('div');
        textDiv.textContent = text;
        messageDiv.appendChild(textDiv);
        
        this.messages.appendChild(messageDiv);
        this.messages.scrollTop = this.messages.scrollHeight;
    }
}

// Initialize the Alex Voice Agent when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.alexAgent = new AlexVoiceAgent();
    
    console.log('Alex Voice Agent initialized - ElevenLabs style UI ready');
});
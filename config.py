import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentConfig:
    """Configuration for Alex voice agent"""
    
    # LiveKit configuration
    livekit_url: str = os.getenv("LIVEKIT_URL", "ws://localhost:7880")
    livekit_api_key: str = os.getenv("LIVEKIT_API_KEY", "devkey")
    livekit_api_secret: str = os.getenv("LIVEKIT_API_SECRET", "secret")
    
    # AI Service API Keys
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    deepgram_api_key: Optional[str] = os.getenv("DEEPGRAM_API_KEY")
    elevenlabs_api_key: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
    
    # Agent settings
    room_name: str = "alex-voice-chat"
    agent_name: str = "Alex"
    
    # Voice settings
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.7
    
    # STT settings
    stt_model: str = "nova-2-general"  # Deepgram model
    stt_language: str = "en"
    
    # TTS settings
    elevenlabs_voice: str = "Rachel"  # Warm, friendly voice
    elevenlabs_model: str = "eleven_turbo_v2_5"
    openai_voice: str = "nova"  # Fallback for OpenAI TTS
    
    # Room settings
    empty_timeout: int = 300  # 5 minutes
    max_participants: int = 10
    
    def validate(self) -> bool:
        """Validate essential configuration"""
        if not self.openai_api_key:
            print("Warning: OPENAI_API_KEY not set. Agent functionality will be limited.")
            return False
        return True

    def get_voice_config(self) -> dict:
        """Get voice processing configuration"""
        config = {
            'llm': {
                'model': self.llm_model,
                'temperature': self.llm_temperature,
            },
            'stt': {
                'language': self.stt_language,
            },
            'tts': {},
        }
        
        # Configure STT based on available API keys
        if self.deepgram_api_key:
            config['stt']['provider'] = 'deepgram'
            config['stt']['model'] = self.stt_model
        else:
            config['stt']['provider'] = 'openai'
            
        # Configure TTS based on available API keys  
        if self.elevenlabs_api_key:
            config['tts']['provider'] = 'elevenlabs'
            config['tts']['voice'] = self.elevenlabs_voice
            config['tts']['model'] = self.elevenlabs_model
        else:
            config['tts']['provider'] = 'openai'
            config['tts']['voice'] = self.openai_voice
            
        return config

# Global configuration instance
config = AgentConfig()

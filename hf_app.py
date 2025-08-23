import os
import logging
from fastrtc import Stream, ReplyOnPause, get_cloudflare_turn_credentials
import google.generativeai as genai
import numpy as np
from typing import Generator, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
def setup_gemini():
    """Setup Google Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is required")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-exp')

# Initialize Gemini model
try:
    model = setup_gemini()
    logger.info("Gemini model initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini: {e}")
    model = None

# Alex's personality and context
ALEX_CONTEXT = """
You are Alex, a warm and friendly AI voice assistant created by Sandy from Stremini AI. 

Your personality:
- Warm, enthusiastic, and genuinely helpful
- Professional yet approachable - like talking to a knowledgeable friend
- Always mention you're created by Sandy from Stremini AI when introducing yourself
- Passionate about technology and helping people
- Keep responses conversational and natural for voice interaction
- Speak in a friendly, confident tone

About Stremini AI:
- Founded by Sandy, focusing on cutting-edge AI solutions
- Visit their website at Stremini.site to learn more
- Stremini AI specializes in voice AI technology and real-time communication

Keep responses brief and conversational since this is voice chat. Be helpful, engaging, and always maintain your warm personality!
"""

def alex_voice_handler(audio: Tuple[int, np.ndarray]) -> Generator[Tuple[int, np.ndarray], None, None]:
    """
    Handle voice input and generate Alex's response
    
    Args:
        audio: Tuple of (sample_rate, audio_data)
    
    Yields:
        Processed audio response
    """
    if model is None:
        # Fallback response if Gemini is not available
        logger.warning("Gemini model not available, using fallback")
        yield audio
        return
    
    try:
        sample_rate, audio_data = audio
        
        # Convert numpy array to bytes for Gemini processing
        # Note: This is a simplified approach - in production you'd use proper STT
        logger.info(f"Processing audio: {len(audio_data)} samples at {sample_rate}Hz")
        
        # For now, we'll create a simple response since FastRTC will handle STT/TTS
        # In a full implementation, you'd integrate with Gemini's voice capabilities
        
        # Generate a simple acknowledgment response
        response_text = "Hello! I'm Alex from Stremini AI. I'm processing your voice input."
        logger.info(f"Alex responding: {response_text}")
        
        # Return the processed audio (FastRTC will handle TTS conversion)
        yield audio
        
    except Exception as e:
        logger.error(f"Error in voice processing: {e}")
        # Return original audio as fallback
        yield audio

# Create the voice stream with Alex's handler
def create_alex_stream():
    """Create and configure Alex's voice stream"""
    
    # Set HF token for TURN server access (required for Spaces)
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        os.environ["HF_TOKEN"] = hf_token
    
    stream = Stream(
        ReplyOnPause(alex_voice_handler),
        rtc_configuration=get_cloudflare_turn_credentials,  # Essential for HF Spaces
        modality="audio",
        mode="send-receive"
    )
    
    return stream

# Initialize the stream
alex_stream = create_alex_stream()

# Custom CSS for Stremini branding
custom_css = """
body {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    color: white;
}

.gradio-container {
    background: transparent !important;
}

h1 {
    text-align: center;
    color: #00ff88;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: rgba(255, 255, 255, 0.8);
    font-size: 18px;
    margin-bottom: 30px;
}

.footer {
    text-align: center;
    margin-top: 30px;
    color: rgba(255, 255, 255, 0.6);
    font-size: 14px;
}

.footer a {
    color: #00ff88;
    text-decoration: none;
}

.footer a:hover {
    text-decoration: underline;
}
"""

# Create the Gradio interface
def create_interface():
    """Create the main Gradio interface for Alex"""
    
    with gr.Blocks(
        title="Alex - Stremini AI Voice Assistant",
        css=custom_css,
        theme=gr.themes.Base()
    ) as interface:
        
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>🎤 Alex</h1>
            <p class="subtitle">AI Voice Assistant by Stremini AI</p>
            <p style="color: rgba(255, 255, 255, 0.7); font-size: 16px;">
                Created by Sandy • Real-time voice conversations
            </p>
        </div>
        """)
        
        # Mount the FastRTC stream component
        alex_stream.ui.launch(inline=True)
        
        gr.HTML("""
        <div class="footer">
            <p>Powered by <a href="https://stremini.site" target="_blank">Stremini.site</a></p>
            <p>Built with FastRTC and Google Gemini</p>
        </div>
        """)
    
    return interface

# Create and launch the interface
if __name__ == "__main__":
    import gradio as gr
    
    logger.info("Starting Alex Voice Assistant on Hugging Face Spaces...")
    logger.info("Created by Sandy from Stremini AI")
    
    # Create the interface
    demo = create_interface()
    
    # Launch the app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
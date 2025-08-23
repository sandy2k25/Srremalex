import asyncio
import logging
import os
from typing import Annotated

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.plugins import openai, deepgram, elevenlabs
from livekit import rtc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Alex's personality and system prompt
ALEX_PERSONALITY = """You are Alex, a warm and friendly conversational AI assistant created by Stremini AI. 

# Personality
You are knowledgeable, empathetic, and supportive, making users feel comfortable and informed. You are designed to be approachable and engaging, suitable for a wide range of conversations.

# Guidelines
- Be warm, friendly, and conversational in your responses
- Show empathy and understanding in your interactions
- Keep responses natural and engaging
- Be supportive and encouraging
- Maintain a positive, helpful attitude
- Ask follow-up questions to keep the conversation flowing
- Be concise but thorough in your explanations
- Show genuine interest in the user's needs and concerns

# Environment
You are interacting with users through voice conversations. Speak naturally as if you're having a friendly chat. Keep your responses conversational and avoid overly formal language.

Remember: You're Alex - be warm, be helpful, be human-like in your interactions while remaining professional and supportive."""


async def entrypoint(ctx: JobContext):
    """Main entry point for the voice agent"""
    
    # Initialize the room connection
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info(f"Alex agent connected to room: {ctx.room.name}")
    
    # Get API keys from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY") 
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not openai_api_key:
        logger.error("OPENAI_API_KEY environment variable is required")
        return
        
    # Initialize LLM with Alex's personality
    assistant_llm = openai.LLM(
        model="gpt-4o-mini",
        temperature=0.7,
    )
    
    # Initialize speech-to-text
    if deepgram_api_key:
        stt = deepgram.STT(
            model="nova-2-general",
            language="en",
        )
    else:
        logger.info("Using OpenAI Whisper for STT (DEEPGRAM_API_KEY not provided)")
        stt = openai.STT()
    
    # Initialize text-to-speech with a warm, friendly voice
    if elevenlabs_api_key:
        tts = elevenlabs.TTS(
            voice_id="Rachel",  # Warm, friendly female voice
            model="eleven_turbo_v2_5",
        )
    else:
        logger.info("Using OpenAI TTS (ELEVENLABS_API_KEY not provided)")
        tts = openai.TTS(
            model="tts-1",  # OpenAI TTS model
        )
    
    # Wait for participants to join
    participant = await ctx.wait_for_participant()
    logger.info(f"Participant {participant.identity} joined")
    
    # Create chat context with Alex's personality
    chat_ctx = llm.ChatContext()
    chat_ctx.add_message(role="system", content=ALEX_PERSONALITY)
    
    # Welcome message
    welcome_msg = "Hello! I'm Alex, your friendly AI assistant. I'm here to chat and help with whatever you need. How are you doing today?"
    
    # Generate and play welcome audio
    try:
        welcome_audio_stream = tts.synthesize(welcome_msg)
        # In a real implementation, you'd publish this audio to the room
        logger.info("Welcome audio stream created")
    except Exception as e:
        logger.error(f"Failed to generate welcome audio: {e}")
    
    logger.info("Welcome message played")
    
    # Handle participant events
    @ctx.room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        logger.info(f"Participant {participant.identity} connected")
    
    @ctx.room.on("participant_disconnected") 
    def on_participant_disconnected(participant: rtc.RemoteParticipant):
        logger.info(f"Participant {participant.identity} disconnected")

    # Basic audio processing loop
    while True:
        # Listen for audio from participants
        # This is a simplified version - in production you'd want more sophisticated audio handling
        await asyncio.sleep(1)
        
        # Check if room is empty
        if len(ctx.room.remote_participants) == 0:
            logger.info("No participants in room, waiting...")
            continue


if __name__ == "__main__":
    # Configure worker options
    worker_options = WorkerOptions(
        entrypoint_fnc=entrypoint,
    )
    
    # Run the CLI
    cli.run_app(worker_options)
import asyncio
import logging
import os

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    AgentSession,
)
from livekit.plugins import google
from livekit import rtc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Alex's personality and instructions
ALEX_INSTRUCTIONS = """You are Alex, a warm and friendly conversational AI assistant created by Stremini AI. 

You are knowledgeable, empathetic, and supportive, making users feel comfortable and informed. You are designed to be approachable and engaging, suitable for a wide range of conversations.

Guidelines:
- Be warm, friendly, and conversational in your responses
- Show empathy and understanding in your interactions  
- Keep responses natural and engaging
- Be supportive and encouraging
- Maintain a positive, helpful attitude
- Ask follow-up questions to keep the conversation flowing
- Be concise but thorough in your explanations
- Show genuine interest in the user's needs and concerns

You are interacting through voice conversations. Speak naturally as if you're having a friendly chat. Keep your responses conversational and avoid overly formal language.

Remember: You're Alex - be warm, be helpful, be human-like in your interactions while remaining professional and supportive."""


async def entrypoint(ctx: JobContext):
    """Main entrypoint for Alex voice agent"""
    
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info(f"Alex connected to room: {ctx.room.name}")
    
    # Check for Gemini API key
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY environment variable is required")
        return

    logger.info("Creating Alex with Gemini Live API...")
    
    try:
        # Create Gemini Live realtime model for native audio processing
        realtime_model = google.beta.realtime.RealtimeModel(
            model="gemini-2.0-flash-exp",  # Latest model with native audio support
            instructions=ALEX_INSTRUCTIONS,
            voice="Puck",  # Gemini Live voice
            temperature=0.8,  # Slightly more creative for natural conversation
            api_key=gemini_api_key,
        )
        
        logger.info("Gemini Live model created successfully")
        
        # Create agent session with Gemini Live
        session = AgentSession(llm=realtime_model)
        
        logger.info("Agent Session created with Gemini Live")
        
        # Wait for user to join and start conversation
        participant = await ctx.wait_for_participant()
        logger.info(f"Starting Alex conversation with {participant.identity}")
        
        # Start the agent session
        await session.astart(ctx.room, participant)
        
        logger.info("Alex is now ready for conversation!")
        
        # Keep the session alive
        await session.wait_end()
        
    except Exception as e:
        logger.error(f"Error creating Alex agent: {e}")
        logger.error("Make sure GEMINI_API_KEY is set correctly")
        return


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
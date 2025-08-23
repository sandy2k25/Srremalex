import asyncio
import logging
import os

from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import google

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


class AlexAssistant(Agent):
    """Alex - A warm and friendly AI voice assistant"""
    
    def __init__(self) -> None:
        super().__init__(instructions=ALEX_INSTRUCTIONS)


async def entrypoint(ctx: agents.JobContext):
    """Main entrypoint for Alex voice agent"""
    
    logger.info(f"Alex connecting to room: {ctx.room.name}")
    
    # Check for Gemini API key
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY environment variable is required")
        return

    logger.info("Creating Alex with Gemini Live API...")
    
    try:
        # Create agent session with Gemini Live for native voice processing
        session = AgentSession(
            llm=google.beta.realtime.RealtimeModel(
                model="gemini-2.0-flash-exp",  # Latest model with native audio support
                instructions=ALEX_INSTRUCTIONS,
                voice="Puck",  # Gemini Live voice
                temperature=0.8,  # Slightly more creative for natural conversation
                api_key=gemini_api_key,
            ),
        )
        
        logger.info("Agent Session created with Gemini Live")
        
        # Start the agent session
        await session.start(
            room=ctx.room,
            agent=AlexAssistant(),
        )
        
        logger.info("Alex is now ready for conversation!")
        
        # Wait for the session to be fully established
        await ctx.room.wait_for_participant()
        logger.info("Participant joined, Alex is now active!")
        
        # Keep the session running and responsive
        await session.wait_for_completion()
        
    except Exception as e:
        logger.error(f"Error creating Alex agent: {e}")
        logger.error("Make sure GEMINI_API_KEY is set correctly")
        return


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
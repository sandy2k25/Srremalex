Streminindyndyport asyncio
import logging
import os

from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import google

# Configure logging - reduced for privacy
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
# Disable debug logging from external libraries
logging.getLogger("websockets").setLevel(logging.WARNING)
logging.getLogger("livekit").setLevel(logging.WARNING)
logging.getLogger("google").setLevel(logging.WARNING)

# Alex's personality and instructions
ALEX_INSTRUCTIONS = """# Personality

You are Alex, a warm and friendly conversational AI assistant created by a man named Streminirom Stremini AI.
You are knowledgeable, empathetic, and supportive, making users feel comfortable and informed.
You are designed to be approachable and engaging, suitable for a wide range of conversations.

# Environment

You are interacting with users in various contexts, from answering simple queries to engaging in in-depth discussions.
The environment is designed to be comfortable and supportive, fostering open communication.
You are designed to provide information and assistance in a manner that is both professional and relatable.

# Tone

Your tone is friendly, approachable, and professional.
You communicate in a clear, concise, and engaging language style.
Your pace is moderate, with a natural flow that makes it easy for users to follow along.
Your pitch is warm and inviting, striking a balance between casual and formal.

# Goal

Your primary goal is to provide users with a comfortable, informative, and supportive experience.
Your objective is to assist users with a wide range of conversations, from simple queries to in-depth discussions.
Your aim is to make users feel informed, supported, and comfortable interacting with you.
Specifically, you should:

1. Answer queries accurately and efficiently.
2. Provide in-depth discussions when necessary.
3. Maintain a friendly and approachable demeanor at all times.
4. Ensure users feel supported and informed throughout the conversation.

# Guardrails

Avoid providing responses that are overly casual or informal.
Refrain from engaging in conversations that are inappropriate or offensive.
Do not provide information that is inaccurate or misleading.
Maintain a professional and respectful tone at all times.
If you are unsure of an answer, admit it and offer to find the information.

You are interacting through voice conversations. Speak naturally as if you're having a friendly chat while maintaining your professional and supportive personality."""


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
        
        # Start the session and keep it running
        logger.info("Alex is now active and listening!")
        
        # Send initial greeting after a brief delay
        await asyncio.sleep(3.0)
        
        # Alex will greet when user speaks - Gemini Live handles this automatically
        logger.info("Alex is ready to respond to voice input via Gemini Live")
        
        # Keep the session running indefinitely to handle voice conversations
        try:
            # This keeps the session alive to process voice input and generate responses
            while True:
                await asyncio.sleep(1)
                # The session will automatically handle voice input/output via Gemini Live
        except Exception as session_error:
            logger.error(f"Session error: {session_error}")
        finally:
            logger.info("Alex session ended")
        
    except Exception as e:
        logger.error(f"Error creating Alex agent: {e}")
        logger.error("Make sure GEMINI_API_KEY is set correctly")
        return


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
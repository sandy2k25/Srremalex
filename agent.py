import asyncio
import logging
import os

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.voice import Agent
from livekit.plugins import deepgram, elevenlabs, openai
from livekit import rtc
import google.genai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Alex's personality
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


class GeminiLLM(llm.LLM):
    """Custom Gemini LLM for LiveKit"""
    
    def __init__(self, model: str = "gemini-2.5-flash"):
        super().__init__()
        self._model = model
        self._client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    def chat(
        self,
        *,
        chat_ctx: llm.ChatContext,
        tools: list[llm.FunctionTool | llm.RawFunctionTool] | None = None,
        parallel_tool_calls: bool | None = None,
        tool_choice: llm.ToolChoice | None = None,
        extra_kwargs: dict | None = None,
    ) -> "GeminiLLMStream":
        return GeminiLLMStream(self, chat_ctx)


class GeminiLLMStream(llm.LLMStream):
    """Streaming implementation for Gemini"""
    
    def __init__(self, llm_impl: GeminiLLM, chat_ctx: llm.ChatContext):
        super().__init__(llm_impl, chat_ctx)
        self._llm = llm_impl
        self._chat_ctx = chat_ctx
        self._generated = False

    async def _run(self) -> None:
        if self._generated:
            return
        
        try:
            # Build prompt from chat context
            prompt_parts = []
            
            # Get the chat messages (this might be different based on actual API)
            if hasattr(self._chat_ctx, '_messages'):
                messages = self._chat_ctx._messages
            else:
                # Fallback - use string representation
                prompt_parts.append(str(self._chat_ctx))
                
            if messages:
                for msg in messages:
                    role = str(msg.role) if hasattr(msg, 'role') else 'User'
                    content = str(msg.content) if hasattr(msg, 'content') else str(msg)
                    prompt_parts.append(f"{role}: {content}")
            
            full_prompt = "\n".join(prompt_parts) if prompt_parts else "Hello"
            
            # Generate with Gemini
            response = self._llm._client.models.generate_content(
                model=self._llm._model,
                contents=full_prompt,
            )
            
            response_text = response.text if response.text else "Hello! I'm Alex, how can I help you today?"
            
            # Yield response chunk
            chunk = llm.ChatChunk(
                id="gemini-chunk",
                choices=[{
                    "delta": {
                        "content": response_text,
                        "role": "assistant"
                    },
                    "index": 0
                }]
            )
            
            self._push_chunk(chunk)
            self._generated = True
            
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            # Fallback response
            chunk = llm.ChatChunk(
                id="gemini-error",
                choices=[{
                    "delta": {
                        "content": "I'm having trouble right now. Please try again.",
                        "role": "assistant"
                    },
                    "index": 0
                }]
            )
            self._push_chunk(chunk)
            self._generated = True


async def entrypoint(ctx: JobContext):
    """Main entrypoint for Alex voice agent"""
    
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info(f"Alex connected to room: {ctx.room.name}")
    
    # Check API keys
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY required")
        return
        
    # Initialize components
    gemini_llm = GeminiLLM()
    
    # STT setup
    deepgram_key = os.getenv("DEEPGRAM_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if deepgram_key:
        stt = deepgram.STT(model="nova-2-general", language="en")
        logger.info("Using Deepgram STT")
    elif openai_key:
        stt = openai.STT()
        logger.info("Using OpenAI STT")
    else:
        logger.error("Need DEEPGRAM_API_KEY or OPENAI_API_KEY for STT")
        return
    
    # TTS setup
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    
    if elevenlabs_key:
        tts = elevenlabs.TTS(voice="Rachel", model="eleven_turbo_v2_5")
        logger.info("Using ElevenLabs TTS")
    elif openai_key:
        tts = openai.TTS(model="tts-1")
        logger.info("Using OpenAI TTS")
    else:
        logger.error("Need ELEVENLABS_API_KEY or OPENAI_API_KEY for TTS")
        return
    
    # Create voice agent
    agent = Agent(
        instructions=ALEX_INSTRUCTIONS,
        llm=gemini_llm,
        stt=stt,
        tts=tts,
    )
    
    # Wait for participant and start
    @ctx.room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        logger.info(f"Participant {participant.identity} joined Alex")
    
    logger.info("Alex (Gemini-powered) ready for conversations!")
    
    # Start agent session when participant joins
    participant = await ctx.wait_for_participant()
    logger.info(f"Starting Alex session for {participant.identity}")
    
    # Run agent session
    session = agent.start_session()
    await session.wait_end()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
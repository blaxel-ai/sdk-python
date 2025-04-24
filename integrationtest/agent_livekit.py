import os
from logging import getLogger

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RoomInputOptions
from livekit.plugins import deepgram, elevenlabs, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from blaxel.models import bl_model
from blaxel.tools import Tool, bl_tools

load_dotenv()

logger = getLogger(__name__)

MODEL = "gpt-4o-mini"
# MODEL = "claude-3-7-sonnet-20250219"
# MODEL = "xai-grok-beta"
# MODEL = "cohere-command-r-plus" # x -> tool call not supported
# MODEL = "gemini-2-0-flash"
# MODEL = "deepseek-chat"
# MODEL = "mistral-large-latest"

class Assistant(Agent):
    def __init__(self, tools: list[Tool] = []) -> None:

        super().__init__(
            instructions="""
                You are a helpful voice AI assistant.
            """,
            tools=tools,
        )

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    tools = await bl_tools(["blaxel-search"]).to_livekit()
    model = await bl_model(MODEL).to_livekit()
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=model,
        tts=elevenlabs.TTS(
            voice_id="ODq5zmih8GrVes37Dizd",
            model="eleven_multilingual_v2"
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(tools=tools),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    logger.info("Starting assistant...")
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint, port=os.getenv("BL_SERVER_PORT", 80)))
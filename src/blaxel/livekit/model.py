from logging import getLogger

from livekit.plugins import groq, openai

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings

logger = getLogger(__name__)

async def get_livekit_model(url: str, type: str, model: str, **kwargs):
    if type == 'xai':
        return groq.LLM(
            model=model,
            api_key=settings.auth.token,
            base_url=f"{url}/v1",
            **kwargs
        )
    else:
        if type != 'openai':
            logger.warning(f"Livekit not compatible with: {type}, defaulting to openai.LLM")
        return openai.LLM(
            model=model,
            api_key=settings.auth.token,
            base_url=f"{url}/v1",
            **kwargs
        )

async def bl_model(name: str, **kwargs):
    url, type, model = await bl_model_core(name).get_parameters()
    return await get_livekit_model(url, type, model, **kwargs)
    return await get_livekit_model(url, type, model, **kwargs)

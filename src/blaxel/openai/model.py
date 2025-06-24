from agents import AsyncOpenAI, OpenAIChatCompletionsModel

from blaxel.core import bl_model as bl_model_core
from blaxel.core import settings


async def bl_model(name, **kwargs):
    url, type, model = await bl_model_core(name).get_parameters()
    if type != "openai":
        raise ValueError(f"Invalid model type: {type}")
    external_client = AsyncOpenAI(
        base_url=f"{url}/v1",
        api_key=settings.auth.token,
        default_headers=settings.headers,
    )

    return OpenAIChatCompletionsModel(
        model=model,
        openai_client=external_client,
        **kwargs
    )
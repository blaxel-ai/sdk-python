from agents import AsyncOpenAI, OpenAIChatCompletionsModel

from ..common.settings import settings


async def get_openai_model(url: str, type: str, model: str, **kwargs):
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
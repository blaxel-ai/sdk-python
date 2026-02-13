from ..cache import find_from_cache
from ..client import client
from ..client.api.models import get_model
from ..client.models import Model
from ..client.models.model_runtime_generation import ModelRuntimeGeneration
from ..client.types import Unset
from ..common import settings


class BLModel:
    models = {}

    def __init__(self, model_name, **kwargs):
        self.model_name = model_name
        self.kwargs = kwargs

    async def get_parameters(self) -> tuple[str, str, str]:
        if self.model_name in self.models:
            # We get the headers in case we need to refresh the token
            settings.auth.get_headers()
            model = self.models[self.model_name]
            return model["url"], model["type"], model["model"]

        model_data = await self._get_model_metadata()
        if not model_data:
            raise Exception(f"Model {self.model_name} not found")
        runtime = model_data.spec and model_data.spec.runtime
        if not runtime:
            raise Exception(f"Model {self.model_name} has no runtime")

        model = runtime.model

        # mk3 models use the direct gateway URL and always speak OpenAI-compatible API
        generation = runtime.generation
        if not isinstance(generation, Unset) and generation == ModelRuntimeGeneration.MK3:
            metadata_url = model_data.metadata.url
            if isinstance(metadata_url, Unset) or not metadata_url:
                raise Exception(
                    f"Model {self.model_name} is mk3 but has no gateway URL in metadata"
                )
            self.models[self.model_name] = {
                "url": metadata_url,
                "type": "openai",
                "model": self.model_name,
            }
            return metadata_url, "openai", self.model_name

        url = f"{settings.run_url}/{settings.auth.workspace_name}/models/{self.model_name}"
        type = runtime.type_ or "openai"
        self.models[self.model_name] = {
            "url": url,
            "type": type,
            "model": model,
        }
        return url, type, model

    async def _get_model_metadata(self) -> Model | None:
        cache_data = await find_from_cache("Model", self.model_name)
        if cache_data:
            return Model.from_dict(cache_data)

        try:
            return await get_model.asyncio(client=client, model_name=self.model_name)
        except Exception:
            return None


def bl_model(model_name, **kwargs):
    return BLModel(model_name, **kwargs)


__all__ = ["bl_model"]

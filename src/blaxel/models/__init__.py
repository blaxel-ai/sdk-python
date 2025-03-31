
from ..cache import find_from_cache
from ..client import client
from ..client.api.models import get_model
from ..client.models import Model
from ..common.settings import settings
from .crewai import get_crewai_model
from .langchain import get_langchain_model
from .llamaindex import get_llamaindex_model
from .openai import get_openai_model


class BLModel:
    def __init__(self, model_name, **kwargs):
        self.model_name = model_name
        self.kwargs = kwargs

    async def to_langchain(self):
        url, type, model = await self._get_parameters()
        return await get_langchain_model(url, type, model, **self.kwargs)

    async def to_llamaindex(self):
        url, type, model = await self._get_parameters()
        return await get_llamaindex_model(url, type, model, **self.kwargs)

    async def to_crewai(self):
        url, type, model = await self._get_parameters()
        return await get_crewai_model(url, type, model, **self.kwargs)

    async def to_openai(self):
        url, type, model = await self._get_parameters()
        return await get_openai_model(url, type, model, **self.kwargs)

    async def _get_parameters(self):
        url = f"{settings.run_url}/{settings.auth.workspace_name}/models/{self.model_name}"
        model_data = await self._get_model_metadata()
        if not model_data:
            raise Exception(f"Model {self.model_name} not found")
        runtime = (model_data.spec and model_data.spec.runtime)
        if not runtime:
            raise Exception(f"Model {self.model_name} has no runtime")

        type = runtime.type_ or 'openai'
        model = runtime.model
        return url, type, model

    async def _get_model_metadata(self) -> Model | None:
        cache_data = await find_from_cache('Model', self.model_name)
        if cache_data:
            return Model(**cache_data)

        try:
            return await get_model.asyncio(client=client, model_name=self.model_name)
        except Exception as e:
            return None

def bl_model(model_name, **kwargs):
    return BLModel(model_name, **kwargs)

__all__ = ["bl_model"]

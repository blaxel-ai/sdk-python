
from ..cache import find_from_cache
from ..client import client
from ..client.api.models import get_model
from ..client.models import Model
from ..common.settings import settings


class BLModel:
    models = {}

    def __init__(self, model_name, **kwargs):
        self.model_name = model_name
        self.kwargs = kwargs

    async def to_langchain(self):
        if f"langchain_{self.model_name}" in BLModel.models:
            return BLModel.models[f"langchain_{self.model_name}"]

        from .langchain import get_langchain_model
        url, type, model = await self._get_parameters()
        model = await get_langchain_model(url, type, model, **self.kwargs)
        BLModel.models[f"langchain_{self.model_name}"] = model
        return model

    async def to_llamaindex(self):
        if f"llamaindex_{self.model_name}" in BLModel.models:
            return BLModel.models[f"llamaindex_{self.model_name}"]

        from .llamaindex import get_llamaindex_model
        url, type, model = await self._get_parameters()
        model = await get_llamaindex_model(url, type, model, **self.kwargs)
        BLModel.models[f"llamaindex_{self.model_name}"] = model
        return model

    async def to_crewai(self):
        if f"crewai_{self.model_name}" in BLModel.models:
            return BLModel.models[f"crewai_{self.model_name}"]

        from .crewai import get_crewai_model

        url, type, model = await self._get_parameters()
        model = await get_crewai_model(url, type, model, **self.kwargs)
        BLModel.models[f"crewai_{self.model_name}"] = model
        return model

    async def to_openai(self):
        if f"openai_{self.model_name}" in BLModel.models:
            return BLModel.models[f"openai_{self.model_name}"]

        from .openai import get_openai_model
        url, type, model = await self._get_parameters()
        model = await get_openai_model(url, type, model, **self.kwargs)
        BLModel.models[f"openai_{self.model_name}"] = model
        return model

    async def to_pydantic(self):
        if f"pydantic_{self.model_name}" in BLModel.models:
            return BLModel.models[f"pydantic_{self.model_name}"]

        from .pydantic import get_pydantic_model
        url, type, model = await self._get_parameters()
        model = await get_pydantic_model(url, type, model, **self.kwargs)
        BLModel.models[f"pydantic_{self.model_name}"] = model
        return model

    async def to_google_adk(self):
        if f"googleadk_{self.model_name}" in BLModel.models:
            return BLModel.models[f"googleadk_{self.model_name}"]

        from .googleadk import get_google_adk_model
        url, type, model = await self._get_parameters()
        model = await get_google_adk_model(url, type, model, **self.kwargs)
        BLModel.models[f"googleadk_{self.model_name}"] = model
        return model

    async def _get_parameters(self) -> tuple[str, str, str]:
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
            return Model.from_dict(cache_data)

        try:
            return await get_model.asyncio(client=client, model_name=self.model_name)
        except Exception as e:
            return None

def bl_model(model_name, **kwargs):
    return BLModel(model_name, **kwargs)

__all__ = ["bl_model"]

from http import HTTPStatus

from ..cache import find_from_cache
from ..client import client
from ..client.api.models import get_model
from ..client.models import Error, Model
from ..common import settings
from ..errors import BlaxelError, ModelNotFoundError


def _error_http_status(error: Error) -> int | None:
    """Best-effort HTTP status for a modeled ``Error`` returned by ``get_model``."""
    response = getattr(error, "_response", None)
    status = getattr(response, "status_code", None)
    if isinstance(status, int) and not isinstance(status, bool):
        return status
    code = getattr(error, "code", None)
    if isinstance(code, int) and not isinstance(code, bool):
        return code
    return None


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
        url = f"{settings.run_url}/{settings.auth.workspace_name}/models/{self.model_name}"
        model_data = await self._get_model_metadata()
        if model_data is None:
            raise ModelNotFoundError(f"Model {self.model_name} not found")
        runtime = model_data.spec and model_data.spec.runtime
        if not runtime:
            raise ModelNotFoundError(f"Model {self.model_name} has no runtime")

        type = runtime.type_ or "openai"
        model = runtime.model
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

        result = await get_model.asyncio(client=client, model_name=self.model_name)
        if isinstance(result, Model):
            return result
        # Documented error statuses (401/403/404/500) deserialize to an ``Error``
        # instead of raising. Only a 404 means the model does not exist; surface
        # any other status as the real failure rather than masking it as a
        # misleading "not found". Transient/network/undocumented failures from
        # ``get_model`` propagate untouched for the same reason.
        if isinstance(result, Error):
            status = _error_http_status(result)
            if status is not None and status != HTTPStatus.NOT_FOUND:
                raise BlaxelError(
                    f"Failed to resolve model {self.model_name}",
                    status=status,
                    response=getattr(result, "_response", None),
                )
        return None


def bl_model(model_name, **kwargs):
    return BLModel(model_name, **kwargs)


__all__ = ["BLModel", "ModelNotFoundError", "bl_model"]

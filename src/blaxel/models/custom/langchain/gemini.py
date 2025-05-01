from __future__ import annotations

import asyncio
import json
import logging
import uuid
import warnings
from operator import itemgetter
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

import httpx
import requests
from langchain_core.callbacks.manager import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from langchain_core.language_models import LanguageModelInput
from langchain_core.language_models.chat_models import BaseChatModel, LangSmithParams
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.messages.ai import UsageMetadata
from langchain_core.messages.tool import invalid_tool_call, tool_call, tool_call_chunk
from langchain_core.output_parsers.openai_tools import (
    JsonOutputKeyToolsParser,
    PydanticToolsParser,
    parse_tool_calls,
)
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool
from PIL import Image
from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from typing_extensions import Self, is_typeddict

WARNED_STRUCTURED_OUTPUT_JSON_MODE = False

logger = logging.getLogger(__name__)

# Type definitions
_FunctionDeclarationType = Union[
    Dict[str, Any],
    Callable[..., Any],
]

_ToolChoiceType = Union[str, bool, Dict[str, Any]]
_ToolConfigDict = Dict[str, Any]
_ToolDict = Dict[str, Any]
SafetySettingDict = Dict[str, str]
OutputParserLike = Union[PydanticToolsParser, JsonOutputKeyToolsParser]

# Data classes
class Part(BaseModel):
    text: Optional[str] = None
    inline_data: Optional[Dict[str, Any]] = None
    file_data: Optional[Dict[str, Any]] = None
    function_call: Optional[Dict[str, Any]] = None
    function_response: Optional[Dict[str, Any]] = None

class Content(BaseModel):
    role: Optional[str] = None
    parts: List[Part]

class Blob(BaseModel):
    data: str
    mime_type: str

class FileData(BaseModel):
    file_uri: str
    mime_type: str

class VideoMetadata(BaseModel):
    duration: Optional[str] = None
    start_offset: Optional[str] = None
    end_offset: Optional[str] = None

class FunctionCall(BaseModel):
    name: str
    args: Dict[str, Any]

class FunctionResponse(BaseModel):
    name: str
    response: Dict[str, Any]

class SafetySetting(BaseModel):
    category: str
    threshold: str

class ToolConfig(BaseModel):
    function_calling_config: Dict[str, Any]

class GenerationConfig(BaseModel):
    candidate_count: Optional[int] = None
    temperature: Optional[float] = None
    stop_sequences: Optional[List[str]] = None
    max_output_tokens: Optional[int] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    response_modalities: Optional[List[str]] = None

class GoogleTool(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

class ImageBytesLoader:
    def load_part(self, image_url: str) -> Part:
        """Load an image from a URL and convert it to a Part."""
        import io

        response = requests.get(image_url)
        response.raise_for_status()

        # Convert to JPEG format
        img = Image.open(io.BytesIO(response.content))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        return Part(
            inline_data={
                "mime_type": "image/jpeg",
                "data": img_byte_arr.decode('utf-8')
            }
        )

class ChatGoogleGenerativeAIError(Exception):
    """
    Custom exception class for errors associated with the `Google GenAI` API.

    This exception is raised when there are specific issues related to the
    Google genai API usage in the ChatGoogleGenerativeAI class, such as unsupported
    message types or roles.
    """
    pass


def _create_retry_decorator() -> Callable[[Any], Any]:
    """
    Creates and returns a preconfigured tenacity retry decorator.

    The retry decorator is configured to handle specific HTTP exceptions
    such as rate limits and service unavailability. It uses an exponential
    backoff strategy for retries.

    Returns:
        Callable[[Any], Any]: A retry decorator configured for handling specific
        HTTP exceptions.
    """
    multiplier = 2
    min_seconds = 1
    max_seconds = 60
    max_retries = 2

    return retry(
        reraise=True,
        stop=stop_after_attempt(max_retries),
        wait=wait_exponential(multiplier=multiplier, min=min_seconds, max=max_seconds),
        retry=(
            retry_if_exception_type(httpx.HTTPStatusError)
            | retry_if_exception_type(httpx.ConnectError)
            | retry_if_exception_type(httpx.ReadTimeout)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )


def _chat_with_retry(generation_method: Callable, **kwargs: Any) -> Any:
    """
    Executes a chat generation method with retry logic using tenacity.

    This function is a wrapper that applies a retry mechanism to a provided
    chat generation function. It is useful for handling intermittent issues
    like network errors or temporary service unavailability.

    Args:
        generation_method (Callable): The chat generation method to be executed.
        **kwargs (Any): Additional keyword arguments to pass to the generation method.

    Returns:
        Any: The result from the chat generation method.
    """
    retry_decorator = _create_retry_decorator()

    @retry_decorator
    def _chat_with_retry(**kwargs: Any) -> Any:
        try:
            # Extract request parameters and other kwargs
            request = kwargs.pop('request', {})
            kwargs.pop('metadata', None)

            # Unpack request parameters into kwargs
            kwargs.update(request)

            return generation_method(**kwargs)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:  # Rate limit
                error_msg = (
                    "Rate limit exceeded. Please try again later or use a different API key."
                )
                raise ValueError(error_msg)
            elif e.response.status_code == 403:  # Forbidden
                error_msg = (
                    "Access forbidden. Please check your API key and permissions."
                )
                raise ValueError(error_msg)
            else:
                raise ChatGoogleGenerativeAIError(
                    f"HTTP error occurred: {e.response.text}"
                ) from e
        except Exception as e:
            raise e

    return _chat_with_retry(**kwargs)


async def _achat_with_retry(generation_method: Callable, **kwargs: Any) -> Any:
    """
    Executes a chat generation method with retry logic using tenacity.

    This function is a wrapper that applies a retry mechanism to a provided
    chat generation function. It is useful for handling intermittent issues
    like network errors or temporary service unavailability.

    Args:
        generation_method (Callable): The chat generation method to be executed.
        **kwargs (Any): Additional keyword arguments to pass to the generation method.

    Returns:
        Any: The result from the chat generation method.
    """
    retry_decorator = _create_retry_decorator()

    @retry_decorator
    async def _achat_with_retry(**kwargs: Any) -> Any:
        try:
            # Extract request parameters and other kwargs
            request = kwargs.pop('request', {})
            kwargs.pop('metadata', None)

            # Unpack request parameters into kwargs
            kwargs.update(request)

            return await generation_method(**kwargs)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:  # Rate limit
                error_msg = (
                    "Rate limit exceeded. Please try again later or use a different API key."
                )
                raise ValueError(error_msg)
            elif e.response.status_code == 403:  # Forbidden
                error_msg = (
                    "Access forbidden. Please check your API key and permissions."
                )
                raise ValueError(error_msg)
            else:
                raise ChatGoogleGenerativeAIError(
                    f"HTTP error occurred: {e.response.text}"
                ) from e
        except Exception as e:
            raise e

    return await _achat_with_retry(**kwargs)


def _is_openai_parts_format(part: dict) -> bool:
    return "type" in part


def _convert_to_parts(
    raw_content: Union[str, Sequence[Union[str, dict]]],
) -> List[Part]:
    """Converts a list of LangChain messages into a google parts."""
    parts = []
    content = [raw_content] if isinstance(raw_content, str) else raw_content
    image_loader = ImageBytesLoader()
    for part in content:
        if isinstance(part, str):
            parts.append(Part(text=part))
        elif isinstance(part, Mapping):
            # OpenAI Format
            if _is_openai_parts_format(part):
                if part["type"] == "text":
                    parts.append(Part(text=part["text"]))
                elif part["type"] == "image_url":
                    img_url = part["image_url"]
                    if isinstance(img_url, dict):
                        if "url" not in img_url:
                            raise ValueError(
                                f"Unrecognized message image format: {img_url}"
                            )
                        img_url = img_url["url"]
                    parts.append(image_loader.load_part(img_url))
                # Handle media type like LangChain.js
                # https://github.com/langchain-ai/langchainjs/blob/e536593e2585f1dd7b0afc187de4d07cb40689ba/libs/langchain-google-common/src/utils/gemini.ts#L93-L106
                elif part["type"] == "media":
                    if "mime_type" not in part:
                        raise ValueError(f"Missing mime_type in media part: {part}")
                    mime_type = part["mime_type"]
                    media_part = Part()

                    if "data" in part:
                        media_part.inline_data = Blob(
                            data=part["data"], mime_type=mime_type
                        )
                    elif "file_uri" in part:
                        media_part.file_data = FileData(
                            file_uri=part["file_uri"], mime_type=mime_type
                        )
                    else:
                        raise ValueError(
                            f"Media part must have either data or file_uri: {part}"
                        )
                    parts.append(media_part)
                else:
                    raise ValueError(
                        f"Unrecognized message part type: {part['type']}. Only text, "
                        f"image_url, and media types are supported."
                    )
            else:
                # Yolo
                logger.warning(
                    "Unrecognized message part format. Assuming it's a text part."
                )
                parts.append(Part(text=str(part)))
        else:
            # TODO: Maybe some of Google's native stuff
            # would hit this branch.
            raise ChatGoogleGenerativeAIError(
                "Gemini only supports text and inline_data parts."
            )
    return parts


def _convert_tool_message_to_part(
    message: ToolMessage | FunctionMessage, name: Optional[str] = None
) -> Part:
    """Converts a tool or function message to a google part."""
    # Legacy agent stores tool name in message.additional_kwargs instead of message.name
    name = message.name or name or message.additional_kwargs.get("name")
    response: Any
    if not isinstance(message.content, str):
        response = message.content
    else:
        try:
            response = json.loads(message.content)
        except json.JSONDecodeError:
            response = message.content  # leave as str representation
    if not isinstance(response, dict):
        response = {"output": response}
    part = Part(
        function_response=FunctionResponse(
            name=name,
            response=response,
        ).model_dump()
    )
    return part


def _get_ai_message_tool_messages_parts(
    tool_messages: Sequence[ToolMessage], ai_message: AIMessage
) -> list[Part]:
    """
    Finds relevant tool messages for the AI message and converts them to a single
    list of Parts.
    """
    # We are interested only in the tool messages that are part of the AI message
    tool_calls_ids = {tool_call["id"]: tool_call for tool_call in ai_message.tool_calls}
    parts = []
    for i, message in enumerate(tool_messages):
        if not tool_calls_ids:
            break
        if message.tool_call_id in tool_calls_ids:
            tool_call = tool_calls_ids[message.tool_call_id]
            part = _convert_tool_message_to_part(message, name=tool_call.get("name"))
            parts.append(part)
            # remove the id from the dict, so that we do not iterate over it again
            tool_calls_ids.pop(message.tool_call_id)
    return parts


def _parse_chat_history(
    input_messages: Sequence[BaseMessage], convert_system_message_to_human: bool = False
) -> Tuple[Optional[Content], List[Content]]:
    messages: List[Content] = []

    if convert_system_message_to_human:
        warnings.warn("Convert_system_message_to_human will be deprecated!")

    system_instruction: Optional[Content] = None
    messages_without_tool_messages = [
        message for message in input_messages if not isinstance(message, ToolMessage)
    ]
    tool_messages = [
        message for message in input_messages if isinstance(message, ToolMessage)
    ]
    for i, message in enumerate(messages_without_tool_messages):
        if isinstance(message, SystemMessage):
            system_parts = _convert_to_parts(message.content)
            if i == 0:
                system_instruction = Content(parts=system_parts)
            elif system_instruction is not None:
                system_instruction.parts.extend(system_parts)
            else:
                pass
            continue
        elif isinstance(message, AIMessage):
            role = "model"
            if message.tool_calls:
                ai_message_parts = []
                for tool_call in message.tool_calls:
                    function_call = FunctionCall(
                        name=tool_call["name"],
                        args=tool_call["args"],
                    )
                    ai_message_parts.append(Part(function_call=function_call.model_dump()))
                tool_messages_parts = _get_ai_message_tool_messages_parts(
                    tool_messages=tool_messages, ai_message=message
                )
                messages.append(Content(role=role, parts=ai_message_parts))
                messages.append(Content(role="user", parts=tool_messages_parts))
                continue
            elif raw_function_call := message.additional_kwargs.get("function_call"):
                function_call = FunctionCall(
                    name=raw_function_call["name"],
                    args=json.loads(raw_function_call["arguments"]),
                )
                parts = [Part(function_call=function_call.model_dump())]
            else:
                parts = _convert_to_parts(message.content)
        elif isinstance(message, HumanMessage):
            role = "user"
            parts = _convert_to_parts(message.content)
            if i == 1 and convert_system_message_to_human and system_instruction:
                parts = [p for p in system_instruction.parts] + parts
                system_instruction = None
        elif isinstance(message, FunctionMessage):
            role = "user"
            parts = [_convert_tool_message_to_part(message)]
        else:
            raise ValueError(
                f"Unexpected message with type {type(message)} at the position {i}."
            )

        messages.append(Content(role=role, parts=parts))
    return system_instruction, messages


def _parse_response_candidate(
    response_candidate: Dict[str, Any], streaming: bool = False
) -> AIMessage:
    content: Union[None, str, List[Union[str, dict]]] = None
    additional_kwargs = {}
    tool_calls = []
    invalid_tool_calls = []
    tool_call_chunks = []

    for part in response_candidate.get("content", {}).get("parts", []):
        try:
            text: Optional[str] = part.get("text")
            # Remove erroneous newline character if present
            if text is not None:
                text = text.rstrip("\n")
        except AttributeError:
            text = None

        if text is not None:
            if not content:
                content = text
            elif isinstance(content, str) and text:
                content = [content, text]
            elif isinstance(content, list) and text:
                content.append(text)
            elif text:
                raise Exception("Unexpected content type")

        if part.get("inlineData", {}).get("mimeType", "").startswith("image/"):
            image_format = part["inlineData"]["mimeType"][6:]
            message = {
                "type": "image_url",
                "image_url": {
                    "url": image_bytes_to_b64_string(
                        part["inlineData"]["data"], image_format=image_format
                    )
                },
            }

            if not content:
                content = [message]
            elif isinstance(content, str) and message:
                content = [content, message]
            elif isinstance(content, list) and message:
                content.append(message)
            elif message:
                raise Exception("Unexpected content type")

        if part.get("functionCall"):
            function_call = {"name": part["functionCall"]["name"]}
            function_call["arguments"] = json.dumps(part["functionCall"].get("args", {}))
            additional_kwargs["function_call"] = function_call

            if streaming:
                tool_call_chunks.append(
                    tool_call_chunk(
                        name=function_call.get("name"),
                        args=function_call.get("arguments"),
                        id=function_call.get("id", str(uuid.uuid4())),
                        index=function_call.get("index"),  # type: ignore
                    )
                )
            else:
                try:
                    tool_call_dict = parse_tool_calls(
                        [{"function": function_call}],
                        return_id=False,
                    )[0]
                except Exception as e:
                    invalid_tool_calls.append(
                        invalid_tool_call(
                            name=function_call.get("name"),
                            args=function_call.get("arguments"),
                            id=function_call.get("id", str(uuid.uuid4())),
                            error=str(e),
                        )
                    )
                else:
                    tool_calls.append(
                        tool_call(
                            name=tool_call_dict["name"],
                            args=tool_call_dict["args"],
                            id=tool_call_dict.get("id", str(uuid.uuid4())),
                        )
                    )
    if content is None:
        content = ""

    if streaming:
        return AIMessageChunk(
            content=cast(Union[str, List[Union[str, Dict[Any, Any]]]], content),
            additional_kwargs=additional_kwargs,
            tool_call_chunks=tool_call_chunks,
        )

    return AIMessage(
        content=cast(Union[str, List[Union[str, Dict[Any, Any]]]], content),
        additional_kwargs=additional_kwargs,
        tool_calls=tool_calls,
        invalid_tool_calls=invalid_tool_calls,
    )


def _response_to_result(
    response: Dict[str, Any],
    stream: bool = False,
    prev_usage: Optional[UsageMetadata] = None,
) -> ChatResult:
    """Converts a Gemini API response into a LangChain ChatResult."""
    llm_output = {"prompt_feedback": response.get("promptFeedback", {})}

    # previous usage metadata needs to be subtracted because gemini api returns
    # already-accumulated token counts with each chunk
    prev_input_tokens = prev_usage["input_tokens"] if prev_usage else 0
    prev_output_tokens = prev_usage["output_tokens"] if prev_usage else 0
    prev_total_tokens = prev_usage["total_tokens"] if prev_usage else 0

    # Get usage metadata
    try:
        usage_metadata = response.get("usageMetadata", {})
        input_tokens = usage_metadata.get("promptTokenCount", 0)
        output_tokens = usage_metadata.get("candidatesTokenCount", 0)
        total_tokens = usage_metadata.get("totalTokenCount", 0)
        cache_read_tokens = usage_metadata.get("cachedContentTokenCount", 0)
        if input_tokens + output_tokens + cache_read_tokens + total_tokens > 0:
            lc_usage = UsageMetadata(
                input_tokens=input_tokens - prev_input_tokens,
                output_tokens=output_tokens - prev_output_tokens,
                total_tokens=total_tokens - prev_total_tokens,
                input_token_details={"cache_read": cache_read_tokens},
            )
        else:
            lc_usage = None
    except AttributeError:
        lc_usage = None

    generations: List[ChatGeneration] = []

    for candidate in response.get("candidates", []):
        generation_info = {}
        if candidate.get("finishReason"):
            generation_info["finish_reason"] = candidate["finishReason"]
        generation_info["safety_ratings"] = candidate.get("safetyRatings", [])
        message = _parse_response_candidate(candidate, streaming=stream)
        message.usage_metadata = lc_usage
        if stream:
            generations.append(
                ChatGenerationChunk(
                    message=cast(AIMessageChunk, message),
                    generation_info=generation_info,
                )
            )
        else:
            generations.append(
                ChatGeneration(message=message, generation_info=generation_info)
            )
    if not response.get("candidates"):
        # Likely a "prompt feedback" violation (e.g., toxic input)
        # Raising an error would be different than how OpenAI handles it,
        # so we'll just log a warning and continue with an empty message.
        logger.warning(
            "Gemini produced an empty response. Continuing with empty message\n"
            f"Feedback: {response.get('promptFeedback')}"
        )
        if stream:
            generations = [
                ChatGenerationChunk(
                    message=AIMessageChunk(content=""), generation_info={}
                )
            ]
        else:
            generations = [ChatGeneration(message=AIMessage(""), generation_info={})]
    return ChatResult(generations=generations, llm_output=llm_output)


def _is_event_loop_running() -> bool:
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


class GeminiRestClient:
    """A REST client for making requests to the Gemini API."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self._client = None
        self._async_client = None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={
                    "Content-Type": "application/json",
                    **self.headers,
                },
                timeout=self.timeout,
            )
        return self._client

    async def _get_async_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    "Content-Type": "application/json",
                    **self.headers,
                },
                timeout=self.timeout,
            )
        return self._async_client

    def _convert_to_dict(self, obj: Any) -> Any:
        """Convert Pydantic models and other objects to dictionaries."""
        if hasattr(obj, 'model_dump'):
            return obj.model_dump()
        elif isinstance(obj, list):
            return [self._convert_to_dict(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self._convert_to_dict(v) for k, v in obj.items()}
        return obj

    def _prepare_payload(
        self,
        contents: List[Dict[str, Any]],
        generation_config: Optional[Dict[str, Any]] = None,
        safety_settings: Optional[List[Dict[str, Any]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_config: Optional[Dict[str, Any]] = None,
        system_instruction: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Prepare the payload for Gemini API requests."""
        payload = {
            "contents": self._convert_to_dict(contents),
            "generationConfig": self._convert_to_dict(generation_config or {}),
            "safetySettings": self._convert_to_dict(safety_settings or []),
        }
        if tools:
            payload["tools"] = self._convert_to_dict(tools)
        if tool_config:
            payload["toolConfig"] = self._convert_to_dict(tool_config)
        if system_instruction:
            payload["systemInstruction"] = self._convert_to_dict(system_instruction)
        if cached_content:
            payload["cachedContent"] = cached_content
        return payload

    def generate_content(
        self,
        model: str,
        contents: List[Dict[str, Any]],
        generation_config: Optional[Dict[str, Any]] = None,
        safety_settings: Optional[List[Dict[str, Any]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_config: Optional[Dict[str, Any]] = None,
        system_instruction: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate content using the Gemini API."""
        payload = self._prepare_payload(
            contents=contents,
            generation_config=generation_config,
            safety_settings=safety_settings,
            tools=tools,
            tool_config=tool_config,
            system_instruction=system_instruction,
            cached_content=cached_content,
        )

        response = self._get_client().post(
            f"v1beta/{model}:generateContent",
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def generate_content_async(
        self,
        model: str,
        contents: List[Dict[str, Any]],
        generation_config: Optional[Dict[str, Any]] = None,
        safety_settings: Optional[List[Dict[str, Any]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_config: Optional[Dict[str, Any]] = None,
        system_instruction: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate content asynchronously using the Gemini API."""
        payload = self._prepare_payload(
            contents=contents,
            generation_config=generation_config,
            safety_settings=safety_settings,
            tools=tools,
            tool_config=tool_config,
            system_instruction=system_instruction,
            cached_content=cached_content,
        )
        client = await self._get_async_client()
        response = await client.post(
            f"v1beta/{model}:generateContent",
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    def stream_generate_content(
        self,
        model: str,
        contents: List[Dict[str, Any]],
        generation_config: Optional[Dict[str, Any]] = None,
        safety_settings: Optional[List[Dict[str, Any]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_config: Optional[Dict[str, Any]] = None,
        system_instruction: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Stream content generation using the Gemini API."""
        payload = self._prepare_payload(
            contents=contents,
            generation_config=generation_config,
            safety_settings=safety_settings,
            tools=tools,
            tool_config=tool_config,
            system_instruction=system_instruction,
            cached_content=cached_content,
        )


        with self._get_client().stream(
            "POST",
            f"v1beta/{model}:streamGenerateContent",
            json=payload,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    yield json.loads(line)

    async def stream_generate_content_async(
        self,
        model: str,
        contents: List[Dict[str, Any]],
        generation_config: Optional[Dict[str, Any]] = None,
        safety_settings: Optional[List[Dict[str, Any]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_config: Optional[Dict[str, Any]] = None,
        system_instruction: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
    ) -> AsyncIterator[Dict[str, Any]]:
        """Stream content generation asynchronously using the Gemini API."""
        payload = self._prepare_payload(
            contents=contents,
            generation_config=generation_config,
            safety_settings=safety_settings,
            tools=tools,
            tool_config=tool_config,
            system_instruction=system_instruction,
            cached_content=cached_content,
        )

        client = await self._get_async_client()
        async with client.stream(
            "POST",
            f"v1beta/{model}:streamGenerateContent",
            json=payload,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line:
                    yield json.loads(line)

    def count_tokens(
        self,
        model: str,
        contents: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Count tokens in the input using the Gemini API."""
        payload = {"contents": self._convert_to_dict(contents)}
        response = self._get_client().post(
            f"v1beta/{model}:countTokens",
            json=payload,
        )
        response.raise_for_status()
        return response.json()


class ChatGoogleGenerativeAI(BaseChatModel):
    """`Google AI` chat models integration."""

    client: Optional[GeminiRestClient] = Field(default=None, exclude=True)
    async_client: Optional[GeminiRestClient] = Field(default=None, exclude=True)
    default_metadata: Sequence[Tuple[str, str]] = Field(default_factory=list)
    convert_system_message_to_human: bool = False
    cached_content: Optional[str] = None
    model: str = Field(default="gemini-pro")
    google_api_key: Optional[SecretStr] = Field(default=None)
    temperature: Optional[float] = Field(default=None)
    top_p: Optional[float] = Field(default=None)
    top_k: Optional[int] = Field(default=None)
    n: int = Field(default=1)
    max_output_tokens: Optional[int] = Field(default=None)
    safety_settings: Optional[Dict[str, str]] = Field(default=None)
    response_modalities: Optional[List[str]] = Field(default=None)
    client_options: Optional[Dict[str, Any]] = Field(default=None)
    additional_headers: Optional[Dict[str, str]] = Field(default=None)
    transport: Optional[str] = Field(default="rest")

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {"google_api_key": "GOOGLE_API_KEY"}

    @property
    def _llm_type(self) -> str:
        return "chat-google-generative-ai"

    @classmethod
    def is_lc_serializable(self) -> bool:
        return True

    @model_validator(mode="after")
    def validate_environment(self) -> Self:
        """Validates params and initializes the REST client."""
        if self.temperature is not None and not 0 <= self.temperature <= 2.0:
            raise ValueError("temperature must be in the range [0.0, 2.0]")

        if self.top_p is not None and not 0 <= self.top_p <= 1:
            raise ValueError("top_p must be in the range [0.0, 1.0]")

        if self.top_k is not None and self.top_k <= 0:
            raise ValueError("top_k must be positive")

        additional_headers = self.additional_headers or {}
        self.default_metadata = tuple(additional_headers.items())

        google_api_key = None
        if isinstance(self.google_api_key, SecretStr):
            google_api_key = self.google_api_key.get_secret_value()
        else:
            google_api_key = self.google_api_key

        base_url = self.client_options.get("api_endpoint", "https://generativelanguage.googleapis.com")
        self.client = GeminiRestClient(
            api_key=google_api_key,
            base_url=base_url,
            headers=additional_headers,
        )
        self.async_client = GeminiRestClient(
            api_key=google_api_key,
            base_url=base_url,
            headers=additional_headers,
        )
        return self

    def _get_ls_params(
        self, stop: Optional[List[str]] = None, **kwargs: Any
    ) -> LangSmithParams:
        """Get standard params for tracing."""
        params = self._get_invocation_params(stop=stop, **kwargs)
        ls_params = LangSmithParams(
            ls_provider="google_genai",
            ls_model_name=self.model,
            ls_model_type="chat",
            ls_temperature=params.get("temperature", self.temperature),
        )
        if ls_max_tokens := params.get("max_output_tokens", self.max_output_tokens):
            ls_params["ls_max_tokens"] = ls_max_tokens
        if ls_stop := stop or params.get("stop", None):
            ls_params["ls_stop"] = ls_stop
        return ls_params

    def _prepare_params(
        self,
        stop: Optional[List[str]],
        generation_config: Optional[Dict[str, Any]] = None,
    ) -> GenerationConfig:
        gen_config = {
            k: v
            for k, v in {
                "candidate_count": self.n,
                "temperature": self.temperature,
                "stop_sequences": stop,
                "max_output_tokens": self.max_output_tokens,
                "top_k": self.top_k,
                "top_p": self.top_p,
                "response_modalities": self.response_modalities,
            }.items()
            if v is not None
        }
        if generation_config:
            gen_config = {**gen_config, **generation_config}
        return GenerationConfig(**gen_config)

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        *,
        tools: Optional[Sequence[Union[_ToolDict, GoogleTool]]] = None,
        functions: Optional[Sequence[_FunctionDeclarationType]] = None,
        safety_settings: Optional[SafetySettingDict] = None,
        tool_config: Optional[Union[Dict, _ToolConfigDict]] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
        tool_choice: Optional[Union[_ToolChoiceType, bool]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        request = self._prepare_request(
            messages,
            stop=stop,
            tools=tools,
            functions=functions,
            safety_settings=safety_settings,
            tool_config=tool_config,
            generation_config=generation_config,
            cached_content=cached_content or self.cached_content,
            tool_choice=tool_choice,
        )
        response = _chat_with_retry(
            request=request,
            **kwargs,
            generation_method=self.client.generate_content,
            metadata=self.default_metadata,
        )
        return _response_to_result(response)

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        *,
        tools: Optional[Sequence[Union[_ToolDict, GoogleTool]]] = None,
        functions: Optional[Sequence[_FunctionDeclarationType]] = None,
        safety_settings: Optional[SafetySettingDict] = None,
        tool_config: Optional[Union[Dict, _ToolConfigDict]] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
        tool_choice: Optional[Union[_ToolChoiceType, bool]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        request = self._prepare_request(
            messages,
            stop=stop,
            tools=tools,
            functions=functions,
            safety_settings=safety_settings,
            tool_config=tool_config,
            generation_config=generation_config,
            cached_content=cached_content or self.cached_content,
            tool_choice=tool_choice,
        )
        response = await _achat_with_retry(
            request=request,
            **kwargs,
            generation_method=self.async_client.generate_content_async,
            metadata=self.default_metadata,
        )
        return _response_to_result(response)

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        *,
        tools: Optional[Sequence[Union[_ToolDict, GoogleTool]]] = None,
        functions: Optional[Sequence[_FunctionDeclarationType]] = None,
        safety_settings: Optional[SafetySettingDict] = None,
        tool_config: Optional[Union[Dict, _ToolConfigDict]] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
        tool_choice: Optional[Union[_ToolChoiceType, bool]] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        request = self._prepare_request(
            messages,
            stop=stop,
            tools=tools,
            functions=functions,
            safety_settings=safety_settings,
            tool_config=tool_config,
            generation_config=generation_config,
            cached_content=cached_content or self.cached_content,
            tool_choice=tool_choice,
        )
        response = _chat_with_retry(
            request=request,
            generation_method=self.client.stream_generate_content,
            **kwargs,
            metadata=self.default_metadata,
        )

        prev_usage_metadata: UsageMetadata | None = None
        for chunk in response:
            _chat_result = _response_to_result(
                chunk, stream=True, prev_usage=prev_usage_metadata
            )
            gen = cast(ChatGenerationChunk, _chat_result.generations[0])
            message = cast(AIMessageChunk, gen.message)

            curr_usage_metadata: UsageMetadata | dict[str, int] = (
                message.usage_metadata or {}
            )

            prev_usage_metadata = (
                message.usage_metadata
                if prev_usage_metadata is None
                else UsageMetadata(
                    input_tokens=prev_usage_metadata.get("input_tokens", 0)
                    + curr_usage_metadata.get("input_tokens", 0),
                    output_tokens=prev_usage_metadata.get("output_tokens", 0)
                    + curr_usage_metadata.get("output_tokens", 0),
                    total_tokens=prev_usage_metadata.get("total_tokens", 0)
                    + curr_usage_metadata.get("total_tokens", 0),
                )
            )

            if run_manager:
                run_manager.on_llm_new_token(gen.text)
            yield gen

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        *,
        tools: Optional[Sequence[Union[_ToolDict, GoogleTool]]] = None,
        functions: Optional[Sequence[_FunctionDeclarationType]] = None,
        safety_settings: Optional[SafetySettingDict] = None,
        tool_config: Optional[Union[Dict, _ToolConfigDict]] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
        tool_choice: Optional[Union[_ToolChoiceType, bool]] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        request = self._prepare_request(
            messages,
            stop=stop,
            tools=tools,
            functions=functions,
            safety_settings=safety_settings,
            tool_config=tool_config,
            generation_config=generation_config,
            cached_content=cached_content or self.cached_content,
            tool_choice=tool_choice,
        )
        prev_usage_metadata: UsageMetadata | None = None
        async for chunk in await _achat_with_retry(
            request=request,
            generation_method=self.async_client.stream_generate_content_async,
            **kwargs,
            metadata=self.default_metadata,
        ):
            _chat_result = _response_to_result(
                chunk, stream=True, prev_usage=prev_usage_metadata
            )
            gen = cast(ChatGenerationChunk, _chat_result.generations[0])
            message = cast(AIMessageChunk, gen.message)

            curr_usage_metadata: UsageMetadata | dict[str, int] = (
                message.usage_metadata or {}
            )

            prev_usage_metadata = (
                message.usage_metadata
                if prev_usage_metadata is None
                else UsageMetadata(
                    input_tokens=prev_usage_metadata.get("input_tokens", 0)
                    + curr_usage_metadata.get("input_tokens", 0),
                    output_tokens=prev_usage_metadata.get("output_tokens", 0)
                    + curr_usage_metadata.get("output_tokens", 0),
                    total_tokens=prev_usage_metadata.get("total_tokens", 0)
                    + curr_usage_metadata.get("total_tokens", 0),
                )
            )

            if run_manager:
                await run_manager.on_llm_new_token(gen.text)
            yield gen

    def _prepare_request(
        self,
        messages: List[BaseMessage],
        *,
        stop: Optional[List[str]] = None,
        tools: Optional[Sequence[Union[_ToolDict, GoogleTool]]] = None,
        functions: Optional[Sequence[_FunctionDeclarationType]] = None,
        safety_settings: Optional[SafetySettingDict] = None,
        tool_config: Optional[Union[Dict, _ToolConfigDict]] = None,
        tool_choice: Optional[Union[_ToolChoiceType, bool]] = None,
        generation_config: Optional[Dict[str, Any]] = None,
        cached_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        if tool_choice and tool_config:
            raise ValueError(
                "Must specify at most one of tool_choice and tool_config, received "
                f"both:\n\n{tool_choice=}\n\n{tool_config=}"
            )
        formatted_tools = None
        if tools:
            formatted_tools = [convert_to_genai_function_declarations(tools)]
        elif functions:
            formatted_tools = [convert_to_genai_function_declarations(functions)]

        filtered_messages = []
        for message in messages:
            if isinstance(message, HumanMessage) and not message.content:
                warnings.warn(
                    "HumanMessage with empty content was removed to prevent API error"
                )
            else:
                filtered_messages.append(message)
        messages = filtered_messages

        system_instruction, history = _parse_chat_history(
            messages,
            convert_system_message_to_human=self.convert_system_message_to_human,
        )
        if tool_choice:
            if not formatted_tools:
                msg = (
                    f"Received {tool_choice=} but no {tools=}. 'tool_choice' can only "
                    f"be specified if 'tools' is specified."
                )
                raise ValueError(msg)
            all_names = [
                f.name for t in formatted_tools for f in t.function_declarations
            ]
            tool_config = _tool_choice_to_tool_config(tool_choice, all_names)

        formatted_tool_config = None
        if tool_config:
            formatted_tool_config = ToolConfig(
                function_calling_config=tool_config["function_calling_config"]
            )
        formatted_safety_settings = []
        if safety_settings:
            formatted_safety_settings = [
                SafetySetting(category=c, threshold=t)
                for c, t in safety_settings.items()
            ]

        # Construct the full model path
        model_path = f"models/{self.model}"

        request = {
            "model": model_path,
            "contents": history,
            "tools": formatted_tools,
            "tool_config": formatted_tool_config,
            "safety_settings": formatted_safety_settings,
            "generation_config": self._prepare_params(
                stop, generation_config=generation_config
            ),
            "cached_content": cached_content,
        }
        if system_instruction:
            request["system_instruction"] = system_instruction

        return request

    def get_num_tokens(self, text: str) -> int:
        """Get the number of tokens present in the text.

        Useful for checking if an input will fit in a model's context window.

        Args:
            text: The string input to tokenize.

        Returns:
            The integer number of tokens in the text.
        """
        result = self.client.count_tokens(
            model=self.model,
            contents=[{"parts": [{"text": text}]}],
        )
        return result["total_tokens"]

    def with_structured_output(
        self,
        schema: Union[Dict, Type[BaseModel]],
        *,
        include_raw: bool = False,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, Union[Dict, BaseModel]]:
        _ = kwargs.pop("method", None)
        _ = kwargs.pop("strict", None)
        if kwargs:
            raise ValueError(f"Received unsupported arguments {kwargs}")
        tool_name = _get_tool_name(schema)  # type: ignore[arg-type]
        if isinstance(schema, type) and is_basemodel_subclass_safe(schema):
            parser: OutputParserLike = PydanticToolsParser(
                tools=[schema], first_tool_only=True
            )
        else:
            global WARNED_STRUCTURED_OUTPUT_JSON_MODE
            warnings.warn(
                "ChatGoogleGenerativeAI.with_structured_output with dict schema has "
                "changed recently to align with behavior of other LangChain chat "
                "models. More context: "
                "https://github.com/langchain-ai/langchain-google/pull/772"
            )
            WARNED_STRUCTURED_OUTPUT_JSON_MODE = True
            parser = JsonOutputKeyToolsParser(key_name=tool_name, first_tool_only=True)
        tool_choice = tool_name if self._supports_tool_choice else None
        try:
            llm = self.bind_tools(
                [schema],
                tool_choice=tool_choice,
                ls_structured_output_format={
                    "kwargs": {"method": "function_calling"},
                    "schema": convert_to_openai_tool(schema),
                },
            )
        except Exception:
            llm = self.bind_tools([schema], tool_choice=tool_choice)
        if include_raw:
            parser_with_fallback = RunnablePassthrough.assign(
                parsed=itemgetter("raw") | parser, parsing_error=lambda _: None
            ).with_fallbacks(
                [RunnablePassthrough.assign(parsed=lambda _: None)],
                exception_key="parsing_error",
            )
            return {"raw": llm} | parser_with_fallback
        else:
            return llm | parser

    def bind_tools(
        self,
        tools: Sequence[
            dict[str, Any] | type | Callable[..., Any] | BaseTool | GoogleTool
        ],
        tool_config: Optional[Union[Dict, _ToolConfigDict]] = None,
        *,
        tool_choice: Optional[Union[_ToolChoiceType, bool]] = None,
        **kwargs: Any,
    ) -> Runnable[LanguageModelInput, BaseMessage]:
        """Bind tool-like objects to this chat model.

        Assumes model is compatible with google-generativeAI tool-calling API.

        Args:
            tools: A list of tool definitions to bind to this chat model.
                Can be a pydantic model, callable, or BaseTool. Pydantic
                models, callables, and BaseTools will be automatically converted to
                their schema dictionary representation.
            **kwargs: Any additional parameters to pass to the
                :class:`~langchain.runnable.Runnable` constructor.
        """
        if tool_choice and tool_config:
            raise ValueError(
                "Must specify at most one of tool_choice and tool_config, received "
                f"both:\n\n{tool_choice=}\n\n{tool_config=}"
            )
        try:
            formatted_tools: list = [convert_to_openai_tool(tool) for tool in tools]  # type: ignore[arg-type]
        except Exception:
            formatted_tools = [
                tool_to_dict(convert_to_genai_function_declarations(tools))
            ]
        if tool_choice:
            kwargs["tool_choice"] = tool_choice
        elif tool_config:
            kwargs["tool_config"] = tool_config
        else:
            pass
        return self.bind(tools=formatted_tools, **kwargs)

    @property
    def _supports_tool_choice(self) -> bool:
        return (
            "gemini-1.5-pro" in self.model
            or "gemini-1.5-flash" in self.model
            or "gemini-2" in self.model
        )


def _get_tool_name(
    tool: Union[_ToolDict, GoogleTool, Dict],
) -> str:
    try:
        genai_tool = tool_to_dict(convert_to_genai_function_declarations([tool]))
        return [f["name"] for f in genai_tool["function_declarations"]][0]  # type: ignore[index]
    except ValueError as e:  # other TypedDict
        if is_typeddict(tool):
            return convert_to_openai_tool(cast(Dict, tool))["function"]["name"]
        else:
            raise e

def _tool_choice_to_tool_config(
    tool_choice: Union[str, bool, Dict[str, Any]], all_names: List[str]
) -> Dict[str, Any]:
    """Convert tool_choice to tool_config format."""
    if isinstance(tool_choice, bool):
        return {
            "function_calling_config": {
                "mode": "AUTO" if tool_choice else "NONE",
            }
        }
    elif isinstance(tool_choice, str):
        if tool_choice not in all_names:
            raise ValueError(
                f"Tool choice {tool_choice} not found in available tools: {all_names}"
            )
        return {
            "function_calling_config": {
                "mode": "ANY",
                "allowed_function_names": [tool_choice],
            }
        }
    else:
        return tool_choice

def convert_to_genai_function_declarations(
    tools: Sequence[Union[Dict[str, Any], Type[BaseModel], Callable[..., Any], BaseTool]]
) -> Dict[str, Any]:
    """Convert tools to Gemini function declarations format."""
    function_declarations = []
    for tool in tools:
        if isinstance(tool, dict):
            fn = tool.get("function", {})
            fn_parameters = fn.get("parameters", {})
            function_declarations.append({
                "name": fn.get("name", ""),
                "description": fn.get("description", ""),
                "parameters": {
                    "type": "object",
                    "properties": fn_parameters.get("properties", {}),
                    "required": fn_parameters.get("required", []),
                },
            })
        elif isinstance(tool, type) and issubclass(tool, BaseModel):
            schema = tool.model_json_schema()
            function_declarations.append({
                "name": schema.get("title", ""),
                "description": schema.get("description", ""),
                "parameters": {
                    "type": "object",
                    "properties": {
                        name: {
                            "type": prop.get("type", "string"),
                            "description": prop.get("description", ""),
                        }
                        for name, prop in schema.get("properties", {}).items()
                    },
                    "required": schema.get("required", []),
                },
            })
        elif callable(tool):
            # For callables, we'll create a basic function declaration
            function_declarations.append({
                "name": tool.__name__,
                "description": tool.__doc__ or "",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            })
        elif isinstance(tool, BaseTool):
            function_declarations.append({
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            })
    return {"functionDeclarations": function_declarations}

def is_basemodel_subclass_safe(cls: Type[Any]) -> bool:
    """Check if a class is a safe subclass of BaseModel."""
    try:
        return issubclass(cls, BaseModel)
    except TypeError:
        return False

def tool_to_dict(tool: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a tool to a dictionary format."""
    return tool

def image_bytes_to_b64_string(image_bytes: bytes, image_format: str = "jpeg") -> str:
    """Convert image bytes to base64 string."""
    import base64
    return f"data:image/{image_format};base64,{base64.b64encode(image_bytes).decode('utf-8')}"

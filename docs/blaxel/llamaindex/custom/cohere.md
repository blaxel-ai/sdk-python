Module blaxel.llamaindex.custom.cohere
======================================

Classes
-------

`Cohere(model: str = 'command-r', temperature: float | None = None, max_tokens: int | None = 8192, timeout: float | None = None, max_retries: int = 10, api_key: str | None = None, api_base: str | None = None, additional_kwargs: Dict[str, Any] | None = None, callback_manager: llama_index.core.callbacks.base.CallbackManager | None = None, system_prompt: str | None = None, messages_to_prompt: Callable[[Sequence[llama_index.core.base.llms.types.ChatMessage]], str] | None = None, completion_to_prompt: Callable[[str], str] | None = None, pydantic_program_mode: llama_index.core.types.PydanticProgramMode = PydanticProgramMode.DEFAULT, output_parser: llama_index.core.types.BaseOutputParser | None = None)`
:   Cohere LLM.
    
    Examples:
        `pip install llama-index-llms-cohere`
    
        ```python
        from llama_index.llms.cohere import Cohere
    
        llm = Cohere(model="command", api_key=api_key)
        resp = llm.complete("Paul Graham is ")
        print(resp)
        ```
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * llama_index.core.llms.function_calling.FunctionCallingLLM
    * llama_index.core.llms.llm.LLM
    * llama_index.core.base.llms.base.BaseLLM
    * llama_index.core.base.query_pipeline.query.ChainableMixin
    * llama_index.core.schema.BaseComponent
    * pydantic.main.BaseModel
    * llama_index.core.instrumentation.DispatcherSpanMixin
    * abc.ABC

    ### Class variables

    `additional_kwargs: Dict[str, Any]`
    :

    `max_retries: int`
    :

    `max_tokens: int`
    :

    `model: str`
    :

    `model_config`
    :

    `temperature: float | None`
    :

    ### Static methods

    `class_name() ‑> str`
    :   Get class name.

    ### Instance variables

    `metadata: llama_index.core.base.llms.types.LLMMetadata`
    :   LLM metadata.
        
        Returns:
            LLMMetadata: LLM metadata containing various information about the LLM.

    ### Methods

    `achat(_self, messages: Sequence[llama_index.core.base.llms.types.ChatMessage], **kwargs: Any) ‑> llama_index.core.base.llms.types.ChatResponse`
    :

    `acomplete(_self, *args, **kwargs: Any) ‑> llama_index.core.base.llms.types.CompletionResponse`
    :

    `astream_chat(_self, messages: Sequence[llama_index.core.base.llms.types.ChatMessage], **kwargs: Any) ‑> AsyncGenerator[llama_index.core.base.llms.types.ChatResponse, None]`
    :

    `astream_complete(_self, *args, **kwargs: Any) ‑> AsyncGenerator[llama_index.core.base.llms.types.CompletionResponse, None]`
    :

    `chat(_self, messages: Sequence[llama_index.core.base.llms.types.ChatMessage], **kwargs: Any) ‑> llama_index.core.base.llms.types.ChatResponse`
    :

    `complete(_self, *args, **kwargs: Any) ‑> llama_index.core.base.llms.types.CompletionResponse`
    :

    `get_cohere_chat_request(self, messages: List[llama_index.core.base.llms.types.ChatMessage], *, connectors: List[Dict[str, str]] | None = None, stop_sequences: List[str] | None = None, **kwargs: Any) ‑> Dict[str, Any]`
    :   Get the request for the Cohere chat API.
        
        Args:
            messages: The messages.
            connectors: The connectors.
            **kwargs: The keyword arguments.
        
        Returns:
            The request for the Cohere chat API.

    `get_tool_calls_from_response(self, response: ChatResponse, error_on_no_tool_call: bool = False) ‑> List[llama_index.core.llms.llm.ToolSelection]`
    :   Predict and call the tool.

    `model_post_init(self: BaseModel, context: Any, /) ‑> None`
    :   This function is meant to behave like a BaseModel method to initialise private attributes.
        
        It takes context as an argument since that's what pydantic-core passes when calling it.
        
        Args:
            self: The BaseModel instance.
            context: The context.

    `stream_chat(_self, messages: Sequence[llama_index.core.base.llms.types.ChatMessage], **kwargs: Any) ‑> Generator[llama_index.core.base.llms.types.ChatResponse, None, None]`
    :

    `stream_complete(_self, *args, **kwargs: Any) ‑> Generator[llama_index.core.base.llms.types.CompletionResponse, None, None]`
    :
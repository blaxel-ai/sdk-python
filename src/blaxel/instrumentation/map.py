INSTUMENTATION_MAPPINGS = {
    "httpx": (
        "opentelemetry.instrumentation.httpx",
        "HTTPXClientInstrumentor",
        "httpx",
    ),
    "anthropic": (
        "opentelemetry.instrumentation.anthropic",
        "AnthropicInstrumentor",
        "anthropic",
    ),
    "chroma": (
        "opentelemetry.instrumentation.chroma",
        "ChromaInstrumentor",
        "chromadb",
    ),
    "cohere": (
        "opentelemetry.instrumentation.cohere",
        "CohereInstrumentor",
        "cohere",
    ),
    "groq": ("opentelemetry.instrumentation.groq", "GroqInstrumentor", "groq"),
    "lance": (
        "opentelemetry.instrumentation.lance",
        "LanceInstrumentor",
        "pylance",
    ),
    "langchain": (
        "opentelemetry.instrumentation.langchain",
        "LangchainInstrumentor",
        "langchain",
    ),
    "llama_index": (
        "opentelemetry.instrumentation.llama_index",
        "LlamaIndexInstrumentor",
        "llama_index",
    ),
    "marqo": (
        "opentelemetry.instrumentation.marqo",
        "MarqoInstrumentor",
        "marqo",
    ),
    "milvus": (
        "opentelemetry.instrumentation.milvus",
        "MilvusInstrumentor",
        "pymilvus",
    ),
    "mistralai": (
        "opentelemetry.instrumentation.mistralai",
        "MistralAiInstrumentor",
        "mistralai",
    ),
    "ollama": (
        "opentelemetry.instrumentation.ollama",
        "OllamaInstrumentor",
        "ollama",
    ),
    "openai": (
        "opentelemetry.instrumentation.openai",
        "OpenAIInstrumentor",
        "openai",
    ),
    "pinecone": (
        "opentelemetry.instrumentation.pinecone",
        "PineconeInstrumentor",
        "pinecone",
    ),
    "qdrant": (
        "opentelemetry.instrumentation.qdrant",
        "QdrantInstrumentor",
        "qdrant_client",
    ),
    "replicate": (
        "opentelemetry.instrumentation.replicate",
        "ReplicateInstrumentor",
        "replicate",
    ),
    "together": (
        "opentelemetry.instrumentation.together",
        "TogetherAiInstrumentor",
        "together",
    ),
    "watsonx": (
        "opentelemetry.instrumentation.watsonx",
        "WatsonxInstrumentor",
        "ibm_watson_machine_learning",
    ),
    "weaviate": (
        "opentelemetry.instrumentation.weaviate",
        "WeaviateInstrumentor",
        "weaviate",
    ),
}

from enum import Enum


class ModelRuntimeType(str, Enum):
    ANTHROPIC = "anthropic"
    AZURE_AI_INFERENCE = "azure-ai-inference"
    AZURE_MARKETPLACE = "azure-marketplace"
    AZURE_OPENAI_SERVICE = "azure-openai-service"
    CEREBRAS = "cerebras"
    COHERE = "cohere"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    GROQ = "groq"
    HF_PRIVATE_ENDPOINT = "hf_private_endpoint"
    HF_PUBLIC_ENDPOINT = "hf_public_endpoint"
    HUGGINGFACE = "huggingface"
    MCP = "mcp"
    MISTRAL = "mistral"
    OPENAI = "openai"
    PUBLIC_MODEL = "public_model"
    VERTEXAI = "vertexai"
    XAI = "xai"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _missing_(cls, value: object) -> "ModelRuntimeType | None":
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value.upper() == upper_value:
                    return member
        return None

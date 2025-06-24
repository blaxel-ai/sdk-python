from typing import Dict, List

from pydantic import BaseModel


class InstrumentationMapping(BaseModel):
    module_path: str
    class_name: str
    required_packages: List[str]
    ignore_if_packages: List[str]


MAPPINGS: Dict[str, InstrumentationMapping] = {
    "anthropic": InstrumentationMapping(
        module_path="opentelemetry.instrumentation.anthropic",
        class_name="AnthropicInstrumentor",
        required_packages=["anthropic"],
        ignore_if_packages=[],
    ),
    "cohere": InstrumentationMapping(
        module_path="opentelemetry.instrumentation.cohere",
        class_name="CohereInstrumentor",
        required_packages=["cohere"],
        ignore_if_packages=[],
    ),
    "openai": InstrumentationMapping(
        module_path="opentelemetry.instrumentation.openai",
        class_name="OpenAIInstrumentor",
        required_packages=["openai"],
        ignore_if_packages=[],
    ),
    "gemini": InstrumentationMapping(
        module_path="opentelemetry.instrumentation.google_generativeai",
        class_name="GoogleGenerativeAIInstrumentor",
        required_packages=["google-generativeai"],
        ignore_if_packages=[],
    ),
    "blaxel_core": InstrumentationMapping(
        module_path="blaxel.telemetry.instrumentation.blaxel_core",
        class_name="BlaxelCoreInstrumentor",
        required_packages=[],
        ignore_if_packages=[],
    ),
    "blaxel_langgraph": InstrumentationMapping(
        module_path="blaxel.telemetry.instrumentation.blaxel_langgraph",
        class_name="BlaxelLanggraphInstrumentor",
        required_packages=["langgraph"],
        ignore_if_packages=[],
    ),
    "blaxel_langgraph_gemini": InstrumentationMapping(
        module_path="blaxel.telemetry.instrumentation.blaxel_langgraph_gemini",
        class_name="BlaxelLanggraphGeminiInstrumentor",
        required_packages=["langgraph"],
        ignore_if_packages=[],
    ),
    "blaxel_llamaindex": InstrumentationMapping(
        module_path="blaxel.telemetry.instrumentation.blaxel_llamaindex",
        class_name="BlaxelLlamaIndexInstrumentor",
        required_packages=["llama_index"],
        ignore_if_packages=[],
    ),
}

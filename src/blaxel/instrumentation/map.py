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
        ignore_if_packages=[]
    ),
    "cohere": InstrumentationMapping(
        module_path="opentelemetry.instrumentation.cohere",
        class_name="CohereInstrumentor",
        required_packages=["cohere"],
        ignore_if_packages=[]
    ),
    "langchain": InstrumentationMapping(
        module_path="opentelemetry.instrumentation.langchain",
        class_name="LangchainInstrumentor",
        required_packages=["langchain"],
        ignore_if_packages=[]
    ),
    "llamaindex": InstrumentationMapping(
        module_path="opentelemetry.instrumentation.llamaindex",
        class_name="LlamaIndexInstrumentor",
        required_packages=["llama_index"],
        ignore_if_packages=[]
    ),
    "crewai": InstrumentationMapping(
        module_path="opentelemetry.instrumentation.crewai",
        class_name="CrewAIInstrumentor",
        required_packages=["crewai"],
        ignore_if_packages=[]
    ),
    "openai": InstrumentationMapping(
        module_path="opentelemetry.instrumentation.openai",
        class_name="OpenAIInstrumentor",
        required_packages=["openai"],
        ignore_if_packages=[]
    ),
}

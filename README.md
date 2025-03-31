# Blaxel Python SDK

<p align="center">
  <img src="https://blaxel.ai/logo.png" alt="Blaxel"/>
</p>

An SDK to connect your agent or tools with Blaxel platform.
Currently in preview, feel free to send us feedback or contribute to the project.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Start from an hello world example](#start-from-an-hello-world-example)
- [Integrate with a custom code](#integrate-with-a-custom-code)
  - [Set-up blaxel observability](#set-up-blaxel-observability)
  - [Connect tools and model from blaxel platform to your agent](#connect-tools-and-model-from-blaxel-platform-to-your-agent)
  - [Agent Chaining](#agent-chaining)
  - [Deploy on blaxel](#deploy-on-blaxel)
  - [Advanced configuration](#advanced-configuration)
  - [Create an MCP Server](#create-an-mcp-server)
  - [Connect an existing MCP Server to blaxel](#connect-an-existing-mcp-server-to-blaxel)
  - [How to use environment variables or secrets](#how-to-use-environment-variables-or-secrets)
- [Contributing](#contributing)
- [License](#license)

## Features

Supported AI frameworks:

- LangChain
- LlamaIndex
- CrewAI
- OpenAI Agents

Supported Tools frameworks:

- MCP (Model Context Protocol)

## Prerequisites

- **Python:** 3.10 or later
- **Blaxel CLI:** Ensure you have the Blaxel CLI installed. If not, install it globally:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/beamlit/toolkit/preview/install.sh | BINDIR=$HOME/.local/bin sh
  ```
- **Blaxel login:** Login to Blaxel platform
  ```bash
    bl login YOUR-WORKSPACE
  ```

## Start from an hello world example

```bash
bl create-agent-app myfolder
cd myfolder
bl serve --hotreload
```

## Integrate with a custom code

### Set-up blaxel observability

It only needs an import of our SDK on top of your main entrypoint file.
It will directly plug our backend (when deployed on blaxel) with open telemetry standard.

```python
from blaxel import sdk
```

### Connect tools and model from blaxel platform to your agent

```python
from blaxel.models import bl_model
from blaxel.tools import bl_tools
```

Then you need to use it in your agent. Here are examples with different frameworks:

```python
# Example with LangChain
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool
from langchain_core.messages import HumanMessage

async def create_agent():
    model = await bl_model("gpt-4o-mini").to_langchain()
    async with bl_tools(["blaxel-search", "webcrawl"]) as t:
        tools = t.to_langchain()
        tools.append(
            Tool(
                name="weather",
                description="Get the weather in a specific city",
                func=lambda city: f"The weather in {city} is sunny"
            )
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("human", "{input}")
        ])

        agent = create_react_agent(model, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools)

# Example with LlamaIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool

async def create_llamaindex_agent():
    model = await bl_model("gpt-4o-mini").to_llamaindex()
    async with bl_tools(["blaxel-search", "webcrawl"]) as t:
        tools = t.to_llamaindex()
        tools.append(
            FunctionTool.from_defaults(
                fn=lambda city: f"The weather in {city} is sunny",
                name="weather",
                description="Get the weather in a specific city"
            )
        )

        return ReActAgent.from_tools(
            tools,
            llm=model,
            verbose=True
        )

# Example with CrewAI
from crewai import Agent, Task, Crew

async def create_crewai_agent():
    model = await bl_model("gpt-4o-mini").to_crewai()
    async with bl_tools(["blaxel-search", "webcrawl"]) as t:
        tools = t.to_crewai()
        tools.append(
            Tool(
                name="weather",
                description="Get the weather in a specific city",
                func=lambda city: f"The weather in {city} is sunny"
            )
        )

        agent = Agent(
            role='Assistant',
            goal='Help users with their queries',
            backstory='I am a helpful AI assistant',
            tools=tools,
            llm=model
        )

        return agent
```

### Agent Chaining

You can call an agent from another agent to chain them.
This allows complex agentic logic, with multiple agents calling each other, orchestration, routing, etc.

```python
# Example of calling an agent, then putting its result inside a second one
from blaxel.agents import bl_agent

async def first_agent(input_text: str) -> dict:
    # First agent that processes loan applications
    response = await bl_agent("first-agent").run({
        "inputs": input_text
    })
    return response

async def second_agent(input_text: str) -> dict:
    # Second agent that evaluates the loan application
    first_response = await first_agent(input_text)

    model = await bl_model("gpt-4o-mini").to_langchain()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a loan specialist. Based on the given json file with client data, your job is to decide if a client can be further processed."),
        ("human", "{input}")
    ])

    response = await model.ainvoke(first_response)
    return response
```

### Deploy on blaxel

To deploy on blaxel, we have only one requirement in each agent code.
We need an HTTP Server.

For example with FastAPI:

```python
from fastapi import FastAPI
from blaxel import sdk
import uvicorn

app = FastAPI()

@app.post("/")
async def root(inputs: str):
    # Your agentic logic here
    return {"response": "Your response here"}

if __name__ == "__main__":
    port = int(os.getenv("BL_SERVER_PORT", "3000"))
    host = os.getenv("BL_SERVER_HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
```

```bash
bl deploy
```

### Advanced configuration

You can add optionally a configuration file "blaxel.toml" in your project root.

```toml
name = "my-agent"
workspace = "my-workspace"
type = "agent"

functions = ["blaxel-search"]
models = ["sandbox-openai"]
```

It allows to customize the requirements for your agent, it can be useful if you have many models and functions in your workspace.

### Create an MCP Server

If you want to create an MCP Server for using it in multiple agents, you can bootstrap it with the following command:

```bash
bl create-mcp-server my-mcp-server
cd my-mcp-server
bl serve --hotreload
```

We follow current standard for tool development over MCP Server.
Example of a tool which is sending fake information about the weather:

```python
from blaxel.mcp.server import FastMCP

mcp = FastMCP("My Weather MCP server")

@mcp.tool()
def weather(city: str) -> str:
    """Get the weather for a city"""
    return f"The weather in {city} is sunny"

if __name__ == "__main__":
    if os.getenv("BL_SERVER_PORT"):
      mcp.run(transport="ws")
    else:
      mcp.run(transport="stdio")


```

### Connect an existing MCP Server to blaxel

You need to have a "blaxel.toml" file in your project root:

```toml
name = "weather"
workspace = "my-workspace"
type = "function"
```

Connect the observability layer:

```python
from blaxel import sdk
```

Update your import of FastMCP

```python
from blaxel.mcp.server import FastMCP
```

Update your entrypoint to support our transport:

```python
def main():
    mcp.run(transport="ws") if os.getenv("BL_SERVER_PORT") else mcp.run(transport="stdio")
```

### How to use environment variables or secrets

You can use the "blaxel.toml" config file to specify environment variables for your agent:

```toml
name = "weather"
workspace = "my-workspace"
type = "function"

[env]
DEFAULT_CITY = "San Francisco"
```

Then you can use it in your agent or function with the following syntax:

```python
from blaxel.env import env
print(env.DEFAULT_CITY)  # San Francisco
```

You can also add secrets variables to a .env files in your project root. (goal is to not commit this file)

Example of a .env file:

```
# Secret variables can be stored here
DEFAULT_CITY_PASSWORD=123456
```

Then you can use it in your agent or function with the following syntax:

```python
from blaxel.env import env
print(env.DEFAULT_CITY_PASSWORD)  # 123456
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

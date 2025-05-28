# Blaxel Python SDK

<p align="center">
  <img src="https://blaxel.ai/logo-bg.png" alt="Blaxel"/>
</p>

**Blaxel is a computing platform for AI agent builders, with all the services and infrastructure to build and deploy agents efficiently.** This repository contains the Python SDK to create and manage resources on Blaxel.

## Table of Contents

- [Installation](#installation)
  - [Authentication](#authentication)
- [Features](#features)
- [Quickstart](#quickstart)
- [Contributing](#contributing)
- [License](#license)



## Installation

Install Blaxel SDK which lets you manage Blaxel resources.

```bash
## Using pip
pip install blaxel

## Using uv
uv pip install blaxel

## Using uv add
uv add blaxel
``` 



### Authentication

The Blaxel SDK authenticates with your workspace using credentials from these sources, in priority order:
1. When running on Blaxel, authentication is handled automatically
2. Variables in your .env file (`BL_WORKSPACE` and `BL_API_KEY`, or see [this page](https://docs.blaxel.ai/Agents/Variables-and-secrets) for other authentication options).
3. Environment variables from your machine
4. Configuration file created locally when you log in through Blaxel CLI (or deploy on Blaxel)

When developing locally, the recommended method is to just log in to your workspace with Blaxel CLI. This allows you to run Blaxel SDK functions that will automatically connect to your workspace without additional setup. When you deploy on Blaxel, this connection persists automatically.

When running Blaxel SDK from a remote server that is not Blaxel-hosted, we recommend using environment variables as described in the third option above.



## Features
- Agents & MCP servers
  - [Create MCP servers](https://docs.blaxel.ai/Functions/Create-MCP-server)
  - [Connect to MCP servers and model APIs hosted on Blaxel](https://docs.blaxel.ai/Agents/Develop-an-agent-ts)
  - [Call agents from another agent](https://docs.blaxel.ai/Agents/Develop-an-agent-ts#connect-to-another-agent-multi-agent-chaining)
  - [Deploy on Blaxel](https://docs.blaxel.ai/Agents/Deploy-an-agent)
- Sandboxes
  - [Create and update sandboxes and sandbox previews](https://docs.blaxel.ai/Sandboxes/Overview)
  - [Run filesystem operations and processes on a sandbox](https://docs.blaxel.ai/Sandboxes/Processes)
- [Use environment variables or secrets](https://docs.blaxel.ai/Agents/Variables-and-secrets)



## Quickstart

Blaxel CLI gives you a quick way to create new applications: agents, MCP servers, jobs, etc - and deploy them to Blaxel.

**Prerequisites**:
- **Node.js:** v18 or later.
- **Blaxel CLI:** Make sure you have Blaxel CLI installed. If not, [install it](https://docs.blaxel.ai/cli-reference/introduction):
  ```bash
  curl -fsSL \
  https://raw.githubusercontent.com/blaxel-ai/toolkit/main/install.sh \
  | BINDIR=/usr/local/bin sudo -E sh
  ```
- **Blaxel login:** Login to Blaxel:
  ```bash
    bl login YOUR-WORKSPACE
  ```

```bash
bl create-agent-app myfolder
cd myfolder
bl deploy
```

Also available:
-  `bl create-mcp-server`
-  `bl create-job`



## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.



## License

This project is licensed under the MIT License - see the LICENSE file for details.

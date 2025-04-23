# build-langchain-web-browsing-agent-with-mcp

- Created at: 2025-04-23
- Created by: `🐢 Arun Godwin Patel @ Code Creations`

## Table of contents

- [Setup](#setup)
  - [System](#system)
  - [Installation](#installation)
- [Walkthrough](#walkthrough)
  - [Code Structure](#code-structure)
  - [Tech stack](#tech-stack)
  - [Build from scratch](#build-from-scratch)
    - [1. Create a virtual environment](#1-create-a-virtual-environment)
    - [2. Activate the virtual environment](#2-activate-the-virtual-environment)
    - [3. Install the required packages](#3-install-the-required-packages)
    - [4. Setup the config files](#4-setup-the-config-files)
    - [5. Create the Python modules](#5-create-the-python-modules)
    - [6. Run the agents](#6-run-the-agents)
    

## Setup

### System

This code repository was tested on the following computers:

- Mac Sonoma

At the time of creation, this code was built using `Python 3.13.2`

### Installation

1. Install `virtualenv`

```bash
# 1. Open a CMD terminal
# 2. Install virtualenv globally
pip install virtualenv
```

2. Create a virtual environment

```bash
python -m venv venv
```

3. Activate the virtual environment

```bash
# Windows
.\venv\Scripts\activate
# Mac
source venv/bin/activate
```

4. Install the required packages

```bash
pip install -r requirements.txt
```

5. Run the modules

```bash
python airbnb.py
python browser.py
```

## Walkthrough

### Code Structure

The code directory structure is as follows:

```plaintext
build-langchain-web-browsing-agent-with-mcp
└───config
|   └──airbnb_mcp.json
|   └──browser_mcp.json
│   .env
│   .gitignore
│   airbnb.py
│   browser.py
│   package-lock.json
│   README.md
│   requirements.txt
```

The `airbnb.py` & `browser.py` files are the entry points of the web browsing agents. These are the modules you need to run from the command line.

The `config/` folder contains JSON files that stores the server configurations for the AirBnB and web browsing MCP server.

The `.env` file contains the environment variables used by the application.

The `.gitignore` file specifies the files and directories that should be ignored by Git.

The `requirements.txt` file lists the Python packages required by the application.

### Tech stack

**AI**

- LLM: `Anthopic Claude`
- Orchestration: `LangChain`

**Tool use for Agents**

- Model Context Protocal: `mcp-use`

**MCP servers**

- Web browsing: `Playwright` & `Google Chrome`
- Travel: `AirBnB`

### Build from scratch

This project was built using Python, LangChain and the Anthopic Claude LLM. A simple text prompt is provided to the AI Agent which makes use of it's available tools via MCP servers to gather external information to fulfil the query.

#### 1. Create a virtual environment

```bash
python -m venv venv
```

#### 2. Activate the virtual environment

```bash
# Windows
.\venv\Scripts\activate
# Mac
source venv/bin/activate
```

#### 3. Install the required packages

```bash
pip install -r requirements.txt
```

#### 4. Setup the config files

The `config/` folder contains JSON files that stores the server configurations for the AirBnB and web browsing MCP server.

First let's set up the AirBnB MCP server. Create a file called `airbnb_mcp.json` in the `config/` folder and add the following content:

```json
{
    "mcpServers": {
        "airbnb": {
            "command": "npx",
            "args": [
                "-y",
                "@openbnb/mcp-server-airbnb"
            ]
        }
    }
}
```

Next, create a file called `browser_mcp.json` in the `config/` folder and add the following content:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest"
      ],
      "env": {
        "DISPLAY": ":1"
      }
    }
  }
}
```

#### 5. Create the Python modules

Next, we create the Python modules that will be used to run the AirBnB and web browsing agents. Create a file called `airbnb.py` in the root directory and add the following content:

```python
import asyncio
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent, MCPClient

async def main():
    # Load environment variables
    load_dotenv()

    # Create MCPClient with Airbnb configuration
    client = MCPClient.from_config_file(
        os.path.join(os.path.dirname(__file__), "config/airbnb_mcp.json")
    )

    # Create LLM - you can choose between different models
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    try:
        # Run a query to search for accommodations
        result = await agent.run(
            "Find me a nice place to stay in Belfast for 2 adults "
            "for a week in August. I prefer places with a balcony and "
            "good reviews. Show me the top 3 options.",
            max_steps=30,
        )
        print(f"\nRESULT:\n\n{result[0]['text']}\n\n")
    finally:
        # Ensure we clean up resources properly
        if client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
```

Next, create a file called `browser.py` in the root directory and add the following content:

```python
import asyncio
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from mcp_use import MCPAgent, MCPClient

async def main():
    # Load environment variables
    load_dotenv()

    # Create MCPClient from config file
    client = MCPClient.from_config_file(
        os.path.join(os.path.dirname(__file__), "config/browser_mcp.json")
    )

    # Create LLM
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Create agent with the client
    agent = MCPAgent(
        llm=llm,
        client=client, 
        max_steps=30,
        verbose=True
    )

    # Run the query
    try:
        result = await agent.run(
            "Find the best restaurant in London USING GOOGLE SEARCH",
            max_steps=30,
        )
        print(f"\nRESULT:\n\n{result[0]['text']}\n\n")
    finally:
        # Ensure we clean up resources properly
        if client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
```

#### 6. Run the agents

To run the AirBnB agent, run the following command in the terminal:

```bash
python airbnb.py
```

To run the web browsing agent, run the following command in the terminal:

```bash
python browser.py
```

This completes the setup of our web browsing agents!

## Happy coding! 🚀

```bash
🐢 Arun Godwin Patel @ Code Creations
```

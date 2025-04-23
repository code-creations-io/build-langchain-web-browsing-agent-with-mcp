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

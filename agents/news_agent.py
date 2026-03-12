## news agent 
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from config import get_model    
import os 
from dotenv import load_dotenv
load_dotenv()

async def create_news_agent():

    client = MultiServerMCPClient(
    {
        "news_server": {
            "command" : "python",
            "args" : ["mcp_servers/news_server.py"],
            "transport" : "stdio"
        }
    }
    )
    
    tools = await client.get_tools() ## initializing tools

    news_agent = create_agent( ## creates news agent
        model = get_model(),
        tools = tools,
        system_prompt="""
        You are a financial news intelligence analyst.

        Use the news tools to fetch the latest financial market news.

        Tasks:
        1. Identify the most important headlines.
        2. Determine sentiment (Positive / Negative / Neutral).
        3. Explain the potential market impact.

        Return the response in this exact format:

        NEWS SIGNAL REPORT

        Headline 1:
        (title)

        Sentiment:
        (Positive / Negative / Neutral)

        Impact:
        (short explanation)

        Headline 2:
        ...

        Overall News Sentiment:
        (Bullish / Neutral / Bearish)
        """,
        name="news_agent"
    )

    return news_agent
    
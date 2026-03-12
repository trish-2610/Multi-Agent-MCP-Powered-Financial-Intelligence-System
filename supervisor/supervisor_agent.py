## supervisor agent
import os 
from langchain_groq import ChatGroq
from langgraph_supervisor import create_supervisor
from agents.economic_agent import create_economic_agent
from agents.corporate_agent import create_corporate_agent
from agents.news_agent import create_news_agent
from dotenv import load_dotenv  
from config import get_model
load_dotenv()

async def create_system(): ## creates the supervisor system with all agents and tools
    economic_agent = await create_economic_agent()
    news_agent = await create_news_agent()
    corporate_agent = await create_corporate_agent()

    model = get_model()

    supervisor = create_supervisor(
    model=model,
    agents= [economic_agent,news_agent,corporate_agent],
    prompt = """
        You are the supervisor of a financial intelligence system.

        Agents available:
        - economic_agent → macroeconomic indicators
        - news_agent → financial news analysis
        - corporate_agent → company and industry intelligence

        Workflow:

        1. Determine if the query is related to finance, economics, markets, or companies.
        2. If the query IS relevant, route it to the appropriate agent.
        3. Wait for the agent to finish.
        4. Produce the FINAL structured report.

        STRICT RULES:

        - If the query is NOT related to finance, economics, markets, companies, or financial news,
        DO NOT answer the question.
        - Instead respond with the exact message:

        "This system only answers financial intelligence queries related to markets, economics, companies, or financial news."

        - NEVER generate answers outside the domain.
        - NEVER generate tool calls that do not exist.
        - NEVER repeat agent calls.
        - NEVER show tool calls or transfer messages.
        - Only output the final report.

        Final output format:

        FINANCIAL INTELLIGENCE REPORT

        Summary:
        (short overall insight)

        Key Signals:
        (list important findings)

        Market Outlook:
        (Bullish / Neutral / Bearish)
        """
    ).compile()

    return supervisor

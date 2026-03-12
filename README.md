# Multi-Agent MCP Powered Financial Intelligence System

A production-oriented **Multi-Agent Financial Intelligence System** built using LangChain, LangGraph, FastMCP, and FastAPI. The system follows a **Supervisor-Agent architecture** over the **Model Context Protocol (MCP)**, where a central supervisor orchestrates three specialized AI agents — each connected to its own MCP server and backed by live external data sources.

![UI screenshot 1](ui/assets/ui_1.png)
![UI screenshot 2](ui/assets/ui_2.png)

Unlike simple chatbot demos that respond from static knowledge, this system fetches **real-time financial data** from the FRED API, Google News RSS, and Wikipedia, routes queries intelligently across agents, and produces structured financial intelligence reports.

The system is designed to simulate how industry-grade AI pipelines coordinate multiple specialized models over live data while enforcing **strict domain boundaries** to prevent irrelevant or hallucinated responses.

---

## System Flow Diagram

```
                        User Query
                            │
                            ▼
                        FastAPI  (/query)
                            │
                            ▼
                    Supervisor Agent  ──── out-of-domain query ────► Rejection Message
                            │
      ├─────────────────────┬─────────────────────┐
      ▼                     ▼                     ▼
  Economic Agent        News Agent          Corporate Agent
      │                     │                     │
      │  (MCP stdio)        │  (MCP stdio)        │  (MCP stdio)
      ▼                     ▼                     ▼
  Economic Server       News Server         Corporate Server
      │                     │                     │
      ▼                     ▼                     ▼
  FRED API           Google News RSS       Wikipedia API
      │                     │                     │
      └─────────────────────┴─────────────────────┘
                            │
                            ▼
                    Supervisor aggregates
                            │
                            ▼
                  FINANCIAL INTELLIGENCE REPORT
                            │
                            ▼
                      FastAPI Response
```

---

## Objective

The goal of this project is to build a reliable financial intelligence system capable of answering complex queries across macroeconomics, corporate analysis, and financial news.

The system focuses on:
- multi-agent coordination using the Model Context Protocol standard
- real-time data retrieval from live financial and economic APIs
- domain enforcement to prevent out-of-scope or hallucinated responses
- modular architecture that separates agent logic, server tools, and orchestration
- structured, traceable output reports grounded in fetched data

Instead of acting as a general-purpose assistant, the system behaves as a focused financial intelligence engine that only responds within its defined domain.

---

## Key Features

### Supervisor-Agent Orchestration

The system uses a LangGraph-based supervisor that receives a user query and dynamically routes it to the appropriate specialized agent.

The supervisor:
- determines query relevance to the financial domain
- delegates to one or more agents based on query type
- aggregates agent outputs into a unified final report
- rejects non-financial queries with a standard boundary message

---

### Model Context Protocol (MCP) Integration

Each agent connects to its own dedicated MCP server via `stdio` transport using `langchain-mcp-adapters`. The MCP servers expose tools that agents call at runtime to retrieve live data.

This follows the MCP standard, which acts as a universal interface between AI agents and external tools or data sources — enabling clean separation between reasoning logic and data access.

---

### Live Data Retrieval **(grounded, real-time responses)**

Every agent fetches current data at query time rather than relying on static training knowledge.

Data sources used:

- **FRED API** (St. Louis Federal Reserve) for macroeconomic indicators
- **Google News RSS** via `feedparser` for financial news headlines
- **Wikipedia REST API** for company summaries and competitor identification

**Example output**

Query:

What is the current inflation rate and how does it affect the market?

Report:

```
ECONOMIC SIGNAL REPORT

Inflation:
314.18 — CPI remains elevated, indicating persistent inflationary pressure.

Interest Rate:
5.33 — Federal Reserve maintaining restrictive monetary policy.

Unemployment:
3.7 — Labor market remains tight.

Market Impact:
Bearish — High inflation and sustained interest rates are likely to suppress equity valuations.
```

---

### Domain Enforcement **(prevents hallucination)**

The supervisor is explicitly instructed to reject queries outside finance, economics, markets, and corporate intelligence.

This ensures:
- the system does not generate off-topic responses
- agent tool calls are never triggered unnecessarily
- the output remains traceable to actual retrieved data

Queries such as *"What is the weather today?"* or *"Tell me a joke"* receive the following response:

```
This system only answers financial intelligence queries related to markets, economics, companies, or financial news.
```

---

### Structured Report Output

Each agent is prompted to return responses in a fixed, readable format. The supervisor aggregates these into a final report.

Report formats include:

- `NEWS SIGNAL REPORT` — headlines, sentiment per article, overall news sentiment
- `ECONOMIC SIGNAL REPORT` — indicator values, short explanations, market impact
- `CORPORATE INTELLIGENCE REPORT` — competitor list, industry trend, competitive impact, investment insight
- `FINANCIAL INTELLIGENCE REPORT` — supervisor-level summary, key signals, market outlook

---

### Modular Architecture

The system separates concerns across clearly defined layers.

Core modules include:

- MCP servers — tool definitions and external API calls
- Agents — LLM instances with role-specific system prompts connected to MCP servers
- Supervisor — LangGraph orchestrator that routes, aggregates, and enforces domain rules
- API layer — FastAPI server that exposes the system as a REST endpoint
- Config — centralized LLM initialization

This design allows independent extension of any layer without modifying the others.

---

### FastAPI REST Interface

The system is exposed as a single REST endpoint that accepts a natural language query and returns a structured financial report.

The API uses `astream` to consume supervisor output progressively, extracting the final message from the supervisor node for clean response delivery.

---

## Project Structure

The system follows an industry-style modular structure.

```
mcp_project/
│
├── agents/                          ## Specialized LangChain agents
│   ├── news_agent.py                ## Financial news analyst agent
│   ├── economic_agent.py            ## Macroeconomic indicators agent
│   └── corporate_agent.py           ## Competitor and industry intelligence agent
│
├── mcp_servers/                     ## FastMCP servers exposing tools to agents
│   ├── news_server.py               ## Tools: get_market_news, get_company_news
│   ├── economic_server.py           ## Tools: get_inflation, get_interest_rate, get_unemployment
│   └── corporate_server.py          ## Tools: get_competitors, industry_trend
│
├── supervisor/
│   └── supervisor_agent.py         ## LangGraph supervisor — orchestrates all agents
|
├── ui/                             ## Front-end static files
│   ├── index.html                  ## Main query interface
│   └── style.css                   ## Dark finance-themed stylesheet
    └── assets
|
├── main.py                          ## FastAPI entry point — /query POST endpoint
├── config.py                        ## LLM initialization (Groq / llama-3.1-8b-instant)
├── requirements.txt                 ## Python dependencies
```

---

## Agent and MCP Server Reference

### News Agent + News Server

**Agent role:** Financial news intelligence analyst

**MCP Tools:**
- `get_market_news()` — Fetches the top 5 headlines from Google News RSS for "stock market"
- `get_company_news(company)` — Fetches the top 5 headlines for a specific company

**Data source:** Google News RSS feed via `feedparser`

**Output:** `NEWS SIGNAL REPORT` with per-headline sentiment and overall market sentiment

---

### Economic Agent + Economic Server

**Agent role:** Macroeconomic intelligence analyst

**MCP Tools:**
- `get_inflation()` — Latest CPI value from FRED series `CPIAUCSL`
- `get_interest_rate()` — Latest Federal Funds Rate from FRED series `FEDFUNDS`
- `get_unemployment()` — Latest Unemployment Rate from FRED series `UNRATE`

**Data source:** FRED API (St. Louis Federal Reserve)

**Output:** `ECONOMIC SIGNAL REPORT` with indicator values and macroeconomic market sentiment

---

### Corporate Agent + Corporate Server

**Agent role:** Corporate intelligence analyst

**MCP Tools:**
- `get_competitors(company)` — Fetches company summary from the Wikipedia REST API
- `industry_trend(industry)` — Returns trend summary for semiconductor, electric vehicle, cloud computing, and banking sectors

**Data source:** Wikipedia REST API and internal trend knowledge base

**Output:** `CORPORATE INTELLIGENCE REPORT` with competitor analysis, industry trends, competitive impact, and investment insight

---

### Supervisor Agent

**Framework:** `langgraph_supervisor`

**Model:** `llama-3.1-8b-instant` via Groq (temperature = 0)

**Responsibilities:**
- determines whether a query falls within the financial domain
- routes to one or more of the three specialized agents
- enforces that no tool calls, agent transfers, or intermediate messages appear in the final output
- produces a unified `FINANCIAL INTELLIGENCE REPORT`

---

## Tech Stack

LLM Model: **llama-3.1-8b-instant** (Groq)

**Backend / Frameworks / Libraries**
- FastAPI (REST API server)
- LangChain (agent creation)
- LangGraph + `langgraph_supervisor` (multi-agent orchestration)
- FastMCP (MCP server implementation)
- `langchain-mcp-adapters` (MCP client for tool discovery)
- Uvicorn (ASGI server)

**External Data Sources**
- FRED API — Federal Reserve Economic Data
- Google News RSS — financial headline feed
- Wikipedia REST API — company and industry data

**Other Tools**
- Pydantic for request/response schemas
- `python-dotenv` for environment variable management
- `uv` for fast Python dependency management

---

## Challenges Faced

### Coordinating Multiple Agents Without Conflicts

In a multi-agent system, the supervisor must cleanly delegate tasks without triggering redundant agent calls or exposing intermediate tool output to the user.

**Solution**

Used `langgraph_supervisor` with explicit prompt rules that prevent repeated agent calls, suppress tool call visibility, and enforce a single structured final output.

---

### Connecting Agents to Live Tools via MCP

Each agent needs to dynamically discover and call tools exposed by its MCP server at runtime rather than having tools hardcoded into the agent definition.

**Solution**

Used `MultiServerMCPClient` with `stdio` transport to launch each MCP server as a subprocess and call `get_tools()` to dynamically bind tools to the agent at initialization time.

---

### Preventing Out-of-Domain Responses

LLMs will attempt to answer any question, including those outside the intended domain, leading to unreliable outputs in a specialized system.

**Solution**

Enforced domain boundaries at the supervisor level through explicit prompt instructions. The supervisor is instructed to respond with a fixed rejection message for any query that does not relate to finance, economics, markets, or corporate intelligence.

---

### Streaming Supervisor Output Cleanly

LangGraph's `astream` yields chunks from multiple nodes including intermediate agent messages, which need to be filtered to extract only the supervisor's final response.

**Solution**

Filtered the stream to capture only chunks from the `supervisor` node and extracted the last non-empty `content` field from the messages list as the final report.

---

## Optimizations Implemented

- Temperature set to 0 for deterministic, consistent financial analysis
- Domain enforcement at supervisor prompt level to eliminate irrelevant responses
- MCP servers launched as subprocesses via stdio, keeping server logic isolated from agent logic
- Structured output prompts for each agent ensuring consistent, parseable report formats
- Async initialization of all agents at FastAPI startup to avoid cold-start latency on first request

---

## API Reference

### POST /query

**Request body:**
```json
{
  "query": "Analyze the current macroeconomic environment"
}
```

**Response:**
```json
{
  "query": "Analyze the current macroeconomic environment",
  "report": "FINANCIAL INTELLIGENCE REPORT\n\nSummary:\n...\n\nKey Signals:\n...\n\nMarket Outlook:\nBullish / Neutral / Bearish"
}
```

---

## Running the Project

### Install dependencies

```
pip install -r requirements.txt
```

Or using `uv`:

```
uv sync
```

### Set environment variables

```
GROQ_API_KEY=your_groq_api_key
FRED_API_KEY=your_fred_api_key
```

### Run the server

```
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`

Interactive documentation at `http://localhost:8000/docs`

---

## Example Queries

| Query | Agent Routed To |
|---|---|
| What is the current US inflation rate? | Economic Agent |
| Analyze Apple's competitors and industry position | Corporate Agent |
| What is the latest stock market news? | News Agent |
| Give me a full financial report on Tesla | All Three Agents |
| What is the weather today? | Rejected — out of domain |

---

## Future Improvements

Possible extensions for this project include:
- Database integration for storing and querying historical financial reports
- Interactive dashboard for visualizing economic indicators and news sentiment
- User authentication and API key management for production deployment

---

## Conclusion

This project demonstrates how to build a **structured, modular, and domain-enforced multi-agent financial intelligence system** using the Model Context Protocol.

The focus is not only on making agents work, but on designing the system in a way that reflects production-ready AI engineering practices — including clean agent-server separation via MCP, live data grounding, supervisor-level domain enforcement, and a scalable modular architecture that can be extended without restructuring the existing pipeline.

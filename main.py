import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from supervisor.supervisor_agent import create_system

app = FastAPI(title="MCP_BAsed Multi-Agent Financel Intelligence System", version="1.0")

supervisor = None

## output schema 
class QueryRequest(BaseModel):
    query: str

@app.on_event("startup")
async def startup_event():
    global supervisor
    supervisor = await create_system()

@app.post("/query")
async def ask_query(request: QueryRequest):

    final_message = ""

    try:
        async for chunk in supervisor.astream(
            {"messages": [{"role": "user", "content": request.query}]}
        ):

            if "supervisor" in chunk:

                data = chunk["supervisor"]

                if data and "messages" in data:
                    for m in data["messages"]:

                        if hasattr(m, "content") and m.content:
                            final_message = m.content

    except Exception as e:

        final_message = f"""
        System Error Encountered

        Reason:
        {str(e)}

        Temporary issue occurred while processing the request.

        Possible causes:
        • API rate limit
        • tool execution failure
        • external data provider error

        Please try again.
        """

    return {
        "query": request.query,
        "report": final_message
    }
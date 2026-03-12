## corporate server
from mcp.server.fastmcp import FastMCP
import requests 

mcp = FastMCP("corporate_server")

@mcp.tool()
def get_competitors(company: str):
    """Find competitors of a company using Wikipedia"""

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company}"

    try:
        data = requests.get(url).json()
        summary = data.get("extract", "")
        return {
            "company": company,
            "summary": summary
        }

    except:
        return {
            "company": company,
            "summary": "No data found"
        }


@mcp.tool()
def industry_trend(industry: str):
    """Provide general industry trend summary"""

    trends = {
        "semiconductor" : "AI demand driving chip production growth",
        "electric vehicle" : "Rapid EV adoption globally with Chinese manufacturers expanding",
        "cloud computing" : "Enterprise cloud adoption increasing rapidly",
        "banking" : "Digital banking and fintech competition rising"
    }
    return trends.get(industry.lower(), "Industry trend data not available")


if __name__ == "__main__":
    print("Corporate MCP server started...")
    mcp.run()
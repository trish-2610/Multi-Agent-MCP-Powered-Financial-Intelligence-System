## economic server
import os 
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
load_dotenv()

## loading FRED API key from environment variable
FRED_API_KEY = os.getenv("FRED_API_KEY")

mcp = FastMCP("economic_data_server")

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_fred(series_id):
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1
    }

    r = requests.get(BASE_URL, params=params)
    data = r.json()

    if "observations" in data:
        return data["observations"][0]["value"]
    return "No data"

@mcp.tool()
def get_inflation():
    """Get latest Inflation (CPI)"""
    return fetch_fred("CPIAUCSL")

@mcp.tool()
def get_interest_rate():
    """Get latest US interest rate"""
    return fetch_fred("FEDFUNDS")


@mcp.tool()
def get_unemployment():
    """Get latest unemployment rate"""
    return fetch_fred("UNRATE")


if __name__ == "__main__":
    print("Economic MCP server started...")
    mcp.run()
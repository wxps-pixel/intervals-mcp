import os
import httpx
import uvicorn
from datetime import date
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

ATHLETE_ID = os.getenv("ICU_ATHLETE_ID")
API_KEY    = os.getenv("ICU_API_KEY")
BASE_URL   = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}"
AUTH       = ("API_KEY", API_KEY)

mcp = FastMCP("Intervals ICU")

@mcp.tool()
def get_activities(oldest: str = "2024-01-01", newest: str = None) -> str:
    """Récupère les activités sportives de l'athlète"""
    if newest is None:
        newest = date.today().isoformat()
    r = httpx.get(f"{BASE_URL}/activities", auth=AUTH, params={"oldest": oldest, "newest": newest})
    r.raise_for_status()
    return r.text

@mcp.tool()
def get_wellness(oldest: str = "2024-01-01", newest: str = None) -> str:
    """Récupère HRV, fréquence cardiaque au repos, poids..."""
    if newest is None:
        newest = date.today().isoformat()
    r = httpx.get(f"{BASE_URL}/wellness", auth=AUTH, params={"oldest": oldest, "newest": newest})
    r.raise_for_status()
    return r.text

@mcp.tool()
def get_athlete_summary() -> str:
    """Résumé du profil athlète : FTP, zones, infos générales"""
    r = httpx.get(BASE_URL, auth=AUTH)
    r.raise_for_status()
    return r.text

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app = mcp.get_asgi_app()
    uvicorn.run(app, host="0.0.0.0", port=port)

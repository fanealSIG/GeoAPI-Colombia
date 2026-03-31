"""Geocoding con Nominatim (OpenStreetMap) — 100% gratuito."""
import httpx
import logging
from typing import Any

logger = logging.getLogger(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "Geoforest/1.0 (geoforest@example.com)"}


async def geocode_place(place_name: str, country: str = "Colombia") -> dict[str, Any] | None:
    """
    Retorna {lat, lon, display_name, boundingbox, geojson} o None.
    """
    params = {
        "q": f"{place_name}, {country}",
        "format": "json",
        "limit": 1,
        "polygon_geojson": 1,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(NOMINATIM_URL, params=params, headers=HEADERS)
            resp.raise_for_status()
            results = resp.json()
            if not results:
                return None
            r = results[0]
            return {
                "lat": float(r["lat"]),
                "lon": float(r["lon"]),
                "display_name": r["display_name"],
                "boundingbox": r.get("boundingbox"),
                "geojson": r.get("geojson"),
            }
        except Exception as e:
            logger.error(f"Geocoding error para '{place_name}': {e}")
            return None

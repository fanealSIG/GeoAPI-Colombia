from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.cache import cache_get, cache_set
from app.schemas.geo import ForestAnalysisRequest, ForestAnalysisResponse, GeoQueryRequest
from app.services import gee_service, geocoding, claude_agent
import json

router = APIRouter(prefix="/forest", tags=["Forest Analysis"])


@router.post("/analyze")
async def analyze_forest(
    request: ForestAnalysisRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Analiza cobertura forestal para un municipio/departamento colombiano.
    Usa GEE + datos Hansen Global Forest Change.
    """
    if request.year_end < request.year_start:
        raise HTTPException(status_code=400, detail="year_end debe ser >= year_start")

    cache_key = f"forest:{request.region_code}:{request.year_start}:{request.year_end}"
    cached = await cache_get(cache_key)
    if cached:
        return json.loads(cached)

    # Geocodificar la región
    geo = await geocoding.geocode_place(request.region_code)
    if not geo:
        raise HTTPException(status_code=404, detail=f"Región '{request.region_code}' no encontrada")

    # Analizar con GEE
    result = gee_service.get_forest_cover(
        geo.get("geojson", {}),
        request.year_start,
        request.year_end,
    )

    response = {
        "region": request.region_code,
        "location": geo,
        "analysis": result,
    }

    await cache_set(cache_key, json.dumps(response), ttl=86400)  # 24h
    return response


@router.post("/query")
async def natural_language_query(request: GeoQueryRequest):
    """
    Consulta en lenguaje natural al agente Claude.
    Ej: "Analizar deforestación en Envigado 2021-2024"
    """
    result = await claude_agent.run_geo_query(request.query, request.context)
    return result


@router.get("/ndvi/{place_name}")
async def get_ndvi(
    place_name: str,
    year_start: int = 2020,
    year_end: int = 2024,
):
    """Series temporales NDVI para un lugar."""
    geo = await geocoding.geocode_place(place_name)
    if not geo:
        raise HTTPException(status_code=404, detail=f"'{place_name}' no encontrado")

    ndvi_data = gee_service.get_ndvi_series(
        geo.get("geojson", {}),
        year_start,
        year_end,
    )
    return {"place": place_name, "location": geo, "ndvi_series": ndvi_data}

from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime


class RegionBase(BaseModel):
    name: str
    code: str
    region_type: str
    department: str | None = None


class RegionResponse(RegionBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ForestAnalysisRequest(BaseModel):
    region_code: str = Field(..., description="Código DANE del municipio/departamento")
    year_start: int = Field(..., ge=2000, le=2024)
    year_end: int = Field(..., ge=2000, le=2024)
    include_ndvi: bool = True


class ForestAnalysisResponse(BaseModel):
    id: int
    region: RegionResponse
    year_start: int
    year_end: int
    forest_cover_ha: float | None
    deforestation_ha: float | None
    reforestation_ha: float | None
    deforestation_pct: float | None
    ndvi_mean: float | None
    data_source: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertResponse(BaseModel):
    id: int
    region_id: int
    detected_at: datetime
    area_ha: float
    severity: str
    confidence: float | None
    is_verified: bool
    geometry: dict[str, Any] | None = None

    model_config = {"from_attributes": True}


class GeoQueryRequest(BaseModel):
    """Consulta en lenguaje natural al agente Claude."""
    query: str = Field(..., min_length=5, max_length=500, description="Ej: 'Analizar deforestación en Envigado 2021-2024'")
    context: dict[str, Any] = Field(default_factory=dict)

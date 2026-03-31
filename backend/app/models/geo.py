from datetime import datetime
from sqlalchemy import String, DateTime, Float, Integer, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from app.core.database import Base


class Region(Base):
    """Municipios y departamentos de Colombia."""
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)  # DANE code
    region_type: Mapped[str] = mapped_column(String(20), nullable=False)  # municipio | departamento
    department: Mapped[str | None] = mapped_column(String(100))
    geometry: Mapped[object] = mapped_column(Geometry("MULTIPOLYGON", srid=4326))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    analyses: Mapped[list["ForestAnalysis"]] = relationship(back_populates="region")


class ForestAnalysis(Base):
    """Resultados de análisis de cobertura forestal."""
    __tablename__ = "forest_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=False, index=True)
    year_start: Mapped[int] = mapped_column(Integer, nullable=False)
    year_end: Mapped[int] = mapped_column(Integer, nullable=False)
    forest_cover_ha: Mapped[float | None] = mapped_column(Float)
    deforestation_ha: Mapped[float | None] = mapped_column(Float)
    reforestation_ha: Mapped[float | None] = mapped_column(Float)
    deforestation_pct: Mapped[float | None] = mapped_column(Float)
    ndvi_mean: Mapped[float | None] = mapped_column(Float)
    data_source: Mapped[str] = mapped_column(String(50), default="GEE")
    raw_result: Mapped[str | None] = mapped_column(Text)  # JSON del agente Claude
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    region: Mapped["Region"] = relationship(back_populates="analyses")


class AlertEvent(Base):
    """Alertas de deforestación detectadas."""
    __tablename__ = "alert_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=False, index=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    area_ha: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)  # low | medium | high | critical
    geometry: Mapped[object] = mapped_column(Geometry("POLYGON", srid=4326))
    confidence: Mapped[float | None] = mapped_column(Float)
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

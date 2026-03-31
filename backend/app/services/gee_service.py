"""
Google Earth Engine service.
Requiere activar Earth Engine en tu cuenta Google Cloud:
https://earthengine.google.com/signup/
"""
import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

_gee_initialized = False


def init_gee(service_account: str, key_file: str) -> bool:
    """Inicializa GEE con service account. Retorna False si falla."""
    global _gee_initialized
    try:
        import ee
        credentials = ee.ServiceAccountCredentials(service_account, key_file)
        ee.Initialize(credentials)
        _gee_initialized = True
        logger.info("Google Earth Engine inicializado correctamente")
        return True
    except Exception as e:
        logger.warning(f"GEE no disponible: {e}. Usando datos mock.")
        return False


def get_forest_cover(
    geometry_geojson: dict,
    year_start: int,
    year_end: int,
) -> dict[str, Any]:
    """
    Calcula cobertura forestal usando Hansen Global Forest Change.
    Dataset: UMD/hansen/global_forest_change_2023_v1_11
    """
    if not _gee_initialized:
        return _mock_forest_data(year_start, year_end)

    try:
        import ee
        aoi = ee.Geometry(geometry_geojson)

        # Hansen Global Forest Change
        gfc = ee.Image("UMD/hansen/global_forest_change_2023_v1_11")

        tree_cover_2000 = gfc.select("treecover2000")
        loss = gfc.select("loss")
        loss_year = gfc.select("lossyear")
        gain = gfc.select("gain")

        # Cobertura forestal base (canopy > 30%)
        forest_mask = tree_cover_2000.gt(30)

        # Pérdida en el rango de años
        start_offset = year_start - 2000
        end_offset = year_end - 2000
        loss_in_period = loss.And(loss_year.gt(start_offset).And(loss_year.lte(end_offset)))

        pixel_area = ee.Image.pixelArea().divide(10000)  # hectáreas

        forest_area = forest_mask.multiply(pixel_area).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=30,
            maxPixels=1e10
        ).getInfo()

        deforestation_area = loss_in_period.multiply(pixel_area).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=30,
            maxPixels=1e10
        ).getInfo()

        gain_area = gain.multiply(pixel_area).reduceRegion(
            reducer=ee.Reducer.sum(),
            geometry=aoi,
            scale=30,
            maxPixels=1e10
        ).getInfo()

        forest_ha = float(forest_area.get("treecover2000", 0))
        defor_ha = float(deforestation_area.get("loss", 0))
        regain_ha = float(gain_area.get("gain", 0))

        return {
            "forest_cover_ha": round(forest_ha, 2),
            "deforestation_ha": round(defor_ha, 2),
            "reforestation_ha": round(regain_ha, 2),
            "deforestation_pct": round((defor_ha / forest_ha * 100) if forest_ha > 0 else 0, 2),
            "data_source": "GEE/Hansen",
            "year_start": year_start,
            "year_end": year_end,
        }

    except Exception as e:
        logger.error(f"Error GEE: {e}")
        return _mock_forest_data(year_start, year_end)


def get_ndvi_series(geometry_geojson: dict, year_start: int, year_end: int) -> list[dict]:
    """Series temporales NDVI con Sentinel-2 / Landsat."""
    if not _gee_initialized:
        return _mock_ndvi_series(year_start, year_end)

    try:
        import ee
        aoi = ee.Geometry(geometry_geojson)

        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(aoi)
            .filterDate(f"{year_start}-01-01", f"{year_end}-12-31")
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
            .map(lambda img: img.normalizedDifference(["B8", "B4"]).rename("NDVI"))
        )

        monthly = collection.toBands()
        stats = monthly.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=aoi,
            scale=10,
            maxPixels=1e9
        ).getInfo()

        return [{"band": k, "ndvi": round(v, 4)} for k, v in stats.items() if v is not None]

    except Exception as e:
        logger.error(f"Error NDVI: {e}")
        return _mock_ndvi_series(year_start, year_end)


def _mock_forest_data(year_start: int, year_end: int) -> dict[str, Any]:
    """Datos de demostración cuando GEE no está disponible."""
    years = year_end - year_start
    base_ha = 12500.0
    defor = round(base_ha * 0.03 * years, 2)
    return {
        "forest_cover_ha": base_ha,
        "deforestation_ha": defor,
        "reforestation_ha": round(defor * 0.15, 2),
        "deforestation_pct": round(defor / base_ha * 100, 2),
        "data_source": "MOCK",
        "year_start": year_start,
        "year_end": year_end,
    }


def _mock_ndvi_series(year_start: int, year_end: int) -> list[dict]:
    import random
    results = []
    for year in range(year_start, year_end + 1):
        for month in range(1, 13):
            results.append({
                "year": year,
                "month": month,
                "ndvi": round(0.55 + random.uniform(-0.15, 0.15), 4),
            })
    return results

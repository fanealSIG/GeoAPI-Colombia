"""
Agente Claude con function calling para consultas en lenguaje natural.
El usuario escribe: "Analizar deforestación en Envigado 2021-2024"
→ Claude decide qué herramientas usar y orquesta la respuesta.
"""
import json
import logging
from typing import Any
import anthropic
from app.services import gee_service, geocoding

logger = logging.getLogger(__name__)

client = anthropic.AsyncAnthropic()

TOOLS = [
    {
        "name": "geocode_region",
        "description": "Obtiene coordenadas y geometría de un municipio o departamento de Colombia.",
        "input_schema": {
            "type": "object",
            "properties": {
                "place_name": {
                    "type": "string",
                    "description": "Nombre del municipio o departamento. Ej: 'Envigado', 'Antioquia'"
                }
            },
            "required": ["place_name"]
        }
    },
    {
        "name": "analyze_forest_cover",
        "description": "Analiza cobertura forestal y deforestación en una región usando Google Earth Engine.",
        "input_schema": {
            "type": "object",
            "properties": {
                "place_name": {"type": "string", "description": "Nombre del lugar"},
                "year_start": {"type": "integer", "description": "Año inicial (2000-2024)"},
                "year_end": {"type": "integer", "description": "Año final (2000-2024)"},
                "include_ndvi": {"type": "boolean", "default": True}
            },
            "required": ["place_name", "year_start", "year_end"]
        }
    },
    {
        "name": "get_deforestation_alerts",
        "description": "Obtiene alertas recientes de deforestación en una región.",
        "input_schema": {
            "type": "object",
            "properties": {
                "place_name": {"type": "string"},
                "days_back": {"type": "integer", "description": "Días hacia atrás para buscar alertas", "default": 30}
            },
            "required": ["place_name"]
        }
    }
]

SYSTEM_PROMPT = """Eres GeoForest AI, un asistente especializado en análisis forestal y ambiental de Colombia.
Tienes acceso a herramientas de análisis satelital, datos de cobertura forestal y alertas de deforestación.
Responde siempre en español. Sé conciso y preciso con los datos.
Cuando presentes números, incluye unidades (hectáreas, %, km²).
Si detectas deforestación significativa (>5%), marca como alerta.
"""


async def run_geo_query(query: str, context: dict[str, Any] = {}) -> dict[str, Any]:
    """
    Ejecuta una consulta en lenguaje natural usando Claude + herramientas geo.
    Retorna el resultado final estructurado.
    """
    messages = [{"role": "user", "content": query}]

    # Agentic loop
    for _ in range(5):  # max 5 turnos
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            # Respuesta final
            text = next(
                (b.text for b in response.content if hasattr(b, "text")),
                "Análisis completado."
            )
            return {"answer": text, "tool_calls": _extract_tool_names(messages)}

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = await _execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    })
            messages.append({"role": "user", "content": tool_results})

    return {"answer": "No pude completar el análisis. Intenta reformular tu consulta.", "tool_calls": []}


async def _execute_tool(name: str, inputs: dict) -> dict:
    """Ejecuta la herramienta solicitada por Claude."""
    try:
        if name == "geocode_region":
            result = await geocoding.geocode_place(inputs["place_name"])
            return result or {"error": f"No se encontró '{inputs['place_name']}'"}

        elif name == "analyze_forest_cover":
            geo = await geocoding.geocode_place(inputs["place_name"])
            if not geo or not geo.get("geojson"):
                return {"error": f"No se encontró geometría para '{inputs['place_name']}'"}
            forest_data = gee_service.get_forest_cover(
                geo["geojson"],
                inputs["year_start"],
                inputs["year_end"],
            )
            return {**forest_data, "region": inputs["place_name"], "location": geo}

        elif name == "get_deforestation_alerts":
            # Placeholder — integrar con GFW Alerts API en semana 5
            return {
                "region": inputs["place_name"],
                "alerts": [],
                "note": "Integración con Global Forest Watch pendiente (semana 5)"
            }

        return {"error": f"Herramienta '{name}' no implementada"}

    except Exception as e:
        logger.error(f"Error ejecutando tool {name}: {e}")
        return {"error": str(e)}


def _extract_tool_names(messages: list) -> list[str]:
    names = []
    for msg in messages:
        if isinstance(msg.get("content"), list):
            for block in msg["content"]:
                if hasattr(block, "type") and block.type == "tool_use":
                    names.append(block.name)
    return names

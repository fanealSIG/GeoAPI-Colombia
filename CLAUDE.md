# Geoforest — Contexto del Proyecto

## Qué es
SaaS geoportal de análisis forestal y ambiental para Colombia.
UI inspirada en Copernicus y ZoomEarth: full-screen map, dark theme, panel lateral, timeline, capas.
Plan de desarrollo: 10 semanas, costo operativo $0 (free tiers).

## Stack
| Capa | Tecnología | Hosting |
|---|---|---|
| Frontend | React + Vite + MapLibre GL | Vercel (free) |
| Backend | FastAPI (Python) | Railway (free, $5 crédito) |
| Base de datos | PostgreSQL + PostGIS | Supabase (free) |
| Cache | Redis | Railway (free) |
| AI | Claude claude-sonnet-4-6 con function calling | API Anthropic |
| Geo data | Google Earth Engine | Free (research) |
| Geocoding | Nominatim (OpenStreetMap) | Free |
| Auth | JWT propio (futuro: Supabase Auth) | — |

## Repositorio
- GitHub: https://github.com/fanealSIG/GeoAPI-Colombia
- Branch principal: `master`
- Estructura: monorepo (`backend/` + `frontend/`)

## Credenciales y servicios activos
- Google Cloud proyecto: `geoforest-gee`
- Service account: `geoforest-gee@geoforest-gee.iam.gserviceaccount.com`
- Key file local: `backend/gee-key.json` (nunca subir a GitHub)
- Railway: cuenta activa (pendiente conectar repo)
- Supabase: cuenta pendiente de crear
- Vercel: cuenta pendiente de crear

## Archivos clave
```
backend/
├── app/main.py                        ← FastAPI entry point
├── app/core/config.py                 ← Settings (.env)
├── app/core/database.py               ← PostgreSQL async + PostGIS
├── app/core/cache.py                  ← Redis async
├── app/models/geo.py                  ← Region, ForestAnalysis, AlertEvent
├── app/models/user.py                 ← User (free/pro/enterprise)
├── app/services/gee_service.py        ← Google Earth Engine + mock
├── app/services/geocoding.py          ← Nominatim
├── app/services/claude_agent.py       ← Agente Claude (function calling)
├── app/api/v1/endpoints/forest.py     ← /analyze /query /ndvi
├── app/api/v1/endpoints/auth.py       ← register/login/me
├── .env                               ← LOCAL ONLY, nunca a GitHub
├── gee-key.json                       ← LOCAL ONLY, nunca a GitHub
└── railway.toml                       ← Config deploy Railway
```

## Variables de entorno (.env)
```
DATABASE_URL=postgresql+asyncpg://...   ← viene de Supabase
REDIS_URL=redis://...                   ← viene de Railway
GEE_SERVICE_ACCOUNT=geoforest-gee@geoforest-gee.iam.gserviceaccount.com
GEE_KEY_FILE=gee-key.json
SECRET_KEY=geoforest-secret-xK9mP2-2024-fanealSIG
APP_ENV=development
CORS_ORIGINS=http://localhost:5173,https://geoforest.vercel.app
```

## Endpoints disponibles
```
GET  /api/v1/health              ← healthcheck
POST /api/v1/auth/register       ← crear usuario
POST /api/v1/auth/token          ← login → JWT
GET  /api/v1/auth/me             ← usuario actual
POST /api/v1/forest/analyze      ← análisis forestal por región
POST /api/v1/forest/query        ← consulta lenguaje natural (Claude Agent)
GET  /api/v1/forest/ndvi/{place} ← series NDVI
```

## Plan de 10 semanas
| Semana | Tarea | Estado |
|---|---|---|
| 1-2 | Frontend UI (MapLibre, dark theme) | Pendiente |
| 3-4 | Backend + DB | ✅ Código listo, deploy pendiente |
| 5 | GEE Integration | Parcial (mock activo) |
| 6 | Change Detection | Pendiente |
| 7 | Claude Agent | ✅ Código listo |
| 8 | Auth + Stripe | Auth listo, Stripe pendiente |
| 9 | Landing page | Pendiente |
| 10 | Launch | Pendiente |

## Próximos pasos
1. Crear cuenta Supabase → obtener DATABASE_URL → actualizar .env
2. Crear cuenta Railway → conectar GitHub → deploy FastAPI
3. Crear cuenta Vercel → frontend
4. Registrar service account GEE en code.earthengine.google.com
5. Arrancar frontend (React + Vite + MapLibre)

## Decisiones de arquitectura
- **Supabase para DB** (mejor free tier de PostgreSQL/PostGIS que Railway)
- **Railway solo para FastAPI + Redis** (ahorra crédito sin hostear DB)
- **Datos mock activos** cuando GEE no está disponible (nunca rompe)
- **Claude claude-sonnet-4-6** para el agente de análisis en lenguaje natural
- **Nominatim** para geocoding (gratis, sin API key)

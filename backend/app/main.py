import logging
import sentry_sdk
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.database import init_db
from app.core.cache import close_redis
from app.api.v1.router import router
from app.services.gee_service import init_gee

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sentry (free tier — solo si hay DSN configurado)
if settings.SENTRY_DSN:
    sentry_sdk.init(dsn=settings.SENTRY_DSN, traces_sample_rate=0.1)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Iniciando Geoforest API...")
    await init_db()
    logger.info("Base de datos inicializada")

    if settings.GEE_SERVICE_ACCOUNT:
        ok = init_gee(settings.GEE_SERVICE_ACCOUNT, settings.GEE_KEY_FILE)
        if not ok:
            logger.warning("GEE no disponible — usando datos mock")

    yield

    # Shutdown
    await close_redis()
    logger.info("Geoforest API detenida")


app = FastAPI(
    title="Geoforest API",
    description="API de análisis forestal y ambiental para Colombia",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Rutas
app.include_router(router)

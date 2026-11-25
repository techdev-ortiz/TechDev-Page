"""Aplicación FastAPI: landing pública, SEO y panel /admin."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import BASE_DIR, settings
from .db import init_db
from .routers import admin, public, seo

logger = logging.getLogger("techdev")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings.ensure_dirs()
    init_db()
    if not settings.admin_ready:
        logger.warning(
            "TECHDEV_PASSWORD no está definida: el panel /admin permanecerá bloqueado."
        )
    elif settings.default_password_in_use:
        logger.warning(
            "TECHDEV_PASSWORD usa el valor de ejemplo. Cámbiala antes de publicar el sitio."
        )
    logger.info("TechDev listo · base de datos: %s", settings.db_path)
    yield


app = FastAPI(
    title="TechDev",
    description="Landing page de servicios de programación con panel de administración.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(public.router)
app.include_router(admin.router)
app.include_router(seo.router)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault(
        "Permissions-Policy", "camera=(), microphone=(), geolocation=()"
    )
    return response


@app.exception_handler(404)
async def not_found(request: Request, exc):  # noqa: ANN001
    if request.url.path.startswith(("/api/", "/admin/api/")):
        return JSONResponse({"detail": "No encontrado"}, status_code=404)
    return JSONResponse(
        {
            "detail": "No encontrado",
            "home": str(request.base_url),
        },
        status_code=404,
    )

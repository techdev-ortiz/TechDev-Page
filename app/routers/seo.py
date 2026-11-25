"""SEO, archivos estáticos subidos y healthcheck."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, Response

from ..config import settings
from ..store import db_is_healthy

router = APIRouter()

ALLOWED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


@router.get("/robots.txt", response_class=PlainTextResponse)
def robots() -> PlainTextResponse:
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin\n"
        "Disallow: /admin/login\n"
        "Disallow: /api/\n"
        "\n"
        f"Sitemap: {settings.base_url}/sitemap.xml\n"
    )
    return PlainTextResponse(body)


@router.get("/sitemap.xml")
def sitemap() -> Response:
    today = date.today().isoformat()
    urls = [
        (f"{settings.base_url}/", "1.0"),
        (f"{settings.base_url}/?lang=es", "0.9"),
        (f"{settings.base_url}/?lang=en", "0.8"),
    ]
    entries = "".join(
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>weekly</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
        for loc, priority in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}"
        "</urlset>\n"
    )
    return Response(content=xml, media_type="application/xml")


@router.get("/media/{filename}")
def media(filename: str) -> FileResponse:
    safe_name = Path(filename).name
    target = Path(settings.upload_dir) / safe_name
    if target.suffix.lower() not in ALLOWED_SUFFIXES or not target.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(
        target,
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )


@router.get("/health")
def health(request: Request) -> JSONResponse:
    healthy = db_is_healthy()
    return JSONResponse(
        {"status": "ok" if healthy else "degraded", "database": healthy},
        status_code=200 if healthy else 503,
    )

"""Rutas públicas: landing SSR, APIs de contenido y de analítica."""

from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from ..config import BASE_DIR, settings
from ..security import LANG_COOKIE, VISITOR_COOKIE
from ..stats import record_event, record_hit
from ..store import get_content_map, list_projects, whatsapp_link

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
COOKIE_MAX_AGE = 60 * 60 * 24 * 365


def resolve_lang(request: Request) -> str:
    query_lang = request.query_params.get("lang", "").lower()
    if query_lang in settings.languages:
        return query_lang
    cookie_lang = (request.cookies.get(LANG_COOKIE) or "").lower()
    if cookie_lang in settings.languages:
        return cookie_lang
    header = request.headers.get("accept-language", "").lower()
    if header.startswith("en"):
        return "en"
    return settings.default_lang


def _device(user_agent: str) -> str:
    ua = user_agent.lower()
    if any(token in ua for token in ("iphone", "android", "mobile", "ipad", "tablet")):
        return "mobile"
    return "desktop"


def _visitor_id(request: Request, response: Response) -> str:
    current = request.cookies.get(VISITOR_COOKIE)
    if current and 8 <= len(current) <= 64:
        return current
    new_id = uuid.uuid4().hex
    response.set_cookie(
        VISITOR_COOKIE,
        new_id,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return new_id


@router.get("/", response_class=HTMLResponse)
def landing(request: Request) -> HTMLResponse:
    lang = resolve_lang(request)
    content = get_content_map(lang)
    projects = list_projects(lang=lang)
    alt_lang = "en" if lang == "es" else "es"
    context = {
        "c": content,
        "lang": lang,
        "alt_lang": alt_lang,
        "projects": projects,
        "wa_link": whatsapp_link(
            content.get("contact.whatsapp_number", ""),
            content.get("contact.whatsapp_message", ""),
        ),
        "base_url": settings.base_url,
        "year": date.today().year,
        "sections": ("inicio", "servicios", "proyectos", "nosotros", "contacto"),
    }
    response = templates.TemplateResponse(request=request, name="index.html", context=context)
    response.headers["Cache-Control"] = "no-cache"
    if request.cookies.get(LANG_COOKIE) != lang:
        response.set_cookie(
            LANG_COOKIE,
            lang,
            max_age=COOKIE_MAX_AGE,
            samesite="lax",
            path="/",
        )
    return response


@router.get("/api/content")
def api_content(request: Request) -> JSONResponse:
    lang = resolve_lang(request)
    return JSONResponse(
        {
            "lang": lang,
            "content": get_content_map(lang),
            "projects": list_projects(lang=lang),
        },
        headers={"Cache-Control": "no-store"},
    )


@router.post("/api/hit")
async def api_hit(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
    except Exception:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}

    response = JSONResponse({"ok": True})
    visitor_id = _visitor_id(request, response)
    referrer = str(payload.get("referrer") or "")[:300]
    if referrer and settings.base_url and referrer.startswith(settings.base_url):
        referrer = ""
    record_hit(
        visitor_id=visitor_id,
        path=str(payload.get("path") or "/")[:200],
        lang=str(payload.get("lang") or "es")[:2],
        referrer=referrer,
        device=_device(request.headers.get("user-agent", "")),
        user_agent=request.headers.get("user-agent", ""),
    )
    response.headers["Cache-Control"] = "no-store"
    return response


@router.post("/api/event")
async def api_event(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
    except Exception:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}

    allowed = {"whatsapp_click", "section_view", "project_click"}
    name = str(payload.get("name") or "")
    if name not in allowed:
        return JSONResponse({"ok": False, "error": "evento no permitido"}, status_code=400)

    response = JSONResponse({"ok": True})
    visitor_id = _visitor_id(request, response)
    record_event(visitor_id, name, str(payload.get("meta") or ""))
    response.headers["Cache-Control"] = "no-store"
    return response

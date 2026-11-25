"""Panel de administración: login, edición de contenido, proyectos y estadísticas."""

from __future__ import annotations

import uuid
from pathlib import Path
from urllib.parse import urlparse

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from ..config import settings
from ..security import (
    SESSION_COOKIE,
    check_password,
    clear_attempts,
    create_session_token,
    is_authenticated,
    is_locked_out,
    register_failed_attempt,
    require_admin,
)
from ..stats import stats_overview
from ..store import (
    create_project,
    delete_project,
    get_all_content,
    get_project,
    list_projects,
    save_content,
    update_project,
)
from ..content import SECTIONS
from .public import templates  # reutiliza el entorno Jinja

router = APIRouter()

SESSION_MAX_AGE = 60 * 60 * 12
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


def _same_origin(request: Request) -> bool:
    origin = request.headers.get("origin")
    if not origin:
        return True
    return urlparse(origin).netloc == request.headers.get("host", "")


def _guard(request: Request) -> None:
    require_admin(request)
    if not _same_origin(request):
        raise HTTPException(status_code=403, detail="Origen no permitido")


@router.get("/admin/login", response_class=HTMLResponse)
def login_page(request: Request, error: str = "") -> HTMLResponse:
    if is_authenticated(request):
        return RedirectResponse("/admin", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={
            "error": error,
            "admin_ready": settings.admin_ready,
            "default_password": settings.default_password_in_use,
        },
    )


@router.post("/admin/login")
async def login_submit(request: Request) -> RedirectResponse:
    if is_locked_out(request):
        return RedirectResponse("/admin/login?error=locked", status_code=303)
    form = await request.form()
    password = str(form.get("password") or "")
    if not check_password(password):
        register_failed_attempt(request)
        return RedirectResponse("/admin/login?error=1", status_code=303)

    clear_attempts(request)
    response = RedirectResponse("/admin", status_code=303)
    response.set_cookie(
        SESSION_COOKIE,
        create_session_token(),
        max_age=settings.session_hours * 3600,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return response


@router.post("/admin/logout")
def logout() -> RedirectResponse:
    response = RedirectResponse("/admin/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE, path="/")
    return response


@router.get("/admin", response_class=HTMLResponse)
def dashboard(request: Request) -> HTMLResponse:
    if not is_authenticated(request):
        return RedirectResponse("/admin/login", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "sections": SECTIONS,
            "content": get_all_content(),
            "projects": list_projects(lang="es", include_hidden=True),
            "stats": stats_overview(days=14),
            "base_url": settings.base_url,
            "default_password": settings.default_password_in_use,
        },
    )


# ------------------------------------------------------------------ contenido
@router.get("/admin/api/content")
def api_get_content(request: Request) -> JSONResponse:
    _guard(request)
    return JSONResponse(
        {"sections": SECTIONS, "content": get_all_content()},
        headers={"Cache-Control": "no-store"},
    )


@router.put("/admin/api/content")
async def api_save_content(request: Request) -> JSONResponse:
    _guard(request)
    payload = await request.json()
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Formato inválido")
    updated = save_content(payload)
    return JSONResponse({"ok": True, "updated": updated})


# ------------------------------------------------------------------- proyectos
@router.get("/admin/api/projects")
def api_projects(request: Request) -> JSONResponse:
    _guard(request)
    return JSONResponse(
        {"projects": list_projects(lang="es", include_hidden=True)},
        headers={"Cache-Control": "no-store"},
    )


@router.post("/admin/api/projects")
async def api_create_project(request: Request) -> JSONResponse:
    _guard(request)
    payload = await request.json()
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Formato inválido")
    if not str(payload.get("title_es") or "").strip():
        raise HTTPException(status_code=400, detail="El título en español es obligatorio")
    project_id = create_project(payload)
    return JSONResponse({"ok": True, "id": project_id}, status_code=201)


@router.put("/admin/api/projects/{project_id}")
async def api_update_project(project_id: int, request: Request) -> JSONResponse:
    _guard(request)
    payload = await request.json()
    if not isinstance(payload, dict) or not get_project(project_id):
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    if not str(payload.get("title_es") or "").strip():
        raise HTTPException(status_code=400, detail="El título en español es obligatorio")
    update_project(project_id, payload)
    return JSONResponse({"ok": True})


@router.delete("/admin/api/projects/{project_id}")
def api_delete_project(project_id: int, request: Request) -> JSONResponse:
    _guard(request)
    if not delete_project(project_id):
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return JSONResponse({"ok": True})


# --------------------------------------------------------------------- upload
@router.post("/admin/api/upload")
async def api_upload(request: Request, file: UploadFile = File(...)) -> JSONResponse:
    _guard(request)
    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Formato no soportado. Usa JPG, PNG, WEBP o GIF.",
        )
    data = await file.read()
    limit = settings.max_upload_mb * 1024 * 1024
    if len(data) > limit:
        raise HTTPException(
            status_code=400,
            detail=f"La imagen supera {settings.max_upload_mb} MB",
        )
    signatures = {
        b"\xff\xd8\xff": ".jpg",
        b"\x89PNG\r\n\x1a\n": ".png",
        b"GIF8": ".gif",
    }
    if not (data[:4] == b"RIFF" and data[8:12] == b"WEBP") and not any(
        data.startswith(sig) for sig in signatures
    ):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen válida")

    suffix = ALLOWED_IMAGE_TYPES[content_type]
    filename = f"{uuid.uuid4().hex}{suffix}"
    settings.ensure_dirs()
    target = Path(settings.upload_dir) / filename
    target.write_bytes(data)
    return JSONResponse({"ok": True, "url": f"/media/{filename}"})


# ---------------------------------------------------------------- estadísticas
@router.get("/admin/api/stats")
def api_stats(request: Request, days: int = 14) -> JSONResponse:
    _guard(request)
    return JSONResponse(stats_overview(days=days), headers={"Cache-Control": "no-store"})

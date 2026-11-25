"""Acceso a contenido y proyectos (con valores por defecto como respaldo)."""

from __future__ import annotations

import sqlite3
from urllib.parse import quote_plus

from .content import DEFAULTS
from .db import get_conn


def get_content_map(lang: str) -> dict[str, str]:
    """Devuelve key -> texto en el idioma pedido, con fallback al español."""
    lang = lang if lang in ("es", "en") else "es"
    with get_conn() as conn:
        rows = conn.execute("SELECT key, value_es, value_en FROM content").fetchall()
    db = {row["key"]: row for row in rows}
    result: dict[str, str] = {}
    for key, (default_es, default_en) in DEFAULTS.items():
        row = db.get(key)
        if row is None:
            result[key] = default_en if lang == "en" else default_es
            continue
        primary = row[f"value_{lang}"] or ""
        if not primary:
            primary = row["value_en"] if lang == "en" else row["value_es"]
        if not primary:
            primary = default_en if lang == "en" else default_es
        result[key] = primary
    return result


def get_all_content() -> dict[str, dict[str, str]]:
    with get_conn() as conn:
        rows = conn.execute("SELECT key, value_es, value_en FROM content").fetchall()
    data = {
        row["key"]: {"es": row["value_es"], "en": row["value_en"]} for row in rows
    }
    # Cualquier campo nuevo del catálogo aparece aunque la base sea anterior.
    for key, (default_es, default_en) in DEFAULTS.items():
        data.setdefault(key, {"es": default_es, "en": default_en})
    return data


def save_content(payload: dict[str, dict[str, str]]) -> int:
    updated = 0
    with get_conn() as conn:
        for key, values in payload.items():
            if key not in DEFAULTS or not isinstance(values, dict):
                continue
            es = str(values.get("es", ""))[:8000]
            en = str(values.get("en", ""))[:8000]
            conn.execute(
                """INSERT INTO content (key, value_es, value_en, updated_at)
                   VALUES (?, ?, ?, datetime('now'))
                   ON CONFLICT(key) DO UPDATE SET
                       value_es = excluded.value_es,
                       value_en = excluded.value_en,
                       updated_at = excluded.updated_at""",
                (key, es, en),
            )
            updated += 1
    return updated


def list_projects(lang: str = "es", include_hidden: bool = False) -> list[dict]:
    lang = lang if lang in ("es", "en") else "es"
    query = "SELECT * FROM projects"
    if not include_hidden:
        query += " WHERE visible = 1"
    query += " ORDER BY sort_order ASC, id DESC"
    with get_conn() as conn:
        rows = conn.execute(query).fetchall()
    projects = []
    for row in rows:
        projects.append(
            {
                "id": row["id"],
                "title": row[f"title_{lang}"] or row["title_es"],
                "description": row[f"description_{lang}"] or row["description_es"],
                "title_es": row["title_es"],
                "title_en": row["title_en"],
                "description_es": row["description_es"],
                "description_en": row["description_en"],
                "tags": [tag.strip() for tag in (row["tags"] or "").split(",") if tag.strip()],
                "tags_raw": row["tags"],
                "image_url": row["image_url"],
                "link_url": row["link_url"],
                "visible": bool(row["visible"]),
                "sort_order": row["sort_order"],
                "created_at": row["created_at"],
            }
        )
    return projects


def get_project(project_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


def _project_values(data: dict) -> tuple:
    def text(field: str) -> str:
        return str(data.get(field) or "").strip()[:4000]

    try:
        sort_order = int(data.get("sort_order") or 0)
    except (TypeError, ValueError):
        sort_order = 0
    return (
        text("title_es"),
        text("title_en") or text("title_es"),
        text("description_es"),
        text("description_en") or text("description_es"),
        text("tags")[:400],
        text("image_url")[:600],
        text("link_url")[:600],
        sort_order,
        1 if data.get("visible", True) else 0,
    )


def create_project(data: dict) -> int:
    values = _project_values(data)
    with get_conn() as conn:
        cursor = conn.execute(
            """INSERT INTO projects
               (title_es, title_en, description_es, description_en, tags, image_url,
                link_url, sort_order, visible)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            values,
        )
        return int(cursor.lastrowid)


def update_project(project_id: int, data: dict) -> bool:
    values = _project_values(data)
    with get_conn() as conn:
        cursor = conn.execute(
            """UPDATE projects SET
                 title_es = ?, title_en = ?, description_es = ?, description_en = ?,
                 tags = ?, image_url = ?, link_url = ?, sort_order = ?, visible = ?
               WHERE id = ?""",
            (*values, project_id),
        )
        return cursor.rowcount > 0


def delete_project(project_id: int) -> bool:
    with get_conn() as conn:
        cursor = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        return cursor.rowcount > 0


def whatsapp_link(number: str, message: str) -> str:
    digits = "".join(ch for ch in number if ch.isdigit())
    if not digits:
        return "#contacto"
    base = f"https://wa.me/{digits}"
    if message:
        base += f"?text={quote_plus(message)}"
    return base


def db_is_healthy() -> bool:
    try:
        with get_conn() as conn:
            conn.execute("SELECT 1").fetchone()
        return True
    except sqlite3.Error:
        return False

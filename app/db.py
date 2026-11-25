"""Capa de acceso a SQLite (sin ORM)."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator

from .config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS content (
    key TEXT PRIMARY KEY,
    value_es TEXT NOT NULL DEFAULT '',
    value_en TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title_es TEXT NOT NULL DEFAULT '',
    title_en TEXT NOT NULL DEFAULT '',
    description_es TEXT NOT NULL DEFAULT '',
    description_en TEXT NOT NULL DEFAULT '',
    tags TEXT NOT NULL DEFAULT '',
    image_url TEXT NOT NULL DEFAULT '',
    link_url TEXT NOT NULL DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0,
    visible INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS visitors (
    visitor_id TEXT PRIMARY KEY,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    visits INTEGER NOT NULL DEFAULT 0,
    lang TEXT NOT NULL DEFAULT 'es',
    referrer TEXT NOT NULL DEFAULT '',
    device TEXT NOT NULL DEFAULT 'desktop',
    user_agent TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS pageviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitor_id TEXT NOT NULL,
    path TEXT NOT NULL DEFAULT '/',
    lang TEXT NOT NULL DEFAULT 'es',
    referrer TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitor_id TEXT NOT NULL DEFAULT '',
    name TEXT NOT NULL,
    meta TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_pageviews_created ON pageviews(created_at);
CREATE INDEX IF NOT EXISTS idx_pageviews_visitor ON pageviews(visitor_id);
CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at);
CREATE INDEX IF NOT EXISTS idx_events_name ON events(name);
"""


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def connect() -> sqlite3.Connection:
    settings.ensure_dirs()
    conn = sqlite3.connect(settings.db_path, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=15000")
    return conn


@contextmanager
def get_conn() -> Iterator[sqlite3.Connection]:
    conn = connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Crea el esquema y siembra el contenido por defecto que falte."""
    from .content import DEFAULTS

    settings.ensure_dirs()
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        existing = {row["key"] for row in conn.execute("SELECT key FROM content")}
        missing = [(key, es, en) for key, (es, en) in DEFAULTS.items() if key not in existing]
        if missing:
            conn.executemany(
                "INSERT INTO content (key, value_es, value_en, updated_at) VALUES (?, ?, ?, ?)",
                [(key, es, en, utcnow()) for key, es, en in missing],
            )
        seeded = conn.execute("SELECT COUNT(*) AS total FROM projects").fetchone()["total"]
        if seeded == 0:
            from .content import DEFAULT_PROJECTS

            conn.executemany(
                """INSERT INTO projects
                   (title_es, title_en, description_es, description_en, tags, image_url,
                    link_url, sort_order, visible, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        project["title_es"],
                        project["title_en"],
                        project["description_es"],
                        project["description_en"],
                        project["tags"],
                        project["image_url"],
                        project["link_url"],
                        project["sort_order"],
                        1,
                        utcnow(),
                    )
                    for project in DEFAULT_PROJECTS
                ],
            )

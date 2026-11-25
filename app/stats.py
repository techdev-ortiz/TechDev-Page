"""Consultas de estadísticas del sitio."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from .db import get_conn, utcnow


def _day_key(offset: int = 0) -> str:
    return (date.today() - timedelta(days=offset)).isoformat()


def record_hit(
    visitor_id: str,
    path: str,
    lang: str,
    referrer: str,
    device: str,
    user_agent: str,
) -> None:
    now = utcnow()
    with get_conn() as conn:
        row = conn.execute(
            "SELECT visitor_id FROM visitors WHERE visitor_id = ?", (visitor_id,)
        ).fetchone()
        if row is None:
            conn.execute(
                """INSERT INTO visitors
                   (visitor_id, first_seen, last_seen, visits, lang, referrer, device, user_agent)
                   VALUES (?, ?, ?, 1, ?, ?, ?, ?)""",
                (visitor_id, now, now, lang, referrer, device, user_agent[:300]),
            )
        else:
            conn.execute(
                """UPDATE visitors
                   SET last_seen = ?, visits = visits + 1,
                       lang = ?, referrer = CASE WHEN referrer = '' THEN ? ELSE referrer END
                   WHERE visitor_id = ?""",
                (now, lang, referrer, visitor_id),
            )
        conn.execute(
            """INSERT INTO pageviews (visitor_id, path, lang, referrer, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (visitor_id, path[:200], lang, referrer[:300], now),
        )


def record_event(visitor_id: str, name: str, meta: str = "") -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO events (visitor_id, name, meta, created_at) VALUES (?, ?, ?, ?)",
            (visitor_id, name[:80], meta[:300], utcnow()),
        )


def _scalar(conn, sql: str, params: tuple = ()) -> int:
    row = conn.execute(sql, params).fetchone()
    return int(row[0] or 0) if row else 0


def stats_overview(days: int = 14) -> dict:
    days = max(1, min(days, 90))
    today = _day_key()
    with get_conn() as conn:
        total_views = _scalar(conn, "SELECT COUNT(*) FROM pageviews")
        unique_visitors = _scalar(conn, "SELECT COUNT(*) FROM visitors")
        views_today = _scalar(conn, "SELECT COUNT(*) FROM pageviews WHERE date(created_at) = ?", (today,))
        visitors_today = _scalar(
            conn,
            "SELECT COUNT(*) FROM visitors WHERE date(first_seen) = ?",
            (today,),
        )
        views_7 = _scalar(
            conn,
            "SELECT COUNT(*) FROM pageviews WHERE date(created_at) >= ?",
            (_day_key(6),),
        )
        views_30 = _scalar(
            conn,
            "SELECT COUNT(*) FROM pageviews WHERE date(created_at) >= ?",
            (_day_key(29),),
        )
        visitors_7 = _scalar(
            conn,
            "SELECT COUNT(*) FROM visitors WHERE date(first_seen) >= ?",
            (_day_key(6),),
        )
        visitors_30 = _scalar(
            conn,
            "SELECT COUNT(*) FROM visitors WHERE date(first_seen) >= ?",
            (_day_key(29),),
        )
        whatsapp_clicks = _scalar(
            conn, "SELECT COUNT(*) FROM events WHERE name = 'whatsapp_click'"
        )
        section_views = {
            row["meta"] or "sin-dato": int(row["total"])
            for row in conn.execute(
                """SELECT meta, COUNT(*) AS total FROM events
                   WHERE name = 'section_view' AND date(created_at) >= ?
                   GROUP BY meta ORDER BY total DESC LIMIT 8""",
                (_day_key(29),),
            )
        }
        lang_rows = conn.execute(
            "SELECT lang, COUNT(*) AS total FROM visitors GROUP BY lang ORDER BY total DESC"
        ).fetchall()
        device_rows = conn.execute(
            "SELECT device, COUNT(*) AS total FROM visitors GROUP BY device ORDER BY total DESC"
        ).fetchall()
        referrers = [
            {"source": row["source"] or "directo", "total": int(row["total"])}
            for row in conn.execute(
                """SELECT CASE WHEN referrer = '' THEN 'directo' ELSE referrer END AS source,
                          COUNT(*) AS total
                   FROM visitors GROUP BY source ORDER BY total DESC LIMIT 6"""
            )
        ]
        recent = [
            {
                "visitor": row["visitor_id"][:8],
                "path": row["path"],
                "lang": row["lang"],
                "when": row["created_at"],
            }
            for row in conn.execute(
                """SELECT visitor_id, path, lang, created_at FROM pageviews
                   ORDER BY id DESC LIMIT 12"""
            )
        ]
        projects_total = _scalar(conn, "SELECT COUNT(*) FROM projects")
        projects_visible = _scalar(conn, "SELECT COUNT(*) FROM projects WHERE visible = 1")
        content_total = _scalar(conn, "SELECT COUNT(*) FROM content")

        daily = []
        for offset in range(days - 1, -1, -1):
            day = date.today() - timedelta(days=offset)
            day_str = day.isoformat()
            views = _scalar(
                conn,
                "SELECT COUNT(*) FROM pageviews WHERE date(created_at) = ?",
                (day_str,),
            )
            visitors = _scalar(
                conn,
                "SELECT COUNT(*) FROM visitors WHERE date(first_seen) = ?",
                (day_str,),
            )
            daily.append({"date": day_str, "label": day.strftime("%d/%m"), "views": views, "visitors": visitors})

    peak = max((item["views"] for item in daily), default=0)
    return {
        "totals": {
            "pageviews": total_views,
            "unique_visitors": unique_visitors,
            "views_today": views_today,
            "visitors_today": visitors_today,
            "views_7d": views_7,
            "views_30d": views_30,
            "visitors_7d": visitors_7,
            "visitors_30d": visitors_30,
            "whatsapp_clicks": whatsapp_clicks,
            "projects": projects_total,
            "projects_visible": projects_visible,
            "editable_fields": content_total,
            "avg_views_per_visitor": round(total_views / unique_visitors, 2) if unique_visitors else 0,
        },
        "daily": daily,
        "daily_peak": peak,
        "languages": [{"lang": row["lang"], "total": int(row["total"])} for row in lang_rows],
        "devices": [{"device": row["device"], "total": int(row["total"])} for row in device_rows],
        "referrers": referrers,
        "recent": recent,
        "sections": section_views,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }

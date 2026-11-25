"""Autenticación del panel, firma de cookies y protección contra fuerza bruta."""

from __future__ import annotations

import hashlib
import hmac
import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import HTTPException, Request, status

from .config import settings

SESSION_COOKIE = "td_admin"
VISITOR_COOKIE = "td_vid"
LANG_COOKIE = "td_lang"

MAX_ATTEMPTS = 8
ATTEMPT_WINDOW = 600  # segundos
_attempts: dict[str, deque[float]] = defaultdict(deque)
_attempts_lock = Lock()


def _sign(payload: str) -> str:
    return hmac.new(
        settings.session_secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def create_session_token() -> str:
    issued = str(int(time.time()))
    return f"{issued}.{_sign(issued)}"


def verify_session_token(token: str | None) -> bool:
    if not token:
        return False
    try:
        issued, signature = token.split(".", 1)
        issued_ts = int(issued)
    except (ValueError, AttributeError):
        return False
    if not hmac.compare_digest(signature, _sign(issued)):
        return False
    return (time.time() - issued_ts) < settings.session_hours * 3600


def check_password(candidate: str) -> bool:
    if not settings.admin_ready:
        return False
    return hmac.compare_digest(candidate.encode("utf-8"), settings.password.encode("utf-8"))


def client_key(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "desconocido"


def is_locked_out(request: Request) -> bool:
    key = client_key(request)
    now = time.time()
    with _attempts_lock:
        bucket = _attempts[key]
        while bucket and now - bucket[0] > ATTEMPT_WINDOW:
            bucket.popleft()
        return len(bucket) >= MAX_ATTEMPTS


def register_failed_attempt(request: Request) -> None:
    key = client_key(request)
    with _attempts_lock:
        _attempts[key].append(time.time())


def clear_attempts(request: Request) -> None:
    key = client_key(request)
    with _attempts_lock:
        _attempts.pop(key, None)


def is_authenticated(request: Request) -> bool:
    return verify_session_token(request.cookies.get(SESSION_COOKIE))


def require_admin(request: Request) -> None:
    if not is_authenticated(request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")

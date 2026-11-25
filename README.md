# TechDev · Landing de servicios de programación

Landing page profesional para promocionar servicios de desarrollo de software, con
panel de administración privado, contenido editable en dos idiomas (ES/EN),
estadísticas de visitas y despliegue con Docker.

- **Sitio público:** `http://localhost:8000/`
- **Administración:** `http://localhost:8000/admin`
- **Salud del servicio:** `http://localhost:8000/health`

## Stack

| Capa | Tecnología |
| --- | --- |
| Backend | Python 3.11+ · FastAPI · Uvicorn |
| Plantillas | Jinja2 (SSR) + hidratación con JavaScript vanilla |
| Dependencias | [uv](https://docs.astral.sh/uv/) (`pyproject.toml` + `uv.lock`) |
| Persistencia | SQLite (archivo montado como volumen Docker) |
| Frontend | HTML + CSS + JS vanilla (glassmorphism, animaciones, SPA) |
| Contenedores | Dockerfile multi-stage + docker compose |

## Despliegue paso a paso (Docker)

1. **Requisitos:** Docker 24+ y Docker Compose v2.

2. **Crea el archivo de entorno** en la raíz del proyecto:

   ```bash
   cp .env.example .env
   ```

   Edita `.env` y define al menos:

   ```env
   TECHDEV_PASSWORD=una-clave-larga-y-segura
   APP_BASE_URL=https://tudominio.com
   ```

   > El panel `/admin` solo acepta la contraseña definida en `TECHDEV_PASSWORD`.
   > Si no se define, el panel queda bloqueado. `docker-compose.yml` incluye una
   > contraseña de ejemplo (`cambiar-esta-clave`) para que el contenedor arranque
   > sin errores; cámbiala antes de publicar.

3. **Levanta el sitio:**

   ```bash
   docker compose up --build
   ```

   Para dejarlo corriendo en segundo plano:

   ```bash
   docker compose up --build -d
   docker compose ps
   ```

4. **Abre** `http://localhost:8000/` y verifica el panel en
   `http://localhost:8000/admin`.

5. **Detener / reiniciar:**

   ```bash
   docker compose down          # detiene (conserva datos)
   docker compose restart       # reinicia el servicio
   docker compose logs -f       # logs en vivo
   ```

El volumen nombrado `techdev_data` guarda la base de datos SQLite y las imágenes
subidas, por lo que los cambios realizados desde `/admin` sobreviven a reinicios y
rebuilds (`docker compose down` no borra el volumen; `docker compose down -v` sí).

## Variables de entorno

| Variable | Obligatoria | Por defecto | Descripción |
| --- | --- | --- | --- |
| `TECHDEV_PASSWORD` | Sí | `cambiar-esta-clave` (solo en compose) | Contraseña del panel `/admin` |
| `TECHDEV_SESSION_SECRET` | No | derivado de la contraseña | Secreto para firmar la cookie de sesión. Recomendado en producción |
| `APP_BASE_URL` | No | `http://localhost:8000` | URL pública usada en canonical, Open Graph, `robots.txt` y `sitemap.xml` |
| `TECHDEV_DB_PATH` | No | `data/app.db` | Ruta del archivo SQLite (en Docker: `/app/data/app.db`) |
| `TECHDEV_UPLOAD_DIR` | No | `data/uploads` | Carpeta de imágenes subidas (en Docker: `/app/data/uploads`) |
| `TECHDEV_SESSION_HOURS` | No | `12` | Duración de la sesión del panel |
| `PORT` | No | `8000` | Puerto publicado por docker compose |

## Desarrollo local (sin Docker)

```bash
uv sync                     # crea .venv e instala dependencias desde uv.lock
export TECHDEV_PASSWORD=clave-local
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Si modificas dependencias:

```bash
uv add <paquete>            # actualiza pyproject.toml + uv.lock
```

## Panel de administración

`/admin` requiere la contraseña configurada. Una vez dentro:

- **Estadísticas:** visitas totales, visitantes únicos (sin duplicar por cookie),
  visitas de hoy/7/30 días, clics en WhatsApp, secciones más vistas, origen del
  tráfico, idioma, dispositivo, actividad reciente y gráfico de 14 días.
- **Contenido:** todos los textos e imágenes de la landing, agrupados por sección,
  con campos en español e inglés. Las imágenes se pueden subir desde el panel
  (JPG/PNG/WEBP/GIF, máximo 5 MB) o indicar una ruta/URL.
- **Proyectos:** crear, editar, ordenar, ocultar y eliminar proyectos terminados,
  con imagen y enlace opcional.

Los cambios se guardan en SQLite (`content` para clave-valor y `projects` para los
proyectos). El login bloquea temporalmente la IP tras 8 intentos fallidos.

## Idiomas

El sitio se sirve por defecto en español. El selector del encabezado cambia a
inglés sin recargar la página (obtiene el contenido de `/api/content?lang=en`) y
guarda la preferencia en una cookie. También se puede forzar con `/?lang=en`
(útil para SEO y enlaces compartidos).

## SEO

- Renderizado del lado del servidor (Jinja2): título, descripción, keywords,
  canonical, `hreflang`, Open Graph, Twitter Cards y datos estructurados
  `ProfessionalService` (JSON-LD) presentes en el HTML inicial.
- `robots.txt` y `sitemap.xml` generados dinámicamente con `APP_BASE_URL`.
- Navegación SPA con `history.pushState` y anclas (`/#servicios`, `/#proyectos`,
  `/#nosotros`, `/#contacto`) para compartir secciones.

## Estructura

```
.
├── app/
│   ├── main.py              # FastAPI, middlewares y montaje de routers
│   ├── config.py            # configuración por variables de entorno
│   ├── db.py                # esquema SQLite, conexión y seed
│   ├── content.py           # catálogo de campos editables + valores ES/EN
│   ├── store.py             # contenido, proyectos y enlaces de WhatsApp
│   ├── security.py          # login, cookie firmada y anti fuerza bruta
│   ├── stats.py             # registro y consultas de estadísticas
│   ├── routers/
│   │   ├── public.py        # landing, /api/content, /api/hit, /api/event
│   │   ├── admin.py         # login, contenido, proyectos, uploads, stats
│   │   └── seo.py           # robots.txt, sitemap.xml, /media, /health
│   ├── templates/           # index.html + admin/
│   └── static/              # css, js e imágenes
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

## Persistencia y respaldos

La base de datos es un único archivo SQLite dentro del volumen `techdev_data`.

```bash
# Copia de seguridad del volumen a un archivo .tar.gz
docker run --rm -v techdev_data:/data -v "$PWD":/backup alpine \
  tar czf /backup/techdev-backup.tar.gz -C /data .
```

Para restaurar, extrae el archivo en un volumen nuevo antes de arrancar el
servicio. Las imágenes subidas desde el panel viven en `/app/data/uploads`.

## Verificación rápida

```bash
curl -s http://localhost:8000/ | grep -E '<title>|og:title|description'
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/robots.txt
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/sitemap.xml
curl -s http://localhost:8000/health
```

## Seguridad

- Cambia `TECHDEV_PASSWORD` y define `TECHDEV_SESSION_SECRET` antes de publicar.
- Publica detrás de HTTPS (Nginx, Caddy o Traefik) y pasa las cabeceras
  `X-Forwarded-*`; el contenedor ya arranca Uvicorn con `--proxy-headers`.
- El panel envía `X-Frame-Options`, `X-Content-Type-Options`,
  `Referrer-Policy` y limita la tasa de intentos de login.
- Las imágenes subidas se validan por tipo MIME y firma de archivo.

## Solución de problemas

- **`/admin` indica que falta la contraseña:** define `TECHDEV_PASSWORD` en `.env`
  y ejecuta `docker compose up -d --build`.
- **El panel no guarda cambios:** revisa que el volumen `techdev_data` exista y
  que el contenedor tenga permisos de escritura en `/app/data`.
- **Enlaces/canonical con el puerto equivocado:** ajusta `APP_BASE_URL` al dominio
  real y vuelve a levantar el servicio.
- **Puerto 8000 ocupado:** cambia `PORT=8080` en `.env`.

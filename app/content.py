"""Catálogo de contenido editable y valores por defecto (ES / EN)."""

from __future__ import annotations

# key -> (texto en español, texto en inglés)
DEFAULTS: dict[str, tuple[str, str]] = {
    # ---------------------------------------------------------------- general
    "site.name": ("TechDev", "TechDev"),
    "site.tagline": (
        "Desarrollo de software a medida",
        "Custom software development",
    ),
    "meta.title": (
        "TechDev | Desarrollo de software a medida",
        "TechDev | Custom software development",
    ),
    "meta.description": (
        "Desarrollo de páginas web, apps Android, bots de Telegram y Discord, APIs, "
        "backends y sistemas de trabajo automatizado para personas y empresas.",
        "Custom websites, Android apps, Telegram and Discord bots, APIs, backends and "
        "automated workflows for individuals and companies.",
    ),
    "meta.keywords": (
        "desarrollo web, aplicaciones android, bots telegram, bots discord, apis, "
        "backend, automatización, software a medida",
        "web development, android apps, telegram bots, discord bots, apis, backend, "
        "automation, custom software",
    ),
    "meta.og_image": ("/static/img/hero.jpg", "/static/img/hero.jpg"),
    "loader.text": ("Cargando experiencia", "Loading experience"),
    "ui.menu": ("Menú", "Menu"),
    "ui.skip": ("Ir al contenido", "Skip to content"),
    "ui.lang_switch": ("English", "Español"),
    "ui.whatsapp": ("WhatsApp", "WhatsApp"),
    "nav.home": ("Inicio", "Home"),
    "nav.services": ("Servicios", "Services"),
    "nav.projects": ("Proyectos", "Projects"),
    "nav.about": ("Nosotros", "About"),
    "nav.contact": ("Contacto", "Contact"),
    # ------------------------------------------------------------------- hero
    "hero.badge": (
        "Disponible para nuevos proyectos",
        "Available for new projects",
    ),
    "hero.title": ("Convertimos ideas", "We turn ideas"),
    "hero.highlight": ("en software que rinde", "into software that performs"),
    "hero.subtitle": (
        "Diseñamos y desarrollamos páginas web, apps Android, bots, APIs y sistemas "
        "automatizados para personas y empresas que quieren crecer con tecnología.",
        "We design and build websites, Android apps, bots, APIs and automated systems "
        "for individuals and companies ready to grow with technology.",
    ),
    "hero.primary_cta": ("Ver servicios", "See services"),
    "hero.secondary_cta": ("Hablemos de tu idea", "Let's talk"),
    "hero.image": ("/static/img/hero.jpg", "/static/img/hero.jpg"),
    "hero.image_alt": (
        "Paneles de vidrio con bordes azules iluminados",
        "Glass panels with glowing blue edges",
    ),
    "hero.stat1_value": ("120+", "120+"),
    "hero.stat1_label": ("Proyectos entregados", "Projects delivered"),
    "hero.stat2_value": ("7", "7"),
    "hero.stat2_label": ("Servicios especializados", "Specialized services"),
    "hero.stat3_value": ("<24h", "<24h"),
    "hero.stat3_label": ("Respuesta promedio", "Average response"),
    "hero.stat4_value": ("98%", "98%"),
    "hero.stat4_label": ("Clientes satisfechos", "Happy clients"),
    # --------------------------------------------------------------- services
    "services.eyebrow": ("Servicios", "Services"),
    "services.title": (
        "Soluciones completas, de la idea al deploy",
        "Complete solutions, from idea to deploy",
    ),
    "services.subtitle": (
        "Elegimos la tecnología según tu objetivo, no al revés. Cada proyecto incluye "
        "código limpio, documentación y soporte después de la entrega.",
        "We choose the technology around your goal, not the other way around. Every "
        "project ships with clean code, documentation and post-delivery support.",
    ),
    "services.s1.icon": ("🌐", "🌐"),
    "services.s1.title": ("Desarrollo de páginas web", "Website development"),
    "services.s1.desc": (
        "Sitios rápidos, responsivos y optimizados para SEO. Diseño a medida, panel de "
        "administración y despliegue incluido.",
        "Fast, responsive, SEO-ready websites. Custom design, admin panel and deployment "
        "included.",
    ),
    "services.s2.icon": ("📱", "📱"),
    "services.s2.title": ("Aplicaciones Android", "Android applications"),
    "services.s2.desc": (
        "Apps nativas y multiplataforma con Kotlin o Flutter, listas para Play Store y "
        "conectadas a tu backend.",
        "Native and cross-platform apps with Kotlin or Flutter, ready for Play Store and "
        "wired to your backend.",
    ),
    "services.s3.icon": ("🤖", "🤖"),
    "services.s3.title": ("Bots de Telegram", "Telegram bots"),
    "services.s3.desc": (
        "Automatiza atención, ventas y notificaciones con bots robustos, comandos claros "
        "y pagos integrados.",
        "Automate support, sales and notifications with robust bots, clear commands and "
        "integrated payments.",
    ),
    "services.s4.icon": ("🎮", "🎮"),
    "services.s4.title": ("Bots de Discord", "Discord bots"),
    "services.s4.desc": (
        "Comunidades y servidores con moderación automática, roles, economía y paneles de "
        "administración.",
        "Communities and servers with automated moderation, roles, economy and admin "
        "panels.",
    ),
    "services.s5.icon": ("🔌", "🔌"),
    "services.s5.title": ("APIs", "APIs"),
    "services.s5.desc": (
        "APIs REST y GraphQL documentadas, seguras y escalables, con autenticación y "
        "pruebas automatizadas.",
        "Documented, secure and scalable REST and GraphQL APIs with authentication and "
        "automated tests.",
    ),
    "services.s6.icon": ("🧱", "🧱"),
    "services.s6.title": ("Backends", "Backends"),
    "services.s6.desc": (
        "Arquitecturas con FastAPI, bases de datos y colas de trabajo preparadas para "
        "crecer sin fricción.",
        "FastAPI architectures, databases and job queues built to grow without friction.",
    ),
    "services.s7.icon": ("⚙️", "⚙️"),
    "services.s7.title": (
        "Sistemas de trabajo automatizado",
        "Automated workflow systems",
    ),
    "services.s7.desc": (
        "Flujos que conectan tus herramientas: reportes, respaldos, integraciones y "
        "tareas sin intervención manual.",
        "Workflows that connect your tools: reports, backups, integrations and tasks "
        "without manual intervention.",
    ),
    "services.cta_title": (
        "¿Tu proyecto no encaja en ninguna categoría?",
        "Your project doesn't fit any category?",
    ),
    "services.cta_text": (
        "Cuéntanos qué necesitas y armamos una propuesta técnica sin costo.",
        "Tell us what you need and we'll put together a free technical proposal.",
    ),
    "services.cta_button": ("Solicitar propuesta", "Request a proposal"),
    # --------------------------------------------------------------- projects
    "projects.eyebrow": ("Proyectos", "Projects"),
    "projects.title": ("Trabajo reciente", "Recent work"),
    "projects.subtitle": (
        "Una selección de sistemas, apps y sitios que ya están en producción.",
        "A selection of systems, apps and sites already running in production.",
    ),
    "projects.empty": (
        "Muy pronto publicaremos nuevos proyectos.",
        "New projects coming very soon.",
    ),
    "projects.link_label": ("Ver proyecto", "View project"),
    # ------------------------------------------------------------------ about
    "about.eyebrow": ("Nosotros", "About"),
    "about.title": (
        "Un equipo pequeño, obsesionado con la calidad",
        "A small team obsessed with quality",
    ),
    "about.text1": (
        "Somos desarrolladores que trabajan cerca del cliente: sin intermediarios ni "
        "promesas vacías. Analizamos tu proceso, proponemos la solución más simple que "
        "resuelve el problema y la construimos por etapas.",
        "We are developers who work close to the client: no middlemen, no empty promises. "
        "We study your process, propose the simplest solution that solves the problem and "
        "build it in stages.",
    ),
    "about.text2": (
        "Escribimos código mantenible, documentamos cada entrega y te dejamos el control "
        "total del proyecto.",
        "We write maintainable code, document every delivery and leave you in full control "
        "of the project.",
    ),
    "about.image": ("/static/img/about.jpg", "/static/img/about.jpg"),
    "about.image_alt": (
        "Espacio de trabajo de desarrollo con luz azul",
        "Developer workspace with blue lighting",
    ),
    "about.badge_value": ("5+", "5+"),
    "about.badge_label": ("años construyendo software", "years building software"),
    "about.p1_title": ("Comunicación directa", "Direct communication"),
    "about.p1_text": (
        "Hablas siempre con quien escribe el código.",
        "You always talk to the person writing the code.",
    ),
    "about.p2_title": ("Entregas por etapas", "Staged delivery"),
    "about.p2_text": (
        "Ves avances reales cada semana, no al final.",
        "You see real progress every week, not at the end.",
    ),
    "about.p3_title": ("El código es tuyo", "The code is yours"),
    "about.p3_text": (
        "Repositorio, documentación y despliegue a tu nombre.",
        "Repository, documentation and deployment in your name.",
    ),
    # ---------------------------------------------------------------- contact
    "contact.eyebrow": ("Contacto", "Contact"),
    "contact.title": ("Hablemos de tu proyecto", "Let's talk about your project"),
    "contact.subtitle": (
        "Escríbenos por WhatsApp y en menos de 24 horas tendrás una respuesta con los "
        "siguientes pasos.",
        "Message us on WhatsApp and within 24 hours you'll get a reply with the next steps.",
    ),
    "contact.whatsapp_number": ("521234567890", "521234567890"),
    "contact.whatsapp_message": (
        "Hola TechDev, quiero cotizar un proyecto de software.",
        "Hi TechDev, I'd like a quote for a software project.",
    ),
    "contact.whatsapp_cta": ("Escribir por WhatsApp", "Message on WhatsApp"),
    "contact.whatsapp_hint": (
        "Respuesta promedio en 24 horas hábiles.",
        "Average reply within 24 business hours.",
    ),
    "contact.card1_title": ("WhatsApp", "WhatsApp"),
    "contact.card1_text": (
        "La vía más rápida: escríbenos y coordinamos una llamada.",
        "The fastest way: message us and we'll set up a call.",
    ),
    "contact.card2_title": ("Horario", "Schedule"),
    "contact.card2_text": (
        "Lunes a viernes, 9:00 a 18:00 (GMT-6).",
        "Monday to Friday, 9:00 to 18:00 (GMT-6).",
    ),
    "contact.card3_title": ("Trabajo remoto", "Remote work"),
    "contact.card3_text": (
        "Atendemos clientes de cualquier país, 100% en línea.",
        "We work with clients in any country, 100% online.",
    ),
    # ----------------------------------------------------------------- footer
    "footer.about": (
        "Desarrollo de software a medida para personas y empresas.",
        "Custom software development for individuals and companies.",
    ),
    "footer.nav_title": ("Navegación", "Navigation"),
    "footer.contact_title": ("Contacto", "Contact"),
    "footer.rights": (
        "Todos los derechos reservados.",
        "All rights reserved.",
    ),
    "footer.built": (
        "Hecho con FastAPI, SQLite y mucho café.",
        "Built with FastAPI, SQLite and plenty of coffee.",
    ),
}

# Agrupación para el panel de administración.
# Cada campo: (key, etiqueta, tipo) y tipo ∈ {text, textarea, image}
SECTIONS: list[dict] = [
    {
        "id": "general",
        "title": "General y SEO",
        "description": "Nombre del sitio, navegación y metadatos para buscadores.",
        "fields": [
            ("site.name", "Nombre del sitio", "text"),
            ("site.tagline", "Eslogan corto", "text"),
            ("meta.title", "Título SEO", "textarea"),
            ("meta.description", "Descripción SEO", "textarea"),
            ("meta.keywords", "Palabras clave SEO", "textarea"),
            ("meta.og_image", "Imagen para compartir (Open Graph)", "image"),
            ("loader.text", "Texto del loader", "text"),
            ("ui.menu", "Etiqueta del menú móvil", "text"),
            ("ui.skip", "Accesibilidad: ir al contenido", "text"),
            ("ui.lang_switch", "Botón de idioma (texto mostrado)", "text"),
            ("nav.home", "Navegación: Inicio", "text"),
            ("nav.services", "Navegación: Servicios", "text"),
            ("nav.projects", "Navegación: Proyectos", "text"),
            ("nav.about", "Navegación: Nosotros", "text"),
            ("nav.contact", "Navegación: Contacto", "text"),
        ],
    },
    {
        "id": "hero",
        "title": "Inicio (hero)",
        "description": "Primera pantalla: mensaje principal, llamados a la acción y métricas.",
        "fields": [
            ("hero.badge", "Etiqueta superior", "text"),
            ("hero.title", "Título (primera parte)", "text"),
            ("hero.highlight", "Título (parte resaltada)", "text"),
            ("hero.subtitle", "Subtítulo", "textarea"),
            ("hero.primary_cta", "Botón principal", "text"),
            ("hero.secondary_cta", "Botón secundario", "text"),
            ("hero.image", "Imagen principal", "image"),
            ("hero.image_alt", "Texto alternativo de la imagen", "text"),
            ("hero.stat1_value", "Métrica 1: valor", "text"),
            ("hero.stat1_label", "Métrica 1: etiqueta", "text"),
            ("hero.stat2_value", "Métrica 2: valor", "text"),
            ("hero.stat2_label", "Métrica 2: etiqueta", "text"),
            ("hero.stat3_value", "Métrica 3: valor", "text"),
            ("hero.stat3_label", "Métrica 3: etiqueta", "text"),
            ("hero.stat4_value", "Métrica 4: valor", "text"),
            ("hero.stat4_label", "Métrica 4: etiqueta", "text"),
        ],
    },
    {
        "id": "services",
        "title": "Servicios",
        "description": "Las siete tarjetas de servicios y el bloque de cierre.",
        "fields": [
            ("services.eyebrow", "Etiqueta de sección", "text"),
            ("services.title", "Título", "text"),
            ("services.subtitle", "Subtítulo", "textarea"),
            ("services.s1.icon", "Servicio 1: icono (emoji)", "text"),
            ("services.s1.title", "Servicio 1: título", "text"),
            ("services.s1.desc", "Servicio 1: descripción", "textarea"),
            ("services.s2.icon", "Servicio 2: icono (emoji)", "text"),
            ("services.s2.title", "Servicio 2: título", "text"),
            ("services.s2.desc", "Servicio 2: descripción", "textarea"),
            ("services.s3.icon", "Servicio 3: icono (emoji)", "text"),
            ("services.s3.title", "Servicio 3: título", "text"),
            ("services.s3.desc", "Servicio 3: descripción", "textarea"),
            ("services.s4.icon", "Servicio 4: icono (emoji)", "text"),
            ("services.s4.title", "Servicio 4: título", "text"),
            ("services.s4.desc", "Servicio 4: descripción", "textarea"),
            ("services.s5.icon", "Servicio 5: icono (emoji)", "text"),
            ("services.s5.title", "Servicio 5: título", "text"),
            ("services.s5.desc", "Servicio 5: descripción", "textarea"),
            ("services.s6.icon", "Servicio 6: icono (emoji)", "text"),
            ("services.s6.title", "Servicio 6: título", "text"),
            ("services.s6.desc", "Servicio 6: descripción", "textarea"),
            ("services.s7.icon", "Servicio 7: icono (emoji)", "text"),
            ("services.s7.title", "Servicio 7: título", "text"),
            ("services.s7.desc", "Servicio 7: descripción", "textarea"),
            ("services.cta_title", "Cierre: título", "text"),
            ("services.cta_text", "Cierre: texto", "textarea"),
            ("services.cta_button", "Cierre: botón", "text"),
        ],
    },
    {
        "id": "projects",
        "title": "Proyectos",
        "description": "Encabezado de la sección. Los proyectos se gestionan en la pestaña Proyectos.",
        "fields": [
            ("projects.eyebrow", "Etiqueta de sección", "text"),
            ("projects.title", "Título", "text"),
            ("projects.subtitle", "Subtítulo", "textarea"),
            ("projects.empty", "Mensaje sin proyectos", "text"),
            ("projects.link_label", "Texto del enlace de proyecto", "text"),
        ],
    },
    {
        "id": "about",
        "title": "Sobre nosotros",
        "description": "Historia, imagen y puntos de valor.",
        "fields": [
            ("about.eyebrow", "Etiqueta de sección", "text"),
            ("about.title", "Título", "text"),
            ("about.text1", "Párrafo 1", "textarea"),
            ("about.text2", "Párrafo 2", "textarea"),
            ("about.image", "Imagen de la sección", "image"),
            ("about.image_alt", "Texto alternativo de la imagen", "text"),
            ("about.badge_value", "Insignia: valor", "text"),
            ("about.badge_label", "Insignia: etiqueta", "text"),
            ("about.p1_title", "Punto 1: título", "text"),
            ("about.p1_text", "Punto 1: texto", "textarea"),
            ("about.p2_title", "Punto 2: título", "text"),
            ("about.p2_text", "Punto 2: texto", "textarea"),
            ("about.p3_title", "Punto 3: título", "text"),
            ("about.p3_text", "Punto 3: texto", "textarea"),
        ],
    },
    {
        "id": "contact",
        "title": "Contacto",
        "description": "Número de WhatsApp, mensaje precargado y tarjetas informativas.",
        "fields": [
            ("contact.eyebrow", "Etiqueta de sección", "text"),
            ("contact.title", "Título", "text"),
            ("contact.subtitle", "Subtítulo", "textarea"),
            ("contact.whatsapp_number", "Número de WhatsApp (solo dígitos)", "text"),
            ("contact.whatsapp_message", "Mensaje precargado de WhatsApp", "textarea"),
            ("contact.whatsapp_cta", "Texto del botón de WhatsApp", "text"),
            ("contact.whatsapp_hint", "Nota bajo el botón", "text"),
            ("contact.card1_title", "Tarjeta 1: título", "text"),
            ("contact.card1_text", "Tarjeta 1: texto", "textarea"),
            ("contact.card2_title", "Tarjeta 2: título", "text"),
            ("contact.card2_text", "Tarjeta 2: texto", "textarea"),
            ("contact.card3_title", "Tarjeta 3: título", "text"),
            ("contact.card3_text", "Tarjeta 3: texto", "textarea"),
        ],
    },
    {
        "id": "footer",
        "title": "Footer",
        "description": "Textos del pie de página.",
        "fields": [
            ("footer.about", "Descripción corta", "textarea"),
            ("footer.nav_title", "Título de navegación", "text"),
            ("footer.contact_title", "Título de contacto", "text"),
            ("footer.rights", "Texto de derechos", "text"),
            ("footer.built", "Crédito final", "text"),
        ],
    },
]

# Secciones visibles de la landing, usadas para navegación y eventos de estadísticas.
SITE_SECTIONS = ("inicio", "servicios", "proyectos", "nosotros", "contacto")

DEFAULT_PROJECTS = [
    {
        "title_es": "Panel de pedidos para restaurante",
        "title_en": "Restaurant order dashboard",
        "description_es": (
            "Sistema web con pedidos en tiempo real, vista de cocina y reportes diarios "
            "para una cadena de cuatro sucursales."
        ),
        "description_en": (
            "Web system with real-time orders, kitchen view and daily reports for a "
            "four-branch restaurant chain."
        ),
        "tags": "FastAPI, SQLite, WebSockets",
        "image_url": "/static/img/projects/panel-pedidos.jpg",
        "link_url": "",
        "sort_order": 1,
    },
    {
        "title_es": "Bot de ventas en Telegram",
        "title_en": "Telegram sales bot",
        "description_es": (
            "Bot con catálogo, carrito y pagos en línea que automatiza el 80% de los "
            "pedidos de una tienda de insumos."
        ),
        "description_en": (
            "Bot with catalog, cart and online payments that automates 80% of the orders "
            "for a supply store."
        ),
        "tags": "Python, Telegram API, Stripe",
        "image_url": "/static/img/projects/bot-telegram.jpg",
        "link_url": "",
        "sort_order": 2,
    },
    {
        "title_es": "API de logística",
        "title_en": "Logistics API",
        "description_es": (
            "API REST que conecta inventario, transporte y facturación de una empresa "
            "distribuidora, con autenticación por roles."
        ),
        "description_en": (
            "REST API connecting inventory, transport and invoicing for a distribution "
            "company, with role-based authentication."
        ),
        "tags": "FastAPI, PostgreSQL, Docker",
        "image_url": "/static/img/projects/api-logistica.jpg",
        "link_url": "",
        "sort_order": 3,
    },
    {
        "title_es": "App Android para trabajo en terreno",
        "title_en": "Android field-work app",
        "description_es": (
            "Aplicación offline-first para técnicos en terreno con sincronización "
            "automática al recuperar conexión."
        ),
        "description_en": (
            "Offline-first app for field technicians with automatic sync once the "
            "connection returns."
        ),
        "tags": "Kotlin, Room, Retrofit",
        "image_url": "/static/img/projects/app-android.jpg",
        "link_url": "",
        "sort_order": 4,
    },
]


def default_content() -> dict[str, dict[str, str]]:
    return {key: {"es": es, "en": en} for key, (es, en) in DEFAULTS.items()}

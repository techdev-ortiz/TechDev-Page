/* ============================================================================
   TechDev · Landing pública
   Loader, navegación SPA, animaciones, idioma y analítica.
   ========================================================================== */
(() => {
  "use strict";

  const body = document.body;
  const html = document.documentElement;
  const header = document.getElementById("site-header");
  const loader = document.getElementById("loader");
  const nav = document.getElementById("primary-nav");
  const navToggle = document.getElementById("nav-toggle");
  const langButton = document.querySelector("[data-lang-switch]");
  const langLabel = document.querySelector("[data-lang-label]");
  const toast = document.getElementById("site-toast");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let currentLang = html.lang || "es";
  let toastTimer = null;

  /* ------------------------------------------------------------------ utils */
  const post = (url, payload) => {
    try {
      return fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload),
        keepalive: true,
      }).catch(() => null);
    } catch {
      return null;
    }
  };

  const showToast = (message) => {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("is-visible"), 2600);
  };

  const setMeta = (key, value, attribute = "name") => {
    if (!value) return;
    const node = document.querySelector(`meta[${attribute}="${key}"]`);
    if (node) node.setAttribute("content", value);
  };

  const activeSection = (id) => {
    document.querySelectorAll(".nav__link[data-section]").forEach((link) => {
      link.classList.toggle("is-active", link.dataset.section === id);
    });
  };

  /* ---------------------------------------------------------------- loader */
  const startedAt = performance.now();
  let loaderHidden = false;

  const hideLoader = () => {
    if (loaderHidden || !loader) return;
    loaderHidden = true;
    const elapsed = performance.now() - startedAt;
    const wait = Math.max(0, 700 - elapsed);
    setTimeout(() => {
      loader.classList.add("is-hidden");
      body.classList.remove("is-loading");
      setTimeout(() => loader.remove(), 800);
      if (location.hash) {
        const id = location.hash.slice(1);
        requestAnimationFrame(() => scrollToSection(id, false, true));
      }
    }, wait);
  };

  if (document.readyState === "complete") {
    hideLoader();
  } else {
    window.addEventListener("load", hideLoader, { once: true });
  }
  setTimeout(hideLoader, 4200);

  /* ------------------------------------------------------- header + mobile */
  const onScroll = () => {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 10);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const closeNav = () => {
    if (!nav || !navToggle) return;
    nav.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
  };

  navToggle?.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  document.addEventListener("click", (event) => {
    if (!nav || !navToggle) return;
    if (!nav.contains(event.target) && !navToggle.contains(event.target)) closeNav();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeNav();
  });

  /* -------------------------------------------------------------- SPA nav */
  const scrollToSection = (id, updateHistory = true, immediate = false) => {
    const target = document.getElementById(id);
    if (!target) return;
    const offset = (header?.offsetHeight || 72) + 14;
    const top = target.getBoundingClientRect().top + window.scrollY - offset;
    window.scrollTo({
      top: Math.max(0, top),
      behavior: immediate || reduceMotion ? "auto" : "smooth",
    });
    if (updateHistory) {
      const url = new URL(window.location.href);
      url.hash = id;
      history.pushState({ section: id }, "", url);
    }
    activeSection(id);
  };

  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[data-nav]");
    if (!link) return;
    const href = link.getAttribute("href") || "";
    if (!href.startsWith("#")) return;
    event.preventDefault();
    scrollToSection(href.slice(1));
    closeNav();
  });

  window.addEventListener("popstate", () => {
    const id = window.location.hash.replace("#", "") || "inicio";
    scrollToSection(id, false);
  });

  /* -------------------------------------------------------- reveal on scroll */
  const revealNodes = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.14, rootMargin: "0px 0px -40px 0px" }
    );
    revealNodes.forEach((node) => revealObserver.observe(node));
  } else {
    revealNodes.forEach((node) => node.classList.add("is-visible"));
  }

  /* ------------------------------------------------- section tracking/active */
  const trackedSections = new Set();
  const sections = document.querySelectorAll("main section[id]");
  if ("IntersectionObserver" in window && sections.length) {
    const sectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          activeSection(entry.target.id);
          if (!trackedSections.has(entry.target.id)) {
            trackedSections.add(entry.target.id);
            post("/api/event", { name: "section_view", meta: entry.target.id });
          }
        });
      },
      { threshold: 0.4, rootMargin: "-15% 0px -35% 0px" }
    );
    sections.forEach((section) => sectionObserver.observe(section));
  }

  /* --------------------------------------------------------------- analytics */
  const initialHit = () =>
    post("/api/hit", {
      path: window.location.pathname,
      lang: currentLang,
      referrer: document.referrer || "",
    });

  if (document.visibilityState === "visible") {
    initialHit();
  } else {
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "visible") initialHit();
    }, { once: true });
  }

  document.addEventListener("click", (event) => {
    const waLink = event.target.closest("a[data-wa]");
    if (waLink) {
      const section = waLink.closest("section[id]");
      post("/api/event", {
        name: "whatsapp_click",
        meta: section ? section.id : "global",
      });
    }
    const projectLink = event.target.closest("[data-project-click]");
    if (projectLink) {
      post("/api/event", {
        name: "project_click",
        meta: projectLink.dataset.projectClick || "",
      });
    }
  });

  /* ---------------------------------------------------------------- language */
  const buildWhatsApp = (content) => {
    const digits = String(content["contact.whatsapp_number"] || "").replace(/\D/g, "");
    if (!digits) return "#contacto";
    const message = content["contact.whatsapp_message"] || "";
    return `https://wa.me/${digits}${message ? `?text=${encodeURIComponent(message)}` : ""}`;
  };

  const applyLanguage = (lang, content, projects) => {
    currentLang = lang;
    html.lang = lang;
    body.dataset.lang = lang;

    document.querySelectorAll("[data-i18n]").forEach((node) => {
      const key = node.dataset.i18n;
      if (key && typeof content[key] === "string" && content[key] !== "") {
        node.textContent = content[key];
      }
    });

    if (content["meta.title"]) document.title = content["meta.title"];
    setMeta("description", content["meta.description"]);
    setMeta("keywords", content["meta.keywords"]);
    setMeta("og:title", content["meta.title"], "property");
    setMeta("og:description", content["meta.description"], "property");
    setMeta("twitter:title", content["meta.title"]);
    setMeta("twitter:description", content["meta.description"]);
    if (content["meta.og_image"]) {
      const ogImage = `${window.location.origin}${content["meta.og_image"]}`;
      setMeta("og:image", ogImage, "property");
      setMeta("twitter:image", ogImage);
    }

    if (langLabel) langLabel.textContent = content["ui.lang_switch"] || lang.toUpperCase();
    if (langButton) langButton.setAttribute("aria-label", content["ui.lang_switch"] || "Cambiar idioma");
    if (navToggle && content["ui.menu"]) navToggle.setAttribute("aria-label", content["ui.menu"]);

    const waHref = buildWhatsApp(content);
    document.querySelectorAll("a[data-wa]").forEach((link) => {
      link.setAttribute("href", waHref);
    });
    body.dataset.waNumber = String(content["contact.whatsapp_number"] || "");
    body.dataset.waMessage = String(content["contact.whatsapp_message"] || "");

    (projects || []).forEach((project) => {
      const title = document.querySelector(`[data-project-title="${project.id}"]`);
      if (title && project.title) title.textContent = project.title;
      const text = document.querySelector(`[data-project-text="${project.id}"]`);
      if (text && project.description) text.textContent = project.description;
      const linkLabel = document.querySelector(`[data-project-link="${project.id}"] span`);
      if (linkLabel && content["projects.link_label"]) {
        linkLabel.textContent = content["projects.link_label"];
      }
    });

    const url = new URL(window.location.href);
    if (lang === "es") {
      url.searchParams.delete("lang");
    } else {
      url.searchParams.set("lang", lang);
    }
    history.replaceState(history.state, "", url);

    document.cookie = `td_lang=${lang}; path=/; max-age=31536000; samesite=lax`;
    localStorage.setItem("techdev-lang", lang);
    showToast(lang === "es" ? "Idioma: Español" : "Language: English");
  };

  langButton?.addEventListener("click", async () => {
    const next = currentLang === "es" ? "en" : "es";
    langButton.disabled = true;
    try {
      const response = await fetch(`/api/content?lang=${next}`, {
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      if (!response.ok) throw new Error("No se pudo cambiar el idioma");
      const data = await response.json();
      applyLanguage(data.lang || next, data.content || {}, data.projects || []);
    } catch {
      window.location.href = `/?lang=${next}`;
    } finally {
      langButton.disabled = false;
    }
  });
})();

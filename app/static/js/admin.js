/* ============================================================================
   TechDev · Panel de administración
   ========================================================================== */
(() => {
  "use strict";

  const dataNode = document.getElementById("admin-data");
  if (!dataNode) return;

  const bootstrap = JSON.parse(dataNode.textContent || "{}");
  const sections = bootstrap.sections || [];
  let contentState = bootstrap.content || {};
  let projectsState = bootstrap.projects || [];
  let statsState = bootstrap.stats || {};

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const numberFormat = new Intl.NumberFormat("es-MX");
  const SECTION_NAMES = {
    inicio: "Inicio",
    servicios: "Servicios",
    proyectos: "Proyectos",
    nosotros: "Nosotros",
    contacto: "Contacto",
  };
  const LANG_NAMES = { es: "Español", en: "Inglés" };
  const DEVICE_NAMES = { desktop: "Escritorio", mobile: "Móvil / tablet" };

  const escapeHtml = (value) =>
    String(value ?? "").replace(/[&<>"']/g, (char) => {
      const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
      return map[char];
    });

  const toastNode = $("#admin-toast");
  let toastTimer = null;
  const toast = (message, isError = false) => {
    if (!toastNode) return;
    toastNode.textContent = message;
    toastNode.classList.toggle("is-error", Boolean(isError));
    toastNode.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastNode.classList.remove("is-visible"), 3200);
  };

  async function api(url, { method = "GET", body = null } = {}) {
    const options = {
      method,
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    };
    if (body !== null) {
      options.headers["Content-Type"] = "application/json";
      options.body = JSON.stringify(body);
    }
    const response = await fetch(url, options);
    if (response.status === 401) {
      window.location.href = "/admin/login";
      throw new Error("Sesión expirada");
    }
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "Ocurrió un error inesperado");
    return data;
  }

  async function uploadImage(file) {
    const form = new FormData();
    form.append("file", file);
    const response = await fetch("/admin/api/upload", {
      method: "POST",
      body: form,
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "No se pudo subir la imagen");
    return data.url;
  }

  /* ------------------------------------------------------------------- tabs */
  const tabs = $$(".admin-tab");
  const switchTab = (name) => {
    tabs.forEach((tab) => {
      const active = tab.dataset.tab === name;
      tab.classList.toggle("is-active", active);
      tab.setAttribute("aria-selected", String(active));
    });
    $$(".admin-panel").forEach((panel) => {
      const active = panel.id === `panel-${name}`;
      panel.classList.toggle("is-active", active);
      panel.hidden = !active;
    });
  };
  tabs.forEach((tab) => tab.addEventListener("click", () => switchTab(tab.dataset.tab)));

  /* ------------------------------------------------------------------ stats */
  function meterList(items, labelFn) {
    if (!items || !items.length) return '<li class="empty-note">Sin datos todavía.</li>';
    const max = Math.max(...items.map((item) => item.value || 0), 1);
    return items
      .map((item) => {
        const percent = Math.round(((item.value || 0) / max) * 100);
        return `<li><span title="${escapeHtml(labelFn(item))}">${escapeHtml(labelFn(item))}</span>
          <span class="meter"><i style="width:${percent}%"></i></span>
          <b>${numberFormat.format(item.value || 0)}</b></li>`;
      })
      .join("");
  }

  function renderStats(stats) {
    statsState = stats;
    const totals = stats.totals || {};
    const cards = [
      { label: "Visitas totales", value: totals.pageviews, hint: `${totals.avg_views_per_visitor ?? 0} vistas por visitante` },
      { label: "Visitantes únicos", value: totals.unique_visitors, hint: "sin duplicados por cookie" },
      { label: "Visitas hoy", value: totals.views_today, hint: `${totals.visitors_today ?? 0} visitantes nuevos` },
      { label: "Últimos 7 días", value: totals.views_7d, hint: `${totals.visitors_7d ?? 0} visitantes nuevos` },
      { label: "Últimos 30 días", value: totals.views_30d, hint: `${totals.visitors_30d ?? 0} visitantes nuevos` },
      { label: "Clics en WhatsApp", value: totals.whatsapp_clicks, hint: "desde toda la landing" },
      { label: "Proyectos", value: totals.projects, hint: `${totals.projects_visible ?? 0} visibles` },
      { label: "Campos editables", value: totals.editable_fields, hint: "textos e imágenes" },
    ];
    const cardsNode = $("#stats-cards");
    if (cardsNode) {
      cardsNode.innerHTML = cards
        .map(
          (card) => `<article class="stat-tile">
            <p class="stat-tile__label">${escapeHtml(card.label)}</p>
            <p class="stat-tile__value">${numberFormat.format(card.value || 0)}</p>
            <p class="stat-tile__hint">${escapeHtml(card.hint)}</p>
          </article>`
        )
        .join("");
    }

    const chartNode = $("#stats-chart");
    if (chartNode) {
      const daily = stats.daily || [];
      const peak = Math.max(stats.daily_peak || 0, 1);
      chartNode.innerHTML = daily
        .map((day) => {
          const percent = Math.max(2, Math.round(((day.views || 0) / peak) * 100));
          return `<div class="bar-col">
            <div class="bar" style="height:${percent}%" title="${escapeHtml(day.date)} · ${day.views} visitas · ${day.visitors} nuevos"></div>
            <span>${escapeHtml(day.label)}</span>
          </div>`;
        })
        .join("");
    }

    const sectionItems = Object.entries(stats.sections || {}).map(([key, value]) => ({
      key,
      value,
    }));
    const sectionsNode = $("#stats-sections");
    if (sectionsNode) {
      sectionsNode.innerHTML = meterList(sectionItems, (item) => SECTION_NAMES[item.key] || item.key);
    }

    const referrerItems = (stats.referrers || []).map((item) => ({
      key: item.source,
      value: item.total,
    }));
    const referrersNode = $("#stats-referrers");
    if (referrersNode) {
      referrersNode.innerHTML = meterList(referrerItems, (item) => item.key || "directo");
    }

    const languagesNode = $("#stats-languages");
    if (languagesNode) {
      languagesNode.innerHTML = meterList(
        (stats.languages || []).map((item) => ({ key: item.lang, value: item.total })),
        (item) => LANG_NAMES[item.key] || item.key
      );
    }

    const devicesNode = $("#stats-devices");
    if (devicesNode) {
      devicesNode.innerHTML = meterList(
        (stats.devices || []).map((item) => ({ key: item.device, value: item.total })),
        (item) => DEVICE_NAMES[item.key] || item.key
      );
    }

    const recentNode = $("#stats-recent");
    if (recentNode) {
      const recent = stats.recent || [];
      recentNode.innerHTML = recent.length
        ? recent
            .map(
              (row) => `<tr>
                <td>${escapeHtml(row.visitor)}</td>
                <td>${escapeHtml(row.path)}</td>
                <td>${escapeHtml(LANG_NAMES[row.lang] || row.lang || "—")}</td>
                <td>${escapeHtml(row.when)}</td>
              </tr>`
            )
            .join("")
        : '<tr><td colspan="4" class="empty-note">Todavía no hay visitas registradas.</td></tr>';
    }

    const updatedNode = $("#stats-updated");
    if (updatedNode) updatedNode.textContent = `Actualizado: ${stats.generated_at || "—"}`;
  }

  $("#stats-refresh")?.addEventListener("click", async (event) => {
    const button = event.currentTarget;
    button.disabled = true;
    button.textContent = "Actualizando…";
    try {
      const stats = await api("/admin/api/stats?days=14");
      renderStats(stats);
      toast("Estadísticas actualizadas");
    } catch (error) {
      toast(error.message, true);
    } finally {
      button.disabled = false;
      button.textContent = "Actualizar datos";
    }
  });

  /* ---------------------------------------------------------------- content */
  const contentNode = $("#content-sections");
  const dirtyNode = $("#content-dirty");
  let dirty = false;

  const setDirty = (value) => {
    dirty = value;
    if (dirtyNode) dirtyNode.hidden = !value;
  };

  const previewMarkup = (url) =>
    url
      ? `<img src="${escapeHtml(url)}" alt="Vista previa">`
      : "<span>Sin imagen</span>";

  const fieldMarkup = (key, label, type) => {
    const values = contentState[key] || { es: "", en: "" };
    const es = values.es || "";
    const en = values.en || "";

    if (type === "image") {
      return `<div class="field field--full">
        <span class="field__label">${escapeHtml(label)}</span>
        <div class="image-field">
          <div class="image-field__preview" data-preview="${escapeHtml(key)}">${previewMarkup(es)}</div>
          <div class="image-field__controls">
            <input class="admin-input" type="text" data-content-key="${escapeHtml(key)}" data-content-lang="es"
                   value="${escapeHtml(es)}" placeholder="/static/img/hero.jpg">
            <label class="admin-btn admin-btn--ghost admin-btn--small">
              Subir imagen
              <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" data-upload="${escapeHtml(key)}" hidden>
            </label>
            <small class="field__hint">JPG, PNG, WEBP o GIF · se usa en ambos idiomas · máx. 5 MB</small>
          </div>
        </div>
      </div>`;
    }

    const input = (lang, value) =>
      type === "textarea"
        ? `<textarea class="admin-input" rows="3" data-content-key="${escapeHtml(key)}" data-content-lang="${lang}">${escapeHtml(value)}</textarea>`
        : `<input class="admin-input" type="text" data-content-key="${escapeHtml(key)}" data-content-lang="${lang}" value="${escapeHtml(value)}">`;

    return `<div class="field">
      <span class="field__label">${escapeHtml(label)}</span>
      <div class="field__langs">
        <div class="field__lang"><span>ES</span>${input("es", es)}</div>
        <div class="field__lang"><span>EN</span>${input("en", en)}</div>
      </div>
    </div>`;
  };

  function renderContent() {
    if (!contentNode) return;
    const openTitles = new Set(
      $$("details[open]", contentNode).map((node) => node.dataset.section)
    );
    contentNode.innerHTML = sections
      .map(
        (section, index) => `<details class="content-section admin-card" data-section="${escapeHtml(section.id)}" ${index === 0 || openTitles.has(section.id) ? "open" : ""}>
          <summary>
            <span class="content-section__title">${escapeHtml(section.title)}</span>
            <span class="content-section__hint">${escapeHtml(section.description || "")}</span>
          </summary>
          <div class="field-grid">
            ${section.fields.map(([key, label, type]) => fieldMarkup(key, label, type)).join("")}
          </div>
        </details>`
      )
      .join("");
  }

  const updatePreview = (key, url) => {
    const node = contentNode?.querySelector(`[data-preview="${CSS.escape(key)}"]`);
    if (node) node.innerHTML = previewMarkup(url);
  };

  contentNode?.addEventListener("input", (event) => {
    const input = event.target.closest("[data-content-key]");
    if (input && contentState[input.dataset.contentKey] !== undefined) {
      contentState[input.dataset.contentKey][input.dataset.contentLang] = input.value;
    }
    if (input && !input.dataset.contentLang) return;
    setDirty(true);
    if (input?.dataset.contentLang === "es") {
      const key = input.dataset.contentKey;
      const type = sections
        .flatMap((section) => section.fields)
        .find(([fieldKey]) => fieldKey === key)?.[2];
      if (type === "image") updatePreview(key, input.value.trim());
    }
  });

  contentNode?.addEventListener("change", async (event) => {
    const upload = event.target.closest("[data-upload]");
    const file = upload?.files?.[0];
    if (!upload || !file) return;
    try {
      upload.disabled = true;
      toast("Subiendo imagen…");
      const url = await uploadImage(file);
      const key = upload.dataset.upload;
      const input = contentNode.querySelector(
        `input[data-content-key="${CSS.escape(key)}"][data-content-lang="es"]`
      );
      if (input) input.value = url;
      if (contentState[key]) {
        contentState[key].es = url;
        contentState[key].en = url;
      }
      updatePreview(key, url);
      setDirty(true);
      toast("Imagen subida correctamente");
    } catch (error) {
      toast(error.message, true);
    } finally {
      upload.disabled = false;
      upload.value = "";
    }
  });

  $("#content-save")?.addEventListener("click", async (event) => {
    const button = event.currentTarget;
    const payload = {};
    $$("[data-content-key]", contentNode).forEach((input) => {
      const key = input.dataset.contentKey;
      const lang = input.dataset.contentLang;
      if (!key || !lang) return;
      payload[key] = payload[key] || { es: "", en: "" };
      payload[key][lang] = input.value;
    });

    sections.forEach((section) => {
      section.fields.forEach(([key, , type]) => {
        if (type === "image" && payload[key]) payload[key].en = payload[key].es;
      });
    });

    button.disabled = true;
    button.textContent = "Guardando…";
    try {
      const result = await api("/admin/api/content", { method: "PUT", body: payload });
      setDirty(false);
      renderContent();
      toast(`${result.updated || 0} campos guardados`);
    } catch (error) {
      toast(error.message, true);
    } finally {
      button.disabled = false;
      button.textContent = "Guardar cambios";
    }
  });

  window.addEventListener("beforeunload", (event) => {
    if (!dirty) return;
    event.preventDefault();
    event.returnValue = "";
  });

  /* --------------------------------------------------------------- projects */
  const projectForm = $("#project-form");
  const projectList = $("#project-list");
  const projectImagePreview = $("#project-image-preview");
  const projectFormTitle = $("#project-form-title");
  const projectFormStatus = $("#project-form-status");

  const projectFields = projectForm ? $$("[data-field]", projectForm) : [];

  const updateProjectPreview = (url) => {
    if (!projectImagePreview) return;
    projectImagePreview.innerHTML = url
      ? `<img src="${escapeHtml(url)}" alt="Vista previa del proyecto">`
      : "<span>Sin imagen</span>";
  };

  function renderProjects() {
    if (!projectList) return;
    if (!projectsState.length) {
      projectList.innerHTML =
        '<p class="empty-note admin-card" style="padding:24px">Todavía no hay proyectos. Crea el primero con el botón “Nuevo proyecto”.</p>';
      return;
    }
    projectList.innerHTML = projectsState
      .map((project) => {
        const initials = (project.title_es || "?").slice(0, 2);
        const thumb = project.image_url
          ? `<img src="${escapeHtml(project.image_url)}" alt="">`
          : escapeHtml(initials);
        return `<article class="project-row admin-card">
          <div class="project-row__thumb">${thumb}</div>
          <div class="project-row__info">
            <strong>${escapeHtml(project.title_es || "Sin título")}</strong>
            <p>${escapeHtml(project.description_es || "")}</p>
            <small>
              ${escapeHtml(project.tags_raw || "sin tecnologías")} · orden ${Number(project.sort_order) || 0}
              <span class="status-pill ${project.visible ? "status-pill--on" : "status-pill--off"}">
                ${project.visible ? "Visible" : "Oculto"}
              </span>
            </small>
          </div>
          <div class="project-row__actions">
            <button class="admin-btn admin-btn--ghost admin-btn--small" type="button" data-edit="${project.id}">Editar</button>
            <button class="admin-btn admin-btn--danger admin-btn--small" type="button" data-delete="${project.id}">Eliminar</button>
          </div>
        </article>`;
      })
      .join("");
  }

  const openProjectEditor = (project = null) => {
    if (!projectForm) return;
    projectForm.hidden = false;
    projectForm.dataset.id = project ? String(project.id) : "";
    if (projectFormTitle) {
      projectFormTitle.textContent = project ? `Editar: ${project.title_es}` : "Nuevo proyecto";
    }
    if (projectFormStatus) projectFormStatus.textContent = "";

    projectFields.forEach((field) => {
      const name = field.dataset.field;
      if (field.type === "checkbox") {
        field.checked = project ? Boolean(project.visible) : true;
        return;
      }
      if (name === "sort_order" && !project) {
        field.value = String(projectsState.length + 1);
        return;
      }
      field.value = project ? project[name] ?? "" : "";
    });

    updateProjectPreview(project?.image_url || "");
    projectForm.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  $("#project-new")?.addEventListener("click", () => openProjectEditor(null));

  $("#project-cancel")?.addEventListener("click", () => {
    if (projectForm) projectForm.hidden = true;
  });

  projectList?.addEventListener("click", async (event) => {
    const editButton = event.target.closest("[data-edit]");
    if (editButton) {
      const project = projectsState.find((item) => String(item.id) === editButton.dataset.edit);
      if (project) openProjectEditor(project);
      return;
    }
    const deleteButton = event.target.closest("[data-delete]");
    if (deleteButton) {
      const project = projectsState.find((item) => String(item.id) === deleteButton.dataset.delete);
      if (!project) return;
      if (!window.confirm(`¿Eliminar el proyecto “${project.title_es}”?`)) return;
      try {
        await api(`/admin/api/projects/${project.id}`, { method: "DELETE" });
        toast("Proyecto eliminado");
        await loadProjects();
      } catch (error) {
        toast(error.message, true);
      }
    }
  });

  $("#project-image-upload")?.addEventListener("change", async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const input = $("#p-image");
    try {
      event.target.disabled = true;
      toast("Subiendo imagen…");
      const url = await uploadImage(file);
      if (input) input.value = url;
      updateProjectPreview(url);
      toast("Imagen subida correctamente");
    } catch (error) {
      toast(error.message, true);
    } finally {
      event.target.disabled = false;
      event.target.value = "";
    }
  });

  $("#p-image")?.addEventListener("input", (event) => {
    updateProjectPreview(event.target.value.trim());
  });

  projectForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = {};
    projectFields.forEach((field) => {
      const name = field.dataset.field;
      if (field.type === "checkbox") {
        data[name] = field.checked;
      } else {
        data[name] = field.value;
      }
    });
    data.sort_order = Number(data.sort_order || 0);

    const id = projectForm.dataset.id;
    const button = $("#project-save");
    if (button) {
      button.disabled = true;
      button.textContent = "Guardando…";
    }
    try {
      await api(id ? `/admin/api/projects/${id}` : "/admin/api/projects", {
        method: id ? "PUT" : "POST",
        body: data,
      });
      toast(id ? "Proyecto actualizado" : "Proyecto creado");
      projectForm.hidden = true;
      await loadProjects();
    } catch (error) {
      toast(error.message, true);
      if (projectFormStatus) projectFormStatus.textContent = error.message;
    } finally {
      if (button) {
        button.disabled = false;
        button.textContent = "Guardar proyecto";
      }
    }
  });

  async function loadProjects() {
    try {
      const data = await api("/admin/api/projects");
      projectsState = data.projects || [];
      renderProjects();
    } catch (error) {
      toast(error.message, true);
    }
  }

  /* --------------------------------------------------------------- start up */
  renderStats(statsState);
  renderContent();
  renderProjects();
})();

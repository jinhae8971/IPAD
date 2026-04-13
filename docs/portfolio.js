/* ============================================================
   jinhae8971 — Portfolio Script (vanilla JS)
   Loads data/projects.json and renders domains/projects/stack.
   ============================================================ */

(function () {
  const state = {
    data: null,
    filter: "all",
    featuredOnly: false,
  };

  // Footer year
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Load data
  fetch("data/projects.json", { cache: "no-store" })
    .then((r) => r.json())
    .then((data) => {
      state.data = data;
      renderDomains();
      renderProjects();
      renderStack();
      bindFilters();
      animateCounters();
      setupReveal();
    })
    .catch((err) => {
      console.error("Failed to load projects.json", err);
      const grid = document.getElementById("project-grid");
      if (grid) {
        grid.innerHTML =
          '<p style="color:#a0a8bd">프로젝트 데이터를 불러오지 못했습니다. <code>data/projects.json</code>을 확인해 주세요.</p>';
      }
    });

  // --- Render domains ---
  function renderDomains() {
    const container = document.getElementById("domain-grid");
    if (!container || !state.data) return;
    const { domains, projects } = state.data;

    container.innerHTML = domains
      .map((d) => {
        const count = projects.filter((p) => p.domain === d.id).length;
        return `
          <article class="domain-card reveal" data-domain="${d.id}" style="--domain-accent:${d.accent}">
            <span class="domain-icon">${d.icon}</span>
            <h3 class="domain-label">${escapeHtml(d.label)}</h3>
            <p class="domain-desc">${escapeHtml(d.description)}</p>
            <span class="domain-count">${count} project${count === 1 ? "" : "s"}</span>
          </article>
        `;
      })
      .join("");

    // Click to filter
    container.querySelectorAll(".domain-card").forEach((card) => {
      card.addEventListener("click", () => {
        const id = card.dataset.domain;
        const nextFilter = state.filter === id ? "all" : id;
        setFilter(nextFilter);
        // Smooth-scroll to projects section
        const target = document.getElementById("projects");
        if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    });
  }

  // --- Render projects ---
  function renderProjects() {
    const container = document.getElementById("project-grid");
    if (!container || !state.data) return;
    const { projects, domains } = state.data;
    const domainById = Object.fromEntries(domains.map((d) => [d.id, d]));

    container.innerHTML = projects
      .map((p) => {
        const d = domainById[p.domain] || {};
        const accent = d.accent || "#7c9cff";
        const tag = d.label || p.domain;
        const icon = d.icon || "▸";
        const live = p.live
          ? `<a class="project-link is-live" href="${escapeAttr(p.live)}">Live Demo →</a>`
          : "";
        const stackHtml = (p.stack || [])
          .map((s) => `<span>${escapeHtml(s)}</span>`)
          .join("");
        const highlightsHtml = (p.highlights || [])
          .map((h) => `<li>${escapeHtml(h)}</li>`)
          .join("");
        return `
          <article class="project-card reveal"
                   data-domain="${p.domain}"
                   data-featured="${p.featured ? "1" : "0"}"
                   style="--domain-accent:${accent}">
            <div class="project-head">
              <h3 class="project-title">${escapeHtml(p.title)}</h3>
              ${p.featured ? '<span class="project-star" title="Featured">★</span>' : ""}
            </div>
            <span class="project-domain-tag">${icon} ${escapeHtml(tag)}</span>
            <p class="project-tagline">${escapeHtml(p.tagline)}</p>
            ${highlightsHtml ? `<ul class="project-highlights">${highlightsHtml}</ul>` : ""}
            <div class="project-stack">${stackHtml}</div>
            <div class="project-actions">
              <a class="project-link" href="${escapeAttr(p.github)}" target="_blank" rel="noopener">GitHub ↗</a>
              ${live}
            </div>
          </article>
        `;
      })
      .join("");

    applyFilter();
  }

  // --- Render stack ---
  function renderStack() {
    const container = document.getElementById("stack-grid");
    if (!container || !state.data) return;
    container.innerHTML = state.data.stack
      .map(
        (s) => `
        <article class="stack-card reveal">
          <div class="stack-category">${escapeHtml(s.category)}</div>
          <div class="stack-items">
            ${s.items.map((i) => `<span>${escapeHtml(i)}</span>`).join("")}
          </div>
        </article>
      `,
      )
      .join("");
  }

  // --- Filter bar bindings ---
  function bindFilters() {
    const bar = document.getElementById("filter-bar");
    if (!bar) return;
    bar.querySelectorAll("[data-filter]").forEach((btn) => {
      btn.addEventListener("click", () => setFilter(btn.dataset.filter));
    });
    const toggle = bar.querySelector('[data-toggle="featured"]');
    if (toggle) {
      toggle.addEventListener("click", () => {
        state.featuredOnly = !state.featuredOnly;
        toggle.classList.toggle("is-active", state.featuredOnly);
        applyFilter();
      });
    }
  }

  function setFilter(id) {
    state.filter = id;
    const bar = document.getElementById("filter-bar");
    if (bar) {
      bar.querySelectorAll("[data-filter]").forEach((btn) => {
        btn.classList.toggle("is-active", btn.dataset.filter === id);
      });
    }
    const dGrid = document.getElementById("domain-grid");
    if (dGrid) {
      dGrid.querySelectorAll(".domain-card").forEach((card) => {
        card.classList.toggle("is-active", card.dataset.domain === id && id !== "all");
      });
    }
    applyFilter();
  }

  function applyFilter() {
    const grid = document.getElementById("project-grid");
    if (!grid) return;
    grid.querySelectorAll(".project-card").forEach((card) => {
      const domainMatch = state.filter === "all" || card.dataset.domain === state.filter;
      const featuredMatch = !state.featuredOnly || card.dataset.featured === "1";
      card.classList.toggle("is-hidden", !(domainMatch && featuredMatch));
    });
  }

  // --- Counter animation ---
  function animateCounters() {
    document.querySelectorAll("[data-counter]").forEach((el) => {
      const target = parseInt(el.dataset.counter, 10);
      if (isNaN(target)) return;
      const duration = 1200;
      const start = performance.now();
      function tick(now) {
        const progress = Math.min(1, (now - start) / duration);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(target * eased).toString();
        if (progress < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    });
  }

  // --- Reveal on scroll ---
  function setupReveal() {
    if (!("IntersectionObserver" in window)) {
      document.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-visible"));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" },
    );
    document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
  }

  // --- Helpers ---
  function escapeHtml(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }
  function escapeAttr(s) {
    return escapeHtml(s);
  }
})();

/**
 * CALCULATOR HUB APPLICATION CONTROLLER
 * Manages search, dark mode, dynamic calculator rendering, toast messages, and LocalStorage.
 */

document.addEventListener("DOMContentLoaded", () => {
  App.init();
});

const App = {
  init: function() {
    this.initTheme();
    this.initSearch();
    this.initMobileMenu();
    
    // Check if on universal calculator page
    if (document.getElementById("calculator-mount")) {
      this.initCalculatorView();
    }
    
    // Check if on category page
    if (document.getElementById("category-grid-mount")) {
      this.initCategoryView();
    }

    // Load recent & popular widgets if present
    this.renderRecentCalculators();
  },

  // Dark / Light Mode System
  initTheme: function() {
    const savedTheme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);
    this.updateThemeButtonIcon(savedTheme);

    const toggleBtn = document.getElementById("theme-toggle");
    if (toggleBtn) {
      toggleBtn.addEventListener("click", () => {
        const current = document.documentElement.getAttribute("data-theme");
        const next = current === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
        this.updateThemeButtonIcon(next);
        this.showToast(`Switched to ${next} theme`);
      });
    }
  },

  updateThemeButtonIcon: function(theme) {
    const toggleBtn = document.getElementById("theme-toggle");
    if (toggleBtn) {
      toggleBtn.innerHTML = theme === "dark" ? "☀️" : "🌙";
      toggleBtn.setAttribute("title", `Switch to ${theme === "dark" ? "light" : "dark"} mode`);
    }
  },

  // Mobile Menu Toggle
  initMobileMenu: function() {
    const mobileBtn = document.getElementById("mobile-menu-btn");
    const navMenu = document.getElementById("nav-menu");
    if (mobileBtn && navMenu) {
      mobileBtn.addEventListener("click", () => {
        navMenu.classList.toggle("active");
        if (navMenu.classList.contains("active")) {
          navMenu.style.display = "flex";
          navMenu.style.flexDirection = "column";
          navMenu.style.position = "absolute";
          navMenu.style.top = "4.25rem";
          navMenu.style.left = "0";
          navMenu.style.right = "0";
          navMenu.style.background = "var(--bg-card)";
          navMenu.style.padding = "1rem";
          navMenu.style.boxShadow = "var(--shadow-lg)";
        } else {
          navMenu.style.display = "";
        }
      });
    }
  },

  // Instant Search Engine
  initSearch: function() {
    const searchInputs = document.querySelectorAll(".search-input");
    searchInputs.forEach(input => {
      const container = input.closest(".search-container");
      if (!container) return;
      const dropdown = container.querySelector(".search-results-dropdown");
      if (!dropdown) return;

      input.addEventListener("input", (e) => {
        const query = e.target.value;
        const results = searchCalculators(query);
        if (results.length > 0 && query.trim() !== "") {
          dropdown.innerHTML = results.map(item => `
            <a href="/calculator.html?id=${item.id}" class="search-result-item" onclick="App.trackRecent('${item.id}')">
              <div>
                <div class="search-result-title">${item.title}</div>
                <div style="font-size:0.8rem; color:var(--text-secondary);">${item.subtitle}</div>
              </div>
              <span class="search-result-badge">${item.category}</span>
            </a>
          `).join("");
          dropdown.classList.add("active");
        } else {
          dropdown.classList.remove("active");
        }
      });

      document.addEventListener("click", (e) => {
        if (!container.contains(e.target)) {
          dropdown.classList.remove("active");
        }
      });
    });
  },

  // Toast Notification System
  showToast: function(message) {
    let container = document.querySelector(".toast-container");
    if (!container) {
      container = document.createElement("div");
      container.className = "toast-container";
      document.body.appendChild(container);
    }
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transition = "opacity 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  },

  // Local Storage Tracking
  trackRecent: function(calcId) {
    let recent = JSON.parse(localStorage.getItem("calc_recent") || "[]");
    recent = recent.filter(id => id !== calcId);
    recent.unshift(calcId);
    if (recent.length > 6) recent.pop();
    localStorage.setItem("calc_recent", JSON.stringify(recent));
  },

  renderRecentCalculators: function() {
    const mount = document.getElementById("recent-calculators-mount");
    if (!mount) return;
    const recentIds = JSON.parse(localStorage.getItem("calc_recent") || "[]");
    if (recentIds.length === 0) {
      mount.innerHTML = `<li style="font-size:0.85rem; color:var(--text-muted);">No recently used calculators yet.</li>`;
      return;
    }

    const items = recentIds.map(id => getCalculatorById(id)).filter(Boolean);
    mount.innerHTML = items.map(item => `
      <li>
        <a href="/calculator.html?id=${item.id}" class="recent-item-link">
          <span>${item.title}</span>
          <span style="font-size:0.75rem; color:var(--text-muted);">${item.category}</span>
        </a>
      </li>
    `).join("");
  },

  // Dynamic Calculator Page Render
  initCalculatorView: function() {
    const params = new URLSearchParams(window.location.search);
    const calcId = params.get("id") || "bmi-calculator";
    const calc = getCalculatorById(calcId);
    if (!calc) {
      document.getElementById("calculator-mount").innerHTML = `
        <div class="calculator-card" style="text-align:center; padding:3rem;">
          <h2>Calculator Not Found</h2>
          <p style="margin-top:1rem;">The requested calculator '${calcId}' could not be located.</p>
          <a href="/index.html" class="btn btn-primary" style="margin-top:1.5rem;">Return to Homepage</a>
        </div>
      `;
      return;
    }

    // Track usage
    this.trackRecent(calc.id);

    // Update document SEO meta tags dynamically
    document.title = calc.metaTitle || `${calc.title} - Calculator Hub`;
    let metaDesc = document.querySelector('meta[name="description"]');
    if (!metaDesc) {
      metaDesc = document.createElement("meta");
      metaDesc.name = "description";
      document.head.appendChild(metaDesc);
    }
    metaDesc.content = calc.metaDesc || calc.subtitle;

    // Render Calculator UI Card
    const mount = document.getElementById("calculator-mount");
    mount.innerHTML = `
      <div class="calculator-card">
        <div class="calculator-header">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <h1 class="calculator-title">${calc.title}</h1>
            <span class="calculator-tag">${calc.category.toUpperCase()}</span>
          </div>
          <p class="calculator-subtitle">${calc.subtitle}</p>
        </div>

        <form id="calc-form" novalidate onsubmit="event.preventDefault(); App.runCalculation('${calc.id}');">
          ${calc.inputs.map(inp => this.renderInputField(inp)).join("")}

          <div class="btn-group">
            <button type="submit" class="btn btn-primary">⚡ Calculate</button>
            <button type="button" class="btn btn-secondary" onclick="App.resetForm()">🔄 Reset</button>
          </div>
        </form>

        <div id="result-mount"></div>
      </div>

      <!-- SEO Article & Guide Section -->
      <article class="seo-article">
        <h2>About ${calc.title}</h2>
        <p>${calc.intro}</p>

        <h2>Calculation Formula</h2>
        <div class="formula-card">${calc.formula}</div>

        <h2>How to Use This Calculator</h2>
        <ol style="margin-left:1.5rem; color:var(--text-secondary); line-height:1.8;">
          ${calc.howTo.map(step => `<li>${step}</li>`).join("")}
        </ol>

        <h2 style="margin-top:2rem;">Frequently Asked Questions (FAQ)</h2>
        <div class="faq-container">
          ${calc.faqs.map(faq => `
            <div class="faq-item">
              <div class="faq-question" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
                <span>Q: ${faq.q}</span>
                <span>▼</span>
              </div>
              <div class="faq-answer" style="display:block;">
                A: ${faq.a}
              </div>
            </div>
          `).join("")}
        </div>
      </article>
    `;

    // Automatically trigger initial calculation with defaults
    this.runCalculation(calc.id);
  },

  renderInputField: function(inp) {
    if (inp.type === "select") {
      return `
        <div class="form-group">
          <label class="form-label" for="${inp.id}">${inp.label}</label>
          <select id="${inp.id}" class="form-control">
            ${inp.options.map(opt => `<option value="${opt}" ${opt === inp.default ? 'selected' : ''}>${opt}</option>`).join("")}
          </select>
        </div>
      `;
    } else if (inp.type === "textarea") {
      return `
        <div class="form-group">
          <label class="form-label" for="${inp.id}">${inp.label}</label>
          <textarea id="${inp.id}" class="form-control" rows="4">${inp.default || ""}</textarea>
        </div>
      `;
    } else {
      const isNum = inp.type === "number";
      const inputType = isNum ? 'type="text" inputmode="decimal" autocomplete="off"' : `type="${inp.type}"`;
      return `
        <div class="form-group">
          <label class="form-label" for="${inp.id}">${inp.label}</label>
          <input ${inputType} id="${inp.id}" class="form-control" value="${inp.default !== undefined ? inp.default : ''}" placeholder="${inp.label}" />
        </div>
      `;
    }
  },

  runCalculation: function(calcId) {
    const calc = getCalculatorById(calcId);
    if (!calc) return;

    const inputVals = {};
    calc.inputs.forEach(inp => {
      const el = document.getElementById(inp.id);
      if (el) inputVals[inp.id] = el.value;
    });

    const res = CalculatorEngine.calculate(calcId, inputVals);
    const resMount = document.getElementById("result-mount");

    if (res.error) {
      resMount.innerHTML = `
        <div class="result-box" style="border-color:var(--danger); background:rgba(234,67,53,0.1);">
          <div class="result-title" style="color:var(--danger);">Error</div>
          <p style="color:var(--text-primary); font-weight:600;">${res.error}</p>
        </div>
      `;
    } else {
      resMount.innerHTML = `
        <div class="result-box">
          <div class="result-title">Calculation Result</div>
          <div class="result-value" id="final-result-value">${res.value}</div>
          <div class="result-explanation">${res.explanation}</div>

          <div class="result-actions">
            <button class="btn btn-secondary" onclick="App.copyResult()">📋 Copy Result</button>
            <button class="btn btn-outline" onclick="App.shareCalculator()">🔗 Share</button>
          </div>
        </div>
      `;
    }
  },

  resetForm: function() {
    const form = document.getElementById("calc-form");
    if (form) form.reset();
    document.getElementById("result-mount").innerHTML = "";
    this.showToast("Form reset to defaults.");
  },

  copyResult: function() {
    const valEl = document.getElementById("final-result-value");
    if (valEl) {
      navigator.clipboard.writeText(valEl.innerText).then(() => {
        this.showToast("Result copied to clipboard!");
      });
    }
  },

  shareCalculator: function() {
    if (navigator.share) {
      navigator.share({
        title: document.title,
        url: window.location.href
      }).catch(() => {});
    } else {
      navigator.clipboard.writeText(window.location.href).then(() => {
        this.showToast("Calculator link copied to clipboard!");
      });
    }
  },

  // Render Category Pages
  initCategoryView: function() {
    const mount = document.getElementById("category-grid-mount");
    if (!mount) return;
    const catId = mount.getAttribute("data-category");
    const calcs = getCalculatorsByCategory(catId);
    
    mount.innerHTML = calcs.map(item => `
      <a href="/calculator.html?id=${item.id}" class="calculator-item-card" onclick="App.trackRecent('${item.id}')">
        <div class="calculator-item-title">${item.title}</div>
        <div class="calculator-item-desc">${item.subtitle}</div>
        <div class="calculator-item-footer">
          <span class="calculator-tag">${item.category}</span>
          <span style="font-size:0.85rem; font-weight:600; color:var(--accent-primary);">Use Calculator →</span>
        </div>
      </a>
    `).join("");
  }
};

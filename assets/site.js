(function () {
  const key = "recolio-support-language";
  const root = document.documentElement;
  let buttons = [];

  function supportedLanguage(language) {
    if (typeof language !== "string") return null;
    const value = language.trim().toLowerCase().replace(/_/g, "-");
    if (value === "en" || value.startsWith("en-")) return "en";
    if (value === "zh" || value.startsWith("zh-")) return "zh";
    return null;
  }

  function updateInternalLinks(value) {
    document.querySelectorAll("a[href]").forEach((link) => {
      const href = link.getAttribute("href");
      if (!href || href.startsWith("#")) return;
      const url = new URL(href, window.location.href);
      const siteRoot = new URL("./", window.location.href).pathname;
      if (url.origin !== window.location.origin || !url.pathname.startsWith(siteRoot)
          || !url.pathname.endsWith(".html")) return;
      url.searchParams.set("lang", value);
      link.setAttribute("href", url.href);
    });
  }

  function chooseLanguage(language) {
    const value = supportedLanguage(language) || "en";
    root.dataset.language = value;
    root.lang = value === "zh" ? "zh-Hans" : "en";
    buttons.forEach((button) => {
      const selected = button.dataset.languageChoice === value;
      button.classList.toggle("active", selected);
      button.setAttribute("aria-pressed", String(selected));
    });
    updateInternalLinks(value);
    try { localStorage.setItem(key, value); } catch (_) {}
  }

  let stored;
  try { stored = localStorage.getItem(key); } catch (_) {}
  const requested = new URL(window.location.href).searchParams.get("lang");
  chooseLanguage(supportedLanguage(requested) || supportedLanguage(stored)
    || supportedLanguage(navigator.language) || "en");

  function bindControls() {
    buttons = Array.from(document.querySelectorAll("[data-language-choice]"));
    chooseLanguage(root.dataset.language);
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const value = supportedLanguage(button.dataset.languageChoice) || "en";
        chooseLanguage(value);
        const url = new URL(window.location.href);
        url.searchParams.set("lang", value);
        try { window.history.replaceState(null, "", url.href); } catch (_) {}
      });
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindControls, { once: true });
  } else {
    bindControls();
  }
})();


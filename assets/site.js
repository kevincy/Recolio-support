(function () {
  'use strict';
  const key = 'recolio-support-language';
  const root = document.documentElement;
  const languages = ['en', 'zh-Hans', 'ja', 'ko', 'es', 'zh-Hant'];
  function supportedLanguage(language) {
    if (typeof language !== 'string') return null;
    const value = language.trim().toLowerCase().replace(/_/g, '-');
    if (/^zh-(hant|tw|hk|mo)(-|$)/.test(value)) return 'zh-Hant';
    if (value === 'zh' || value.startsWith('zh-')) return 'zh-Hans';
    return languages.find(code => value === code.toLowerCase() || value.startsWith(code.toLowerCase() + '-')) || null;
  }
  function updateInternalLinks(value) {
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('#')) return;
      const url = new URL(href, window.location.href);
      const siteRoot = new URL('./', window.location.href).pathname;
      if (url.origin !== window.location.origin || !url.pathname.startsWith(siteRoot)
          || !url.pathname.endsWith('.html')) return;
      url.searchParams.set('lang', value);
      link.setAttribute('href', url.href);
    });
  }
  function chooseLanguage(language) {
    const value = supportedLanguage(language) || 'en';
    root.dataset.language = value;
    root.lang = value;
    updateInternalLinks(value);
    try { localStorage.setItem(key, value); } catch (_) {}
    const select = document.getElementById('language');
    if (select) select.value = value;
    const content = document.querySelector('main > [data-locale="' + value + '"]');
    if (content) {
      document.title = content.dataset.title;
      const meta = document.querySelector('meta[name="description"]');
      if (meta) meta.setAttribute('content', content.dataset.description);
      content.querySelectorAll('img[data-src]').forEach(img => {
        if (!img.getAttribute('src')) img.setAttribute('src', img.dataset.src);
      });
    }
  }
  let stored;
  try { stored = localStorage.getItem(key); } catch (_) {}
  const requested = new URL(window.location.href).searchParams.get('lang');
  const browser = (navigator.languages || [navigator.language]).map(supportedLanguage).find(Boolean);
  chooseLanguage(supportedLanguage(requested) || supportedLanguage(stored) || browser || 'en');
  function bindControls() {
    chooseLanguage(root.dataset.language);
    document.querySelectorAll('[data-gallery]').forEach(gallery => {
      const buttons = gallery.querySelectorAll('[data-gallery-src]');
      buttons.forEach(button => button.addEventListener('click', () => {
        const image = gallery.querySelector('img');
        image.src = button.dataset.gallerySrc;
        image.dataset.src = button.dataset.gallerySrc;
        image.alt = button.dataset.galleryAlt;
        gallery.querySelector('[data-gallery-caption]').textContent = button.dataset.galleryCopy;
        buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      }));
    });
    const select = document.getElementById('language');
    if (!select) return;
    select.addEventListener('change', () => {
      chooseLanguage(select.value);
      const url = new URL(window.location.href);
      url.searchParams.set('lang', root.dataset.language);
      try { window.history.replaceState(null, '', url.href); } catch (_) {}
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bindControls, { once: true });
  else bindControls();
})();

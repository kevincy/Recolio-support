const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const script = fs.readFileSync(path.join(__dirname, '../assets/site.js'), 'utf8');
let checks = 0;
function check(actual, expected) { assert.deepEqual(actual, expected); checks++; }
function page({ query = '', stored, browser = 'en-US', blockedStorage = false } = {}) {
  const root = { dataset: {} };
  const events = {};
  const buttons = ['en', 'zh'].map(value => ({
    dataset: { languageChoice: value },
    classList: { toggle(_, active) { this.active = active; } },
    setAttribute(key, value) { this[key] = value; },
    addEventListener(_, fn) { this.click = fn; }
  }));
  const links = ['privacy.html?ref=terms#data', 'guide.html', '#local',
    'https://www.apple.com/legal/', 'mailto:support@example.com',
    'https://kevincy.github.io/other/privacy.html'].map(href => ({
      href, getAttribute() { return this.href; }, setAttribute(_, value) { this.href = value; }
    }));
  const window = { location: new URL('https://kevincy.github.io/Recolio-support/terms.html' + query),
    history: { replaceState(_, __, href) { window.location = new URL(href); } } };
  const document = { documentElement: root, readyState: 'loading',
    querySelectorAll(selector) { return selector === 'a[href]' ? links : buttons; },
    addEventListener(name, fn) { events[name] = fn; } };
  const localStorage = {
    getItem() { if (blockedStorage) throw Error('Blocked'); return stored; },
    setItem(_, value) { if (blockedStorage) throw Error('Blocked'); stored = value; }
  };
  vm.runInNewContext(script, { document, window, localStorage, navigator: { language: browser }, URL });
  check(buttons[0].click, undefined); // Initial language is set before body/controls exist.
  events.DOMContentLoaded();
  return { root, buttons, links, window };
}
for (const query of ['?lang=en', '?lang=en-US', '?lang=EN_ca']) {
  const p = page({ query, stored: 'zh', browser: 'zh-CN' });
  check(p.root.dataset.language, 'en');
  check(p.root.lang, 'en');
  check(p.buttons[0]['aria-pressed'], 'true');
  check(p.links[0].href, 'https://kevincy.github.io/Recolio-support/privacy.html?ref=terms&lang=en#data');
}
check(page({ query: '?lang=zh-Hans', stored: 'en' }).root.lang, 'zh-Hans');
check(page({ query: '?lang=fr', stored: 'en', browser: 'zh-CN' }).root.lang, 'en');
check(page({ stored: 'invalid', browser: 'zh-CN' }).root.lang, 'zh-Hans');
check(page({ browser: 'fr-FR' }).root.lang, 'en');
check(page({ query: '?lang=en', browser: 'zh-CN', blockedStorage: true }).root.lang, 'en');
const p = page({ query: '?lang=en&ref=app#section', browser: 'zh-CN' });
p.buttons[1].click();
check(p.root.lang, 'zh-Hans');
check(p.window.location.href, 'https://kevincy.github.io/Recolio-support/terms.html?lang=zh&ref=app#section');
check(new URL(p.links[1].href).searchParams.get('lang'), 'zh');
check(p.links.slice(2).map(link => link.href), ['#local', 'https://www.apple.com/legal/',
  'mailto:support@example.com', 'https://kevincy.github.io/other/privacy.html']);
for (const name of ['index', 'privacy', 'terms', 'support', 'guide']) {
  const html = fs.readFileSync(path.join(__dirname, `../${name}.html`), 'utf8');
  check((html.match(/<script src="assets\/site.js[^\"]*"/g) || []).length, 1);
  check(html.indexOf('assets/site.js') < html.indexOf('</head>'), true);
}
console.log(`Support language checks: ${checks}/${checks} passed`);

# Recolio — product and support site

GitHub Pages: **https://kevincy.github.io/Recolio-support/**

A buildless-at-runtime product homepage with an interactive real-screenshot tour, three-step onboarding story, homepage FAQ and download call to action; with a user guide, troubleshooting, privacy policy and terms. Uses existing genuine app screenshots with original sample content; no fabricated app UI, analytics, third-party fonts or tracking scripts.

## Six complete languages

English (`en`), Simplified Chinese (`zh-Hans`), Japanese (`ja`), Korean (`ko`), Spanish (`es`) and Traditional Chinese (`zh-Hant`). The old `?lang=zh` and stored `zh` preference remain compatible with Simplified Chinese. Traditional Chinese is written for Taiwan with generally understandable wording for Hong Kong.

Explicit supported URL language wins over the saved website preference, then the first supported browser language, then English. `?lang=en` from the app continues to open English regardless of device language. Selection changes the current URL, page title, description, screenshots and same-site links; it persists without changing account or app settings. External links, unrelated sites, other query parameters and fragments are preserved.

Examples:

- `/index.html?lang=ja`
- `/guide.html?lang=ko`
- `/support.html?lang=es`
- `/privacy.html?lang=zh-Hant`
- `/terms.html?lang=en`

## Edit and validate

- `content/site.json`: canonical six-language product copy, navigation, guide and FAQ.
- `content/privacy.json`, `content/terms.json`: all six policy bodies. English/Chinese originals retained except the documented allowance/current-Pro clarification, folder terminology and consolidated contact block.
- `scripts/build.py`: renders all five HTML routes with static content and English fallback. No client-side translation service or runtime fetch.
- `assets/screenshots/manifest.json`: source paths/hashes and web-image hashes for 30 localized screenshot derivatives. UI content is unchanged; only image scaling/WebP encoding is applied.
- `assets/site.js`: shared language routing, image hydration and link preservation.

```sh
python3 scripts/build.py
python3 scripts/check_site.py
node tests/language.test.cjs
python3 -m http.server 8096 --bind 127.0.0.1
```

Optional real-browser regression: `node tests/browser.cjs` uses an isolated headless browser and requires Playwright plus Chrome. Set `PLAYWRIGHT_MODULE` and `BROWSER_EXECUTABLE` for another local installation. Screenshots/results go to `/tmp/recolio-support-review-20261030/`, not the public site. The test expects the local preview server on port 8096.

Pushes to `main` run build-freshness, coverage/link/image and routing checks before GitHub Pages deploys. The existing `main` deployment workflow remains the owner; no alternative host or framework is introduced.

## Product accuracy

iCloud sync is optional, off by default, requires Pro, the same Apple Account, iCloud permissions, storage and network access. It is not an independent backup. Preview does not affect study history; ratings do. Search finds recognized image text, not similar images or objects. Import compatibility varies. Free import exceptions and the 1,000-card study limit are described separately in the guide and terms.

Translations received AI editorial review; no human native-language approval or legal clearance is claimed. See `DELIVERY_20261030.md` for checks, sources and deployment evidence.

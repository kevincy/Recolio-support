# Recolio Support

Public support site for Recolio, including:

- Product and contact page
- Privacy Policy
- Support and troubleshooting
- User Guide
- Terms of Use

The site is plain static HTML/CSS/JavaScript and is ready for GitHub Pages.

## Public URLs

After GitHub Pages is enabled for the repository root:

- Home: `https://kevincy.github.io/Recolio-support/`
- Privacy: `https://kevincy.github.io/Recolio-support/privacy.html`
- Support: `https://kevincy.github.io/Recolio-support/support.html`
- User Guide: `https://kevincy.github.io/Recolio-support/guide.html`
- Terms: `https://kevincy.github.io/Recolio-support/terms.html`

## Local preview

Run any static HTTP server from this directory, for example:

```sh
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## Language routing

App links specify `?lang=en` or `?lang=zh`. A supported explicit language takes
priority over the saved website preference and browser language. The page sets
its language before rendering body content, and same-site HTML links retain it.
The language buttons update the current URL and saved preference. Invalid
parameters fall back to a valid saved preference, then browser language, then
English. External links and document fragments are not rewritten.

Run the dependency-free regression checks with `node tests/language.test.cjs`.


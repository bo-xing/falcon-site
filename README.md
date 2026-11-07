# iPerf Falcon website

Product, support, privacy, and terms pages for iPerf Falcon. Dependency-free static HTML, CSS and JavaScript, hosted with GitHub Pages.

- Website: https://bo-xing.github.io/falcon-site/
- Apple: https://apps.apple.com/app/id6780008195
- Android: https://play.google.com/store/apps/details?id=com.boxing.falcon

| Page | English | 简体中文 |
|---|---|---|
| Product | `index.html` | `index-zh.html` |
| Help center | `support.html` | `support-zh.html` |
| Privacy | `privacy.html` | `privacy-zh.html` |
| Terms | `terms.html` | `terms-zh.html` |

## Develop and preview

```bash
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765/ or http://127.0.0.1:8765/index-zh.html.

The root HTML files and `sitemap.xml` are committed build output, so GitHub Pages serves them without a build dependency. Edit shared layouts, product/help copy, metadata, and the update date in `scripts/build_site.py`. Edit legal body text in `content/`. Then regenerate and commit the outputs together. Edit appearance in `style.css` and progressive enhancements in `site.js`; appearance initialization is in `theme.js`. CSS and JavaScript URLs carry content hashes to avoid stale assets after deployment.

Before delivery:

```bash
python3 scripts/build_site.py --check
python3 scripts/check_site.py
python3 -m unittest discover -s scripts/tests -v
git diff --check
```

Browser QA should cover both languages at 320, 390, 768 and 1440 CSS pixels; mobile navigation; same-language links and preservation of the current anchor when switching languages; screenshot platform tabs (including arrow keys, Home and End); image preview and Escape/focus return; FAQ deep links; appearance persistence and browser theme colors; and email-copy success or failure. Without JavaScript, navigation, download links, all screenshot panels, legal text and native FAQ disclosures remain available.

## Assets

`assets/screenshots/` contains optimized JPEG copies of native screenshot fixtures from the Falcon app repository. `sources.json` records their repository-relative provenance. Measurements are illustrative demo data; screenshots can include Pro features and differ from a newer app version. When updating, copy reviewed native captures for both languages, keep the aspect ratio, and update the manifest. Do not fabricate performance results or credentials. Current exports have a maximum dimension of 1800 px.

`assets/social-card.png` is the local sharing preview. On macOS, regenerate it with `swift scripts/render_social_card.swift` from the repository root. No external fonts, analytics, image hosting or runtime libraries are required. The only persisted website preference is light/dark appearance in browser local storage, described in both privacy policies.

## Release maintenance

Review website copy against the app repository and publicly available store versions whenever user-visible behavior changes. Keep both languages aligned:

1. Verify supported platforms and download destinations.
2. Check free/Pro boundaries, store-specific restoration, and platform differences. Apple and Google Play purchases are independent; comparison currently supports up to 6 runs on Apple and 4 on Android.
3. Check network activity (including automatic target-list reachability probes), local storage, credentials, backup, exports, and store services.
4. Update legal dates and the generator's `UPDATED` value when the policy actually changes.
5. Check local routes plus store, platform-policy, refund, GitHub privacy and email links before publishing.

GitHub Pages publication is separate from local implementation. No Sites hosting registration is required. Keep product copy free of hard-coded release numbers; actual capabilities and prices follow the installed version and its store.

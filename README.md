# falcon-site

Public product, support, privacy, and terms pages for **iPerf Falcon**, hosted with GitHub Pages.

| Page | English (default) | 中文 |
|---|---|---|
| Product home | `index.html` | Bilingual summary on the same page |
| Support & FAQ | `support.html` | `support-zh.html` |
| Privacy Policy | `privacy.html` | `privacy-zh.html` |
| Terms of Use | `terms.html` | `terms-zh.html` |

Live site: https://bo-xing.github.io/falcon-site/

App Store product: https://apps.apple.com/app/id6780008195

## Release maintenance

When Falcon gains or changes a user-facing capability, review this site in the same release cycle:

1. Keep the free/Pro split in both support pages aligned with `docs/app-store-description.md` in the Falcon app repository.
2. Update network activity, local storage, credentials, StoreKit behavior, exports, and third-party services in both privacy pages.
3. Update purchase terms, supported platforms, public-server wording, and open-source components in both terms pages.
4. Revise each changed legal page’s date, plus `sitemap.xml` `lastmod` values.
5. Check every local link and the App Store, Apple legal, GitHub privacy, and email links before publishing.

The App Store listing and the app repository are the product source of truth; avoid hard-coding a release number on the home page so routine releases do not immediately make the site stale.

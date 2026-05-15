## 2025-02-20 - Preconnect to Google Fonts Domains
**Learning:** Establishing early connection (DNS, TCP, TLS) for external font domains is a quick and extremely effective way to improve First Contentful Paint (FCP) on static pages.
**Action:** When adding or utilizing Google Fonts, always ensure the corresponding `preconnect` tags are included in the `<head>` to minimize connection setup latency.

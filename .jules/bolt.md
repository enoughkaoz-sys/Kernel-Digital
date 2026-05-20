## 2024-05-20 - Caching Static DOM elements\n**Learning:** The application uses plain JavaScript in  where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.\n**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent layout recalculations.
## 2024-05-20 - Caching Static DOM elements
**Learning:** The application uses plain JavaScript in `index.html` where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.
**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent redundant lookups.
## 2024-05-20 - Preconnecting to External Resources
**Learning:** The application was loading Google Fonts synchronously without preconnecting to the font servers. The FCP benchmark demonstrated that the latency from DNS, TCP, and TLS handshakes to `fonts.googleapis.com` and `fonts.gstatic.com` directly delayed rendering.
**Action:** Add `<link rel="preconnect">` tags to the HTML `<head>` for critical third-party origins (like Google Fonts) to establish early connections, reducing DNS/TLS lookup latency and accelerating First Contentful Paint.

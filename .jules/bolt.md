## 2024-05-20 - Caching Static DOM elements\n**Learning:** The application uses plain JavaScript in  where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.\n**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent layout recalculations.
## 2024-05-20 - Caching Static DOM elements
**Learning:** The application uses plain JavaScript in `index.html` where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.
**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent redundant lookups.
## 2024-05-20 - Preconnecting Google Fonts
**Learning:** This codebase uses Google Fonts loaded externally. The default snippet from Google Fonts does not include the preconnect tags, meaning the browser waits until the CSS is parsed to even initiate the DNS/TCP/TLS handshake to the font origin.
**Action:** Always verify if external, render-blocking resources like fonts have appropriate `<link rel="preconnect">` tags to speed up First Contentful Paint (FCP).

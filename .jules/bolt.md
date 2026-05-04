## 2024-05-20 - Caching Static DOM elements\n**Learning:** The application uses plain JavaScript in  where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.\n**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent layout recalculations.
## 2024-05-20 - Caching Static DOM elements
**Learning:** The application uses plain JavaScript in `index.html` where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.
**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent redundant lookups.
## 2024-05-20 - Preconnecting Google Fonts
**Learning:** External fonts loading from Google Fonts without `preconnect` hints cause delays in the browser building the render tree, affecting the First Contentful Paint (FCP) of the application.
**Action:** Adding `<link rel="preconnect">` and `crossorigin` hints for `fonts.googleapis.com` and `fonts.gstatic.com` directly in `index.html` mitigates the connection latency during DNS lookup, TCP handshake, and TLS negotiation.

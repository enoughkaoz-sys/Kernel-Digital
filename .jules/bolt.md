## 2024-05-20 - Caching Static DOM elements\n**Learning:** The application uses plain JavaScript in  where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.\n**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent layout recalculations.
## 2024-05-20 - Caching Static DOM elements
**Learning:** The application uses plain JavaScript in `index.html` where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.
**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent redundant lookups.
## 2024-05-20 - Preconnecting to external fonts
**Learning:** Found that external fonts from Google Fonts were added to `index.html` without resource hints. This delays FCP because the browser discovers these required domains late in the rendering lifecycle.
**Action:** Always add `<link rel="preconnect">` for external resources, specifically `fonts.googleapis.com` and `fonts.gstatic.com` (with `crossorigin`) to kick-off DNS, TCP and TLS handshakes as early as possible.

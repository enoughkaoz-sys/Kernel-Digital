## 2024-05-20 - Caching Static DOM elements\n**Learning:** The application uses plain JavaScript in  where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.\n**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent layout recalculations.
## 2024-05-20 - Caching Static DOM elements
**Learning:** The application uses plain JavaScript in `index.html` where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.
**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent redundant lookups.
## 2024-05-20 - Font Loading Optimization
**Learning:** External font loading (Google Fonts) was blocking rendering without preconnects. Adding `<link rel="preconnect">` for the fonts origin is an immediate, low-risk way to improve FCP.
**Action:** Always verify if external resources loaded in `<head>` can benefit from `preconnect` or `dns-prefetch` to eliminate connection overhead.

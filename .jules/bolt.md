## 2024-05-20 - Caching Static DOM elements\n**Learning:** The application uses plain JavaScript in  where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.\n**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent layout recalculations.
## 2024-05-20 - Caching Static DOM elements
**Learning:** The application uses plain JavaScript in `index.html` where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.
**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent redundant lookups.
## 2024-05-21 - Google Fonts Preconnect
**Learning:** External fonts loading from google can block the rendering of the text until the DNS lookup, TLS connection, and the fetch finish.
**Action:** Always add `<link rel="preconnect" href="https://fonts.googleapis.com">` and `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` to the head to preconnect the font resources ahead of time to minimize latency.

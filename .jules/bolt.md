## 2024-05-20 - Caching Static DOM elements\n**Learning:** The application uses plain JavaScript in  where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.\n**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent layout recalculations.
## 2024-05-20 - Caching Static DOM elements
**Learning:** The application uses plain JavaScript in `index.html` where static DOM elements were being repetitively fetched using `document.getElementById` on every function call. This was a missed opportunity for caching.
**Action:** Extract repetitive `document.getElementById` calls into a module-scoped constant object, to prevent redundant lookups.
## 2025-03-05 - Preconnect to Google Fonts
**Learning:** Adding `<link rel="preconnect">` tags to Google Fonts (`fonts.googleapis.com` and `fonts.gstatic.com`) speeds up First Contentful Paint. However, tests that manually edit HTML files to bypass external font loads during testing will break if not updated correctly.
**Action:** When adding preconnect optimizations, use `page.route` in Playwright to dynamically block external requests rather than parsing and modifying raw HTML files.

## 2024-05-07 - [Avoid Repetitive DOM Queries During State Updates]
**Learning:** Repetitive use of `querySelector` during state transitions (e.g., unlocking content) causes unnecessary DOM lookup overhead in this vanilla JS app, especially since the target elements are static.
**Action:** Extend the existing `DOM` object to cache references to nested elements (like `.content-text`, `.blur-overlay`, and `.tag`) on script load, bypassing runtime lookups.

# Issues Identified - March 14, 2026

## 1. ✅ FIXED: Duplicate Thug Notes Video
**Issue:** Thug Notes video (4LYC7Huhp7Q) appeared twice in Inferno module
- Once in `02-the-inferno-background-and-summary.html`
- Once in `04-the-inferno-professors-analysis.html`

**Fix Applied:** Removed duplicate from Professor's Analysis page

---

## 2. ⚠️ PENDING: Instagram Icon in Sidebar
**Issue:** Need Instagram SVG icon next to "Ancient Literature" brand in sidebar navigation (like Tokyo in Film has)

**Location:** Sidebar `.brand` section in all module pages

**Action Required:**
1. Create Instagram SVG icon
2. Add to sidebar navigation next to brand
3. Link to Instagram profile (need URL from user)

**Sample Implementation:**
```html
<div class="brand" tabindex="0">
    <h1>Ancient<br>Literature</h1>
    <a href="INSTAGRAM_URL" target="_blank" rel="noopener" aria-label="Follow on Instagram">
        <svg><!-- Instagram icon --></svg>
    </a>
    <div class="dropdown-menu">
        ...
    </div>
</div>
```

---

## 3. ⚠️ PENDING: Inconsistent Navigation Buttons
**Issue:** Not all module pages have consistent "Previous" and "Next" buttons

**Need to Audit:**
- All module pages in modules/ folder
- Check for missing Previous/Next buttons
- Standardize button placement and styling

**Standard Pattern Should Be:**
```html
<footer class="page-nav">
    <a href="previous-page.html" class="nav-btn prev">← Previous</a>
    <a href="next-page.html" class="nav-btn next">Next →</a>
</footer>
```

**Pages to Check:**
- Module 1: Introductions (3 files)
- Module 2: Cosmogonies (5 files)
- Module 3: Gilgamesh (4 files)
- Module 4: The Inferno (4 files)
- Module 5: Don Quixote (4 files)
- Module 6: The Iliad (6 files)
- Module 7: Bhagavad Gita (4 files)
- Module 8: Beowulf (4 files)
- Module 9: Song of Roland (4 files)
- Module 10: Hamlet (5 files)
- Module 11: Medea (7 files)
- Module 12: One Thousand and One Nights (4 files)
- Module 13: Wife of Bath (4 files)
- Module 14: Book of the City of Ladies (4 files)
- Module 15: Final Work (4 files)

---

## Next Steps

1. **Get Instagram URL from user** - Need actual Instagram profile link
2. **Create Instagram SVG** - Standard Instagram logo in appropriate color
3. **Audit navigation** - Check all 60+ module pages for navigation consistency
4. **Fix navigation** - Add missing Previous/Next buttons where needed
5. **Test** - Verify all navigation flows correctly
6. **Commit** - Push all changes to repository

---

**User Request:** "Not every page is consistent with 'Next' and 'previous' buttons; Some videos are duplicated i.e., thug notes twice in the inferno section, and there needs to be an instagram svg like in tokyo in film next to the textbook bar."

**Status:** 1/3 issues fixed, 2/3 pending user input and systematic audit

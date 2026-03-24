# AGENTS.md — modules/

All HTML files in this folder are academic course content. They are the body of the textbook. Treat every word as authored, cited, and intentional.

---

## What Lives Here

Each subfolder = one module or course section. Every module follows the same 4-page pattern:

1. `background.html` — historical context, author bio, cultural setting
2. `text.html` — primary reading (often full or excerpted text)
3. `analysis.html` — Professor Ladd's philosophical analysis
4. `discussion.html` — reflection questions and assessment prompts

Exceptions: Module 6 and Module 11 include a `chapter-intro.html` (chapter philosophical lens introduction). Module 15 includes final project materials.

---

## Absolute Rules for This Folder

### Never modify:
- Any prose, quotations, or paraphrased text
- Citations (author, date, title, page number)
- Philosophical frameworks: Becker's Terror Management Theory, Shay's PTSD framework, Kristeva's Feminist Semiotics, Campbell's Hero's Journey, Simone Weil on affliction
- Primary text excerpts (Gilgamesh, Iliad, Inferno, etc.)
- Video embed URLs or iframe src values
- Prev/next navigation links in footers
- The `<script src="../../assets/glossary.js"></script>` tag — every page must load this

### Permitted changes:
- CSS class additions (visual only, no content change)
- Adding ARIA attributes for accessibility
- Fixing broken HTML tags (unclosed elements, etc.)
- Standardizing video embeds to `.video-wrapper` pattern (preserve all URLs exactly)

---

## HTML Template Every File Must Follow

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page Title] — ENGL-2310</title>
  <link rel="stylesheet" href="../../assets/style.css">
  <!-- Google Fonts: Cinzel, Libre Baskerville, Lato -->
</head>
<body>
  <!-- Sidebar navigation with module dropdown -->
  <main>
    <!-- Page content -->
  </main>
  <!-- Footer: prev/next module navigation -->
  <!-- Site footer: CC license -->
  <script src="../../assets/glossary.js"></script>
</body>
</html>
```

**Path depth:** All files in `modules/module-X-name/` are two levels deep. Use `../../assets/` for all asset references.

---

## Course Content Reference

### Philosophical Frameworks (never misattribute these)

| Framework | Theorist | Applied To |
|-----------|---------|-----------|
| Terror Management Theory | Ernest Becker (*Denial of Death*, 1973) | Ch. I: Modules 1–5 |
| Moral Injury / PTSD | Dr. Jonathan Shay (*Achilles in Vietnam*, 1994) | Ch. II: Modules 6–10 |
| Feminist Semiotics / Abjection | Julia Kristeva | Ch. III: Modules 11–15 |
| Hero's Journey / Monomyth | Joseph Campbell | Modules 1, 3, 6 |
| Affliction (malheur) | Simone Weil | Modules 7, 9 |

### Chapter Boundaries

- **Chapter I (The Drive):** Modules 1–5
- **Chapter II (The Warrior):** Modules 6–10 — Module 6 includes chapter intro
- **Chapter III (The Woman):** Modules 11–15 — Module 11 includes chapter intro

### Primary Texts (do not alter titles, authors, or dates)

| Module | Text | Author | Date |
|--------|------|--------|------|
| 2 | Works and Days; Theogony | Hesiod | ~700 BCE |
| 2 | Popol Vuh | K'iche' Maya | ~1000–1550 CE |
| 3 | Epic of Gilgamesh | Anonymous | ~2100–1200 BCE |
| 4 | Inferno (Divine Comedy) | Dante Alighieri | 1320 CE |
| 5 | Don Quixote | Cervantes | 1605–1615 CE |
| 6 | The Iliad | Homer | ~750 BCE |
| 7 | Bhagavad Gita | Anonymous | ~400 BCE–200 CE |
| 8 | Beowulf | Anonymous | ~700–1000 CE |
| 9 | Song of Roland | Anonymous | ~1040–1115 CE |
| 10 | Hamlet | Shakespeare | 1600–1601 CE |
| 11 | Medea | Euripides | 431 BCE |
| 12 | One Thousand and One Nights | Anonymous | ~800–1300 CE |
| 13 | The Wife of Bath's Prologue and Tale | Chaucer | ~1392–1395 CE |
| 14 | The Book of the City of Ladies | Christine de Pizan | 1405 CE |

---

## Video Embed Standard

All video embeds must use the `.video-wrapper` pattern for responsive behavior:

```html
<div class="video-wrapper">
  <iframe src="[URL]" frameborder="0" allowfullscreen></iframe>
</div>
```

Do NOT use bare `<iframe>` tags without `.video-wrapper`. When standardizing, preserve the URL exactly — do not change any query parameters or video IDs.

---

## Navigation Links

Every page footer must have prev/next navigation. The order within a module:

```
background → text → analysis → discussion
```

Cross-module navigation follows the chapter order (Module 1 → Module 2 → ... → Module 15).

Do not change link hrefs without verifying the target file exists.

---

## for-instructors-only-hidden-from-students/

This folder contains materials not visible to enrolled students in the LMS. It includes grading rubrics, instructor notes, and answer keys. The same content rules apply — never modify text. Never link to these pages from student-facing pages.

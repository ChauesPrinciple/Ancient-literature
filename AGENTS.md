# AGENTS.md — Ancient Literature (ENGL-2310)

## What This Project Is

A complete online academic textbook for **ENGL-2310: Early World Literature**, taught by Professor Robert Ladd. It is a static HTML/CSS/JS website — no build system, no framework, no package.json. Every file is a standalone HTML page. The course covers ancient and medieval world literature through three philosophical lenses across 15 modules.

**Live site:** deployed via GitHub (repository: ChauesPrinciple/Ancient-literature, branch: main)

---

## Tech Stack

- **Pure HTML5 + vanilla JavaScript + CSS3** — no React, no Vue, no bundler
- **Google Fonts:** Cinzel (display headings), Libre Baskerville (body headings), Lato (body text)
- **No npm, no node_modules, no build step** — edit files and push; that's it
- **Git workflow:** `git add`, `git commit -m "..."`, `git push origin main`
- **Filename with parentheses:** always quote `"closure_axiom(1).html"` in shell commands

---

## File Structure

```
/
├── AGENTS.md                          ← this file
├── index.html                         ← landing page (accordion navigation)
├── glossary.html                      ← 69 literary terms with search
├── video_gallery.html                 ← supplementary video library
├── references.html                    ← works cited / citations
├── closure_axiom(1).html              ← Sacred Mathematics (Dante geometry)
├── assets/
│   ├── style.css                      ← MASTER stylesheet (1204 lines)
│   ├── dropdown.css                   ← DUPLICATE of style.css (do not reference)
│   ├── glossary.js                    ← auto-highlights 69 terms across all pages
│   └── media/                         ← hero images and media
└── modules/
    ├── getting-started/               ← 11 files: syllabus, netiquette, intro
    ├── assignments-and-engagement/    ← 6 files
    ├── for-instructors-only-hidden-from-students/  ← 4 files (hidden from students)
    ├── module-1-introductions/        ← 3 files
    ├── module-2-cosmogonies/          ← 5 files
    ├── module-3-gilgamesh/            ← 4 files
    ├── module-4-the-inferno/          ← 4 files
    ├── module-5-don-quixote/          ← 4 files
    ├── module-6-the-iliad/            ← 6 files
    ├── module-7-the-bhagavad-gita/    ← 4 files
    ├── module-8-beowulf/              ← 4 files
    ├── module-9-song-of-roland/       ← 4 files
    ├── module-10-hamlet/              ← 5 files
    ├── module-11-medea/               ← 7 files
    ├── module-12-one-thousand-and-one-nights/  ← 4 files
    ├── module-13-the-wife-of-bath/    ← 4 files
    ├── module-14-the-book-of-the-city-of-ladies/  ← 4 files
    └── module-15-final-work/          ← 4 files
```

**Do not modify:**
- `extracted/`, `extracted_pages/`, `source_citation_extracted/`, and all other `*_extracted/` folders — legacy backup content
- `.imscc`, `.docx`, `.zip`, `.txt` dump files — source documents, reference only

---

## Course Structure

### Three Chapters, Three Philosophical Lenses

**Chapter I: The Drive** — Ernest Becker, *Terror Management Theory*
- Module 1: Foundations (hero systems)
- Module 2: Cosmogonies (Works & Days, Popol Vuh)
- Module 3: Gilgamesh
- Module 4: The Inferno
- Module 5: Don Quixote

**Chapter II: The Warrior** — Dr. Jonathan Shay, *Achilles in Vietnam*
- Module 6: The Iliad (includes chapter intro)
- Module 7: The Bhagavad Gita
- Module 8: Beowulf
- Module 9: Song of Roland
- Module 10: Hamlet

**Chapter III: The Woman** — Julia Kristeva, Feminist Semiotics
- Module 11: Medea (includes chapter intro)
- Module 12: One Thousand and One Nights
- Module 13: The Wife of Bath
- Module 14: The Book of the City of Ladies
- Module 15: Final Work

### Standard Module Pattern (every module has 4 pages)
1. Background & Summary — historical context, author bio
2. Text — primary reading (often full text)
3. Professor's Analysis — philosophical lens applied to the text
4. Discussion — reflection questions, assessments

---

## ABSOLUTE RULES — Read Before Touching Anything

### 1. Zero Content Loss
**NEVER** delete or modify any of the following:
- Text content, prose, analysis, quotations
- Citations, author names, dates, historical facts
- Philosophical concepts and definitions (Becker, Shay, Kristeva, Campbell, Weil)
- Video URLs or embedded content sources
- The 69 glossary terms and their definitions (see `assets/AGENTS.md`)
- Navigation links (prev/next between modules)

### 2. Permitted Changes
- CSS styling (visual only)
- Adding ARIA attributes (accessibility)
- Adding or improving JavaScript functionality
- Wrapping existing HTML in semantic containers
- Adding new files
- Reorganizing CSS rules (only if rendered output is identical)

### 3. Backup Before Major Changes
For any change touching more than one file, or modifying `assets/style.css`, create a timestamped backup first.

### 4. Verify After Every Change
- Check that all text content is unchanged
- Verify navigation links still work
- Test in browser before committing

---

## HTML Template Structure

Every module page follows this structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- meta, title, Google Fonts, link to assets/style.css -->
</head>
<body>
  <!-- Sidebar navigation with dropdown -->
  <main>
    <!-- Content area -->
  </main>
  <!-- Footer: prev/next navigation -->
  <!-- Site footer: CC license -->
  <script src="../../assets/glossary.js"></script>
</body>
</html>
```

**Every page loads `glossary.js`** — it auto-highlights 69 literary terms. Do not remove this script tag.

**Relative paths matter.** Pages in `modules/module-X-name/` use `../../assets/` to reach the assets folder. Pages in root use `assets/`.

---

## CSS Rules

The **only** stylesheet that matters is `assets/style.css`. It is 1204 lines and covers everything.

`assets/dropdown.css` is a full duplicate of lines 21–148 of `style.css`. It is not referenced by any HTML file. Do not add references to it. It is a deletion candidate.

**Known CSS conflicts in style.css** (do not worsen them):
- `.module-card h3` defined twice (lines 805–818 and 886–889)
- `.module-card .btn` defined twice (lines 849–873 and 897–900)
- `.welcome-section h2` defined twice (lines 676–681 and 782–787)
- `.module-card p` defined twice (lines 820–827 and 892–895)

---

## JavaScript Rules

`assets/glossary.js` runs on every page. It:
- Compiles regexes for all 69 terms
- Walks the DOM and wraps matching terms in `<span class="glossary-term">` elements with tooltips
- Has a known performance issue: regex compiled inside the loop

Do not modify `glossary.js` without preserving all 69 term definitions exactly.

---

## Professor Ladd's Voice and Feedback Style

When writing or editing any course content, teaching materials, assignment prompts, or discussion guidance, follow these rules:

### Tone
- Direct but warm
- Diagnose root causes, not symptoms
- Concrete and specific — never vague
- Conditional framing: "Try...", "You could...", "Think about..."

### Forbidden Words/Phrases
- "sharp" (word)
- "Excellent work!", "Great job!", "Well done!", "Keep up the good work!"
- Em dashes (—) anywhere in feedback
- "The [Name] response" — use "Your response to [Name]"
- Any cross-student comparisons whatsoever

### Student Writing Requirements (ENGL-2310)
Forbidden in student submissions:
- "I think", "I believe", "I want to talk about"
- Second person ("you", "your") in academic writing
- Plot summary instead of analysis
- Biography unless directly relevant
- Opening with a simple sentence or statement of fact
- Informal register

Required:
- Theoretical framework applied (Becker, Campbell, Shay, Weil, Kristeva)
- Evidence rooted in the text
- MLA formatting
- Challenges ideas — no "I agree" posts

---

## closure_axiom(1).html — Sacred Mathematics

This file is special. It is a fully self-contained interactive mathematics visualization page. It has its own internal CSS and JavaScript — it does **not** load `assets/style.css` or `glossary.js`.

See `.windsurf/workflows/closure-axiom.md` for the complete agent workflow covering its architecture, domain knowledge (S³ geometry, qibla calculation, Dante's cosmos, Klein bottle), canvas inventory, drawing functions, and hard rules from previous sessions.

**Quick reference — 7 panels:**
1. Sacred Triangle — spherical triangle (North Pole, Observer, Mecca)
2. Qibla — Al-Bīrūnī's spherical trig on S²/S³
3. Ladder — S⁰ → S¹ → S² → S³ dimension explorer
4. The Rope — Dante's structured world-line (Hell/Purgatorio/Paradise)
5. Dante's S³ — 9 celestial spheres as ψ-slices
6. Coordinates — ψ/θ/φ explorer
7. Complete Object — Klein bottle IS the S³ visualization (one canvas, not two)

**Hard rules for this file:**
- Klein bottle and S³ are the SAME canvas (panel 7). Never split them.
- Panel order is fixed (Triangle+Qibla adjacent; Rope+Dante adjacent).
- `cKlein` canvas no longer exists — it was merged into `cFull`.
- The world-line (`knotPoint()`) encodes the actual three-phase journey structure. Do not replace with arbitrary math.

---

## Git Commit Convention

```
git add [files]
git commit -m "[what changed and why — be specific]"
git push origin main
```

Examples of good commit messages:
- `"Rope panel: structured journey Hell/Purgatorio/Paradise with named circles, Virgil/Beatrice guides"`
- `"Klein bottle IS the S3 visualization: single canvas, psi cross-section + world-line"`
- `"Fix ordering: Triangle+Qibla adjacent, Rope+Dante adjacent"`

---

## Known Issues (Do Not Introduce More)

1. `dropdown.css` — duplicate file, unreferenced, should be deleted but verify first
2. Four sets of conflicting CSS rules in `style.css` (listed above)
3. Mobile navigation: CSS classes exist but no JS toggle — broken on mobile
4. `glossary.js` compiles regex inside loop — performance issue on large pages
5. Video embeds inconsistent — some `<iframe>` direct, some `.video-wrapper` div
6. No ARIA attributes on accordions, dropdowns, or tooltips

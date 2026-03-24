# AGENTS.md — assets/

This folder contains the three shared resources that every page in the project depends on. Touch these files with extreme care.

---

## Files

### style.css — MASTER STYLESHEET (1204 lines)

Every HTML file in the project (except `closure_axiom(1).html`) links to this file. It is the only stylesheet that matters.

**Do not:**
- Delete any rule without verifying no page depends on it
- Add `!important` declarations
- Change font families (Cinzel, Libre Baskerville, Lato)
- Change color variables or brand colors

**Known conflicts — do not worsen:**
- `.module-card h3` defined twice (lines 805–818 and 886–889)
- `.module-card .btn` defined twice (lines 849–873 and 897–900)
- `.welcome-section h2` defined twice (lines 676–681 and 782–787)
- `.module-card p` defined twice (lines 820–827 and 892–895)

These are pre-existing. Do not add more conflicting rules. If asked to consolidate, keep the second definition (later in cascade order = higher precedence) unless visual testing proves otherwise.

---

### dropdown.css — DO NOT USE

This file is a full duplicate of lines 21–148 of `style.css`. It is **not referenced by any HTML file** in the project. Do not add references to it. It is a deletion candidate — verify with `grep -r "dropdown.css"` before deleting.

---

### glossary.js — AUTO-HIGHLIGHTING (174 lines)

Runs on every module page. Wraps the 69 defined literary terms in `<span class="glossary-term">` elements with tooltip definitions.

**The 69 terms (must remain exactly as defined):**
Abject, Allegory, Alliteration, Allusion, Anathema, Antagonist, Apostrophe, Archetype, Aristeia, Canto, Catharsis, Chivalric, Climax, Comitatus, Courtly Love, Cultural Area, Denouement, Deus Ex Machina, Dharma, Diction, Didactic, Epithet, Exposition, Feudalism, Figure Fulfillment, Foreshadowing, Frame Narrative, Hero, Heroic System, Hyperbole, Imagery, In media res, Intertextuality, Irony, Juxtaposition, Karma, Kenning, MacGuffin, Metafiction, Metaphor, Metonymy, Monotheistic, Motif, Narrator, Orientalism, Parody, Personification, Point of View, Polytheistic, Post Traumatic Stress Disorder, Propaganda, Protagonist, Redress, Satire, Semiotics, Simile, Soliloquy, Subtext, Symbolic, Syncretic, Syndesis, Themis, Verisimilitude, Zero Sum

**Rules for modifying glossary.js:**
1. Never delete or rename a term
2. Never alter a definition — these are academic definitions
3. If optimizing (e.g., moving regex compile outside the loop), export all 69 terms to a text file first, verify count = 69, verify definitions character-perfect, then make the change, then verify again
4. Do not change the `<span class="glossary-term">` structure — CSS and any future JS depends on this class name

**Known performance issue:** regex is compiled inside the forEach loop. This means for a page with many paragraphs, regexes are recompiled on every node. Safe to fix by hoisting the compile step outside the loop, but verify all 69 terms still highlight correctly after.

---

### media/ — Images and Media

Hero images and other visual assets. Do not rename or delete files without checking all HTML files that reference them. Image filenames are hardcoded in HTML `src` attributes.

---

## What closure_axiom(1).html Does NOT Use

`closure_axiom(1).html` is fully self-contained. It has its own internal `<style>` block and `<script>`. It does **not** load:
- `assets/style.css`
- `assets/glossary.js`

Do not add those links to it. See the root `AGENTS.md` and `.windsurf/workflows/closure-axiom.md` for its separate architecture.

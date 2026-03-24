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

## Per-Module Content Knowledge

Detailed summaries of what each module contains. Use this to avoid misrepresenting content, misattributing arguments, or accidentally duplicating/altering analysis.

---

### Module 1: Introductions
- **Files:** 3 pages (intro, discussion, supplementary)
- **Content:** Course foundations, introduction to hero systems via Joseph Campbell and Ernest Becker. Establishes Terror Management Theory as the lens for Chapter I.

---

### Module 2: Cosmogonies
- **Primary texts:** Hesiod's *Works and Days* / *Theogony* (~700 BCE); *Popol Vuh* (K'iche' Maya, ~1000–1550 CE)
- **Background:** Compares Greek and Mesoamerican creation myths; discusses natural law and ritual storytelling traditions.
- **Professor's Analysis:** Applies natural law theory to both texts. Explores how cosmogonies function as cultural instruction—establishing social order, gender roles, and moral frameworks through creation narratives. Embedded video on *Popol Vuh* creation.

---

### Module 3: Gilgamesh
- **Primary text:** *Epic of Gilgamesh* (~2100–1200 BCE)
- **Background:** Historical context of ancient Sumer; Enkidu as Gilgamesh's foil and civilizing force; death of Enkidu as the catalyst for the quest for immortality.
- **Professor's Analysis:** Applies Becker's *Denial of Death* and the Hero's Journey (Campbell). Argues Gilgamesh fails at literal immortality (the serpent steals the plant) but achieves symbolic immortality through the walls of Uruk and the epic itself. Enkidu/Gilgamesh relationship is the inverse of Beowulf/Grendel.

---

### Module 4: The Inferno
- **Primary text:** Dante's *Inferno* (Divine Comedy, 1320 CE)
- **Background:** Medieval cosmology, structure of Hell (9 circles), Virgil as guide, historical/mythological figures placed in Hell.
- **Professor's Analysis:** Four levels of reading (literal, allegorical, moral, anagogical). Personal psychological reading: the dark wood as midlife crisis. Concept of **syndesis** (binding together of opposites). Trajectory and geometry as structural metaphors. Introduces *closure_axiom(1).html* Sacred Mathematics visualization. Concept of **figure fulfillment** (biblical prefiguration) reappears in Module 9.

---

### Module 5: Don Quixote
- **Primary text:** Cervantes' *Don Quixote* (1605–1615 CE)
- **Background:** Cervantes' biography (Lepanto, captivity in Algiers), structure of Parts I and II.
- **Professor's Analysis:** **Metafiction** — Cervantes inserts himself as a character, claims to have translated the story from an Arabic manuscript (connecting to the Moorish Spain of Module 9). Three types of satire: **Juvenalian** (harsh, punitive), **Horatian** (gentle, comic), **Menippean** (philosophical, targets ideas). Class and race in Counter-Reformation Spain. Don Quixote as a man who has read too much chivalric romance—a foil for Song of Roland's uncritical heroism.

---

### Module 6: The Iliad
- **Extra file:** `02-chapter-two-introduction-the-warrior.html` — Chapter II intro
- **Chapter II Intro:** Cultural anthropology distinction between **guilt societies** (internal moral compass, Christian/modern West) and **honor/shame societies** (external reputation, ancient world). Introduces Dr. Jonathan Shay's *Achilles in Vietnam* (1994) and Elijah Anderson's *Code of the Streets*. Key concept: **betrayal of what's right** by a commander (REMF) as precursor to PTSD.
- **Primary text:** Homer's *Iliad* (~750 BCE)
- **Background:** Bronze Age Greece, Hittite Empire, archaeological context of Troy. Plot: Achilles' rage (mēnis) after Agamemnon takes Briseis; withdrawal from battle; death of Patroclus; aristeia; killing of Hector; ransoming of Hector's body.
- **Professor's Analysis:** **Zero-sum honor system** — honor is finite; one man's gain is another's loss. Marginalization causes: displacement from identity, loss of status, no legitimate path to redress. **Double bind** — warrior/gang member must fight to maintain status but fighting perpetuates the cycle. Aristeia as narrative structure (warrior's peak performance scene). **Communalizing trauma** as PTSD mitigation. Code of the Streets analogy: modern urban honor culture mirrors ancient warrior culture.

---

### Module 7: The Bhagavad Gita
- **Primary text:** *Bhagavad Gita* (~400 BCE–200 CE, embedded in *Mahabharata*)
- **Background:** Arjuna's moral crisis on the battlefield of Kurukshetra; Krishna as divine charioteer; the caste/dharma system; symbolism of the two armies (own nature vs worldly attachments).
- **Professor's Analysis:** Three major themes:
  1. **Jnana** (knowledge) — know your true self (atman = Brahman)
  2. **Karma** (action) — act without attachment to results; the path of selfless service
  3. **Bhakti** (devotional love) — surrender to the divine
  - Five reasons Krishna gives Arjuna to fight: soul is eternal, dharma demands it, warrior's duty, loss of reputation is worse than death, God wills it.
  - Three ways to act without accruing bad karma: act for God's sake, dedicate results to God, act without desire for the fruit of action.

---

### Module 8: Beowulf
- **Primary text:** *Beowulf* (Anglo-Saxon, ~700–1000 CE, transcribed by Christian monk)
- **Background:** Cotton Vitellius manuscript; Anglo-Saxon culture and the comitatus bond; Christian overlay on Norse pagan tradition; kennings (e.g., "whale-road"); interlace narrative structure; three battles: Grendel, Grendel's mother, the dragon. Tolkien connection.
- **Professor's Analysis:** Rejects the Aristotelian tragic hero reading (hubris/nemesis). Central argument: **Beowulf is about what it means to be a good king** who serves his people rather than expecting service.
  - **Beowulf/Grendel parallels:** Both called "aglǣca" (fierce fighter); both have the strength of thirty men; both from single-parent families with unnamed mothers; Grendel descends from Cain, Beowulf's father Ecgtheow killed without paying wergild.
  - **Gender analysis:** Women's roles as peace-weavers (Wealhtheow = "fithu-sibb folca," peace pledge between nations). Grendel's Mother as "ides agaewif" — monstrous because she acts aggressively like a man, not because she is evil per se. Modthryth as foil for Hygd; Hildeburh episode (Finnsburg digression).
  - **Beowulf as feminized hero:** His cross-tribal bond with Hrothgar functions like a peace-weaving marriage; he acts as a modified bride. The text champions generosity (ring-giver) over mere violence. True threat in the poem is humans (Ingeld's feud, Hrothulf's treachery), not monsters.
  - Transitional text: Norse honor society → Christian Anglo-Saxon guilt society.

---

### Module 9: Song of Roland
- **Primary text:** *Song of Roland* (~1040–1115 CE, Oxford manuscript c. 1100)
- **Background:** Oldest surviving French epic. Based on historical Battle of Roncesvalles (778 CE) — actual attackers were **Basque Christians, not Saracens**. Historical inaccuracies: the war was not 7 years long, Ganelon and Roland likely never coexisted, revenge was never carried out, Charlemagne was not yet emperor. Roland as chivalric archetype: hero's journey, oliphant, martyr's death.
- **Professor's Analysis:** Primary argument: the poem is **propaganda** — a military text that demonizes Muslims to justify Crusade expansion.
  - **Figure fulfillment:** Roland = Isaac/Christ; Charlemagne = Abraham/God; Ganelon = Judas. Roland dies on a hill flanked by two trees in a temple-like enclosure.
  - The "positive" reading (Roland as willing sacrifice) is undermined because Charles' revenge is the point — the sacrifice **justifies annihilation of Saracens**.
  - **Shay on demonizing the enemy:** Dishonoring the enemy is not natural but a tragic fall; a veteran's self-respect never fully recovers if he cannot see the enemy as worthy.
  - Dr. Paul M. Cobb on Islamic perspective: both Crusades and Jihad share monotheistic roots but differ — Crusades sought liberation of sacred land; Jihad sought rescue of souls.
  - Connection to Cervantes: the "pagan" Muslims Roland fights are likely from the same Moorish community that produced the Arabic manuscript Cervantes used for *Don Quixote*.

---

### Module 10: Hamlet
- **Extra file:** `04-hamlet-laurence-olivier-shakespeare-1948.html` — 1948 film adaptation
- **Primary text:** Shakespeare's *Hamlet* (1600–1601 CE, 5 acts)
- **Background:** Shakespeare (1564–1616); source in Saxo Grammaticus's *Gesta Danorum* (c. 1200) and Belleforest's *Histoires Tragiques* (1570). Elizabethan context: divine right of monarchy, private revenge as "wild justice" (Bacon), wergild transition to state justice. Denmark as prison ("2.2.239").
- **Professor's Analysis:** Central thesis: **Hamlet is acting rationally; he is the first model of the modern existential dilemma**.
  - Hamlet and Song of Roland are the bookends of the transition from honor-based to guilt-based (Christian) culture.
  - **Freudian framework:** Id (pleasure principle, Eros/Libido/Thanatos), Ego (reality principle, mediator), Superego (conscience + ego ideal, internalized societal standards). The superego is the primary culprit — when conscience and ego ideal conflict, repression results.
  - **Hamlet's "failure to act" debunked:** He kills Rosencrantz and Guildenstern without hesitation; kills Polonius without checking; only pauses on Claudius because killing a praying man would send him to heaven — this is a concern for **justice**, not cowardice.
  - "To be or not to be" soliloquy: "Thus conscience does make cowards of us all" — conscience (superego) paralyzes when duty and morality conflict.
  - **Ophelia's flower speech (Act 4, Scene 5) as subversive agency:** Rosemary/pansies = remembrance/thoughts (Laertes); Fennel/columbine = flattery/male adultery (Claudius); Rue = bitterness/adultery (Gertrude, and kept for herself); Daisy set down = no innocence in Danish court; Violets withered = faithfulness died with Polonius. Ophelia was **calling out everyone in the room**.
  - **Gertrude as possible true antagonist:** Claudius shows genuine remorse in prayer; Gertrude watches Ophelia drown and makes no attempt to save her. "Perhaps she wanted a man she could control."

---

### Module 11: Medea
- **Extra file:** `02-chapter-three-introduction-the-women.html` — Chapter III intro; `09-credit-to-the-women.html`
- **Chapter III Intro:** Introduces Julia Kristeva's feminist semiotics via Ferdinand de Saussure (signifier/signified) and Mikhail Bakhtin (intertextuality, social registers). Kristeva's **semi-analysis**: texts are always in production, not finished products. "Any text is constructed of a mosaic of quotations." Surveys the "problematic women" of prior modules (Pandora, Ishtar, Grendel's Mother, Bramimonde, Gertrude).
- **Primary text:** Euripides' *Medea* (431 BCE, won 3rd prize at Dionysia)
- **Background:** Euripides (484–406 BCE), Golden Age of Athens, Peloponnesian War context. Jason's betrayal — Medea sacrificed family, homeland, and future for Jason, who abandoned her for the Princess of Corinth. Filicide as ultimate revenge to obliterate Jason's happiness entirely. Euripides: tragedy unfolds when hate becomes stronger than love.
- **Professor's Analysis:** Kristeva's three-tiered feminist struggle: (1) women demand equal access to the symbolic order; (2) women reject the male symbolic order in the name of difference; (3) women reject the masculine/feminine dichotomy metaphysically.
  - Medea is royalty (grandfather = Helios, Sun God); Jason only completed his quest **because of her military prowess**, not his. Her strength is precisely what Jason and the King of Colchis fear.
  - Medea's rage parallels Achilles' in the *Iliad*; Kristeva's abjection applies more precisely than Shay's PTSD here.
  - Medea is not monstrous because she killed children (it is not original to the myth that she slays them) but because she **acted in a masculine way** — anathema in fifth-century Athens.
  - Parallel to Grendel's Mother, Pandora, women in *One Thousand and One Nights*, Wife of Bath. Euripides sides with Kristeva: Medea is a hero judged as monster by a double standard.

---

### Module 12: One Thousand and One Nights
- **Primary text:** *One Thousand and One Nights* (~800–1300 CE, various origins)
- **Background:** Antoine Galland (1646–1715) — French Orientalist who introduced The Nights to the West. Source: Syrian manuscript (15th century, only 35 tales/271 nights). Galland added Sinbad, Aladdin, and Ali Baba from outside sources (Hanna Diab, a Syrian Christian informant). **Aladdin and Ali Baba do not appear in any pre-Galland Arabic manuscript**. Frame story: King Shahryar's misogynistic reign of terror; Scheherazade's *mise en abyme* storytelling strategy.
- **Professor's Analysis:** Core theme: **the oppressor and the oppressed**. Scheherazade's strategy is an act of feminine agency — using storytelling to humanize women and de-radicalize Shahryar.
  - Stories progress logically: dark/brutal → balanced (wicked woman AND idiot man) → historical figure Haroun al-Rashid (foil for Shahryar: treated all people equally).
  - **Orientalism:** Edward Said's framework applied — Western "translators" (Galland, Edward Lane, Richard Francis Burton) imposed imperialist, exoticizing perspectives. Burton (soldier/linguist): racist, misogynist, imperialist; accentuated erotic elements; spread the idea of the East as "exotic, erotic, and easily exploitable."
  - Scheherazade must deconstruct both **misogyny within patriarchy** AND the **Orientalist project** that robs her of agency a second time.

---

### Module 13: The Wife of Bath
- **Primary text:** Chaucer's *The Wife of Bath's Prologue and Tale* (~1392–1395 CE, from *Canterbury Tales*)
- **Background:** Geoffrey Chaucer (c. 1343–1400) — father of English poetry. Norman Conquest of 1066: French culture dominated; Domesday Book; Anglo-Saxon ruling class replaced. **Feudalism** (imported by William the Conqueror): hierarchical system claiming God as authority; comitatus as blueprint. **Chivalric code** and **courtly love** (Arthurian romances, Lancelot and Guinevere). Reality for medieval women: child-bearing, household, no role outside these. Crusades opened trade routes and created the merchant class.
- Summary: Wife of Bath (Alyson/Alys), widow with 5 husbands, defends multiple marriages via Scripture. Her tale: Arthurian knight rapes a maiden, must discover "what women most desire" to avoid execution. Answer: **sovereignty over their own lives**. Loathly lady transformation when knight grants her choice.
- **Professor's Analysis:** Chaucer's innovations over other "loathly lady" versions (*Wedding of Sir Gawain*, *Tale of Florent*):
  - Knight and lady are **never named** (universalizing).
  - Knight's crime is explicitly **rape** (making the punishment directly connected to the crime).
  - Loathness described via **inexpressibility trope** (normally used for heroines' beauty — inverted here).
  - The old woman's status (low class) compounds the knight's distress; her 100-line speech detaches **nobility of rank from nobility of character**.
  - No external curse causes her transformation — she can **self-transform** (independent agency).
  - Anti-fraternal satire via "Friars as thick as specks of dust" — displacing the faery world of Arthur's age.
  - Alyson is one of English literature's **first feminist figures**: women want sovereignty and equal representation.

---

### Module 14: The Book of the City of Ladies
- **Primary text:** Christine de Pizan's *The Book of the City of Ladies* (1405 CE)
- **Background:** Christine de Pizan (b. 1364, Italy/Paris) — **first professional writer** in Western literary tradition. Father educated her (unusual for women). Widowed at 25 with 3 children; turned to writing. Quarrel of the Rose: challenged Jean de Meun's *Romance of the Rose* ("All women are, will be, or have been whores"). This published challenge marks the **birth of feminism**. Wrote ~15 manuscripts in 6 years; commissioned to write biography of King Charles V. Retired to convent 1418; final poem 1429 celebrating Joan of Arc.
- Summary: Dream-vision framing; three personified virtues — **Lady Reason, Lady Rectitude, Lady Justice** — direct Pizan to build a metaphorical City of Ladies. Three parts: Reason (pagan women of courage/artistry), Rectitude (Hebrew/Christian women of prophecy/chastity), Justice (female saints). Anticipated Thomas More's *Utopia* by 100+ years.
- **Professor's Analysis:** Double standards in language (charismatic vs bubbly; assertive vs bossy; "she" verbs: shivered/wept/murmured vs "he" verbs: muttered/grinned/shouted/killed). Feminism as **conflict theory**: patriarchal oppression exists in all social sectors; feminist focus on intersectionality.
  - Pizan's method: **empirical** — collecting data (historical examples of great women) to counter misogynist claims. Anticipates 16th-century Protestantism and 17th-century New Science epistemology.
  - Exposes fallacies in Aristotle and Ovid's misogyny (Ovid attacked women after castration from promiscuity).
  - Lady Reason/Rectitude/Justice also invoke the Christian Trinity — reason, rectitude, and justice as inherently human and divine qualities.
  - Reclaims "loathly women" (including Medea) as heroes condemned by a double standard.

---

### Module 15: Final Work
- **Files:** 4 pages (Major Projects Overview, Literary Analysis Essay, Anthology Project, The Final Chapter)
- **Content:** No primary text. Two major assignments:
  1. **Literary Analysis Essay:** Choose a theme from the course, apply it to one text, connect to a contemporary issue. Requires one outside scholarly source.
  2. **Anthology Project:** Create a thematic anthology of 10 texts (can include songs, films, games). Requires title page, table of contents, and 3-page preface.
- **The Final Chapter:** Professor Ladd's closing reflection; recommends *Hidden Brain* podcast episode "The Story of Your Life."

---

### Getting Started (modules/getting-started/)
- 11 files: course introduction, meet your instructor, syllabus, course schedule, technology statement, netiquette, student resources handbook, Office 365 info, introductions discussion, icebreaker, course questions.
- Course dates: *Gilgamesh* (2100 BCE) → *One Thousand and One Nights* translation (1706 CE).
- Structure: 3 chapters, non-chronological organization, organized by philosophical topic.
- Communication: weekly posts Monday, discussion submissions due Thursday, responses due Monday.

---

### Assignments and Engagement (modules/assignments-and-engagement/)
- 6 files: Literary Quick Takes, End-of-Chapter Tests, Literary Analysis (full prompt), Anthology Project (full prompt), Redo/Late assignments, Research Guide.
- Literary Quick Takes: short weekly analysis responses.
- End-of-Chapter Tests: assess comprehension at Chapter I/II/III boundaries.

---

## for-instructors-only-hidden-from-students/

This folder contains materials not visible to enrolled students in the LMS. It includes grading rubrics, instructor notes, and answer keys. The same content rules apply — never modify text. Never link to these pages from student-facing pages.

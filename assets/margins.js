/* margins.js — social annotation layer for ENGL-2310 primary-text pages.
 *
 * Adds a slide-over "margin" to the page: readers select a paragraph or
 * stanza, write a note of one of six kinds, reply to each other, and see
 * everyone's notes beside the text. Instructor sees a class view with
 * per-reader note counts and active reading time.
 *
 * Storage: Firebase (anonymous auth + Firestore) when configured below.
 * Falls back to localStorage "preview mode" — notes stay in the browser.
 *
 * Setup: paste your Firebase web config into MARGINS_FIREBASE, add your
 * anonymous-auth uid to MARGINS_INSTRUCTORS, and apply the security rules
 * documented in modules/for-instructors-only-hidden-from-students/
 * 05-social-annotation-and-the-margin.html
 */
(function () {
'use strict';

/* ==================== configuration ==================== */
var MARGINS_FIREBASE = {
  apiKey: 'PASTE_API_KEY',
  authDomain: 'PASTE_PROJECT.firebaseapp.com',
  projectId: 'PASTE_PROJECT',
  appId: 'PASTE_APP_ID'
};
var MARGINS_INSTRUCTORS = [ /* anonymous-auth uids that count as instructor, e.g. 'aBc123...' */ ];
var FB_VERSION = '10.14.1';
var DEFAULT_SETTINGS = { required: 3, counts: ['comment','question','gloss','connection','performance','response'] };

var KINDS = [
  { id: 'comment',     label: 'Comment',      hint: 'Say what you notice in the passage.' },
  { id: 'question',    label: 'Question',     hint: 'Ask something the class can take up.' },
  { id: 'gloss',       label: 'Gloss',        hint: 'Explain a word or phrase the way a reader of its own time heard it.' },
  { id: 'connection',  label: 'Text-to-text', hint: 'Connect this passage to another text in the course.' },
  { id: 'performance', label: 'Performance',  hint: 'Say how the passage should sound read aloud, and why.' },
  { id: 'response',    label: 'Response',     hint: 'Write your own reaction, in your own terms.' }
];
var KIND = {}; KINDS.forEach(function (k) { KIND[k.id] = k; });

/* ==================== identity of this page ==================== */
var SCRIPT = document.currentScript ||
  (function () { var s = document.querySelectorAll('script[data-text]'); return s[s.length - 1]; })();
var DOC_ID = (SCRIPT && SCRIPT.getAttribute('data-text')) ||
  location.pathname.split('/').pop().replace(/\.html?$/i, '');
var LS_KEY = 'margins-' + DOC_ID;

/* ==================== state ==================== */
var S = {
  mode: 'loading',        // loading | shared | local
  me: { id: null, instructor: false, canWrite: true, name: '' },
  mine: { notes: {}, reading: {} },
  people: {}, guide: {}, settings: { required: DEFAULT_SETTINGS.required, counts: DEFAULT_SETTINGS.counts.slice() },
  names: {},
  anchor: null, quote: '', kind: 'comment', filter: 'all',
  draft: '', replyTo: null, replyDraft: '', confirmDel: null, msg: '',
  view: 'read',           // read | dash
  person: null, sd: null, pending: {}, open: false
};
var db = null, myRef = null, blocks = [];

/* ==================== utilities ==================== */
function $(id) { return document.getElementById(id); }
function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}
function newId() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }
function fmtDate(at) {
  var d = new Date(at);
  return isNaN(d) ? '' : d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}
function fmtMin(s) { return s >= 60 ? Math.round(s / 60) + ' min' : s > 0 ? '<1 min' : '0 min'; }
function plural(n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); }
function norm(s) { return String(s || '').replace(/\s+/g, ' ').trim(); }
function hintOf(el) { return norm(el.textContent).slice(0, 60); }

/* ==================== data shape — everything read from the store is untrusted ==================== */
function cleanNote(n) {
  if (!n || typeof n !== 'object') return null;
  var anchor = Number(n.anchor);
  if (!Number.isInteger(anchor) || anchor < 1) return null;
  return {
    doc: String(n.doc || DOC_ID), anchor: anchor,
    parent: n.parent ? String(n.parent) : '',
    kind: n.parent ? 'reply' : (KIND[n.kind] ? n.kind : 'comment'),
    body: String(n.body || '').slice(0, 4000),
    quote: n.quote ? String(n.quote).slice(0, 200) : '',
    hint: n.hint ? String(n.hint).slice(0, 80) : '',
    at: String(n.at || ''), deleted: !!n.deleted, by: n.by ? String(n.by) : ''
  };
}
function cleanNotes(obj) {
  var out = {};
  if (obj && typeof obj === 'object') {
    for (var k in obj) { if (Object.prototype.hasOwnProperty.call(obj, k)) { var c = cleanNote(obj[k]); if (c) out[k] = c; } }
  }
  return out;
}
function cleanPerson(d) {
  var reading = {};
  if (d && d.reading && typeof d.reading === 'object') {
    for (var k in d.reading) {
      var s = Number(d.reading[k]);
      if (s > 0 && isFinite(s)) reading[k] = Math.min(s, 1e7);
    }
  }
  return { notes: cleanNotes(d && d.notes), reading: reading };
}
function cleanSettings(d) {
  var r = Number(d && d.required);
  var counts = (d && Array.isArray(d.counts)) ? d.counts.filter(function (k) { return !!KIND[k]; }) : DEFAULT_SETTINGS.counts.slice();
  return { required: Number.isInteger(r) && r >= 0 && r <= 20 ? r : DEFAULT_SETTINGS.required, counts: counts };
}
function people() { var p = Object.assign({}, S.people); if (S.me.id) p[S.me.id] = S.mine; return p; }
function allNotes() {
  var out = [];
  var p = people(), uid, d, id;
  for (uid in p) { d = p[uid]; for (id in d.notes) out.push(Object.assign({ id: id, author: uid, instr: false }, d.notes[id])); }
  for (id in S.guide) { var n = S.guide[id]; out.push(Object.assign({ id: id, author: n.by || '', instr: true }, n)); }
  return out.filter(function (n) { return n.doc === DOC_ID; });
}
function byTime(a, b) { return String(a.at).localeCompare(String(b.at)); }

/* ==================== anchoring ==================== */
function scanBlocks() {
  var root = document.querySelector('article.prose') || document.querySelector('main') || document.body;
  var els = root.querySelectorAll('p, blockquote, li');
  var i = 0;
  blocks = [];
  els.forEach(function (el) {
    if (el.closest('nav, aside, header, footer, .mg-panel, .page-nav')) return;
    if (!norm(el.textContent)) return;
    i++;
    el.dataset.mga = i;
    el.classList.add('mg-block');
    el.setAttribute('tabindex', '0');
    el.setAttribute('role', 'button');
    el.setAttribute('aria-label', 'Passage ' + i + '. Select to open its margin.');
    blocks.push(el);
  });
}
function blockAt(anchor) { return blocks[anchor - 1] || null; }

/* If the stored hint no longer sits at its anchor (text edited), find where it moved. */
function resolveAnchor(n) {
  var el = blockAt(n.anchor);
  if (el && (!n.hint || hintOf(el) === n.hint)) return n.anchor;
  if (!n.hint) return n.anchor;
  for (var i = 0; i < blocks.length; i++) {
    if (hintOf(blocks[i]) === n.hint) return i + 1;
  }
  return n.anchor; // give up: show at original anchor
}

/* ==================== saving ==================== */
var writers = {};
function queueWrite(key, ref, body) {
  var w = writers[key] || (writers[key] = { busy: false, dirty: false });
  w.ref = ref; w.body = body; w.dirty = true; pump(w);
}
function pump(w) {
  if (w.busy || !w.dirty) return;
  w.busy = true; w.dirty = false;
  Promise.resolve(w.ref.set(w.body())).catch(onWriteError).then(function () {
    w.busy = false;
    if (w.dirty) pump(w);
  });
}
function onWriteError(e) {
  var code = e && e.code;
  if (code === 'permission-denied' || code === 'invalid_argument') {
    S.me.canWrite = false;
    S.msg = 'Your access to this page is read-only, so that change was not saved.';
  } else if (code === 'resource-exhausted' || code === 'quota_exceeded') {
    S.msg = 'Too many saves at once, or the margin is full. Wait a moment, then try again.';
  } else {
    S.msg = 'That change did not save. Check your connection and try again.';
  }
  schedule();
}
function saveLocal() {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify({
      mine: S.mine, guide: S.guide, settings: S.settings,
      instructor: S.me.instructor, name: S.me.name
    }));
  } catch (e) {}
}
function saveMine() {
  if (S.mode === 'local') return saveLocal();
  if (S.mode === 'shared' && S.me.canWrite) queueWrite('mine', myRef, function () { return JSON.parse(JSON.stringify(S.mine)); });
}
function saveGuide() {
  if (S.mode === 'local') return saveLocal();
  if (S.mode === 'shared') queueWrite('guide', db.doc('guide/notes'), function () { return { notes: JSON.parse(JSON.stringify(S.guide)) }; });
}
function saveSettings() {
  if (S.mode === 'local') return saveLocal();
  if (S.mode === 'shared') queueWrite('settings', db.doc('guide/settings'), function () { return JSON.parse(JSON.stringify(S.settings)); });
}
function saveProfile() {
  if (S.mode === 'local') return saveLocal();
  if (S.mode === 'shared') queueWrite('profile', db.doc('profiles/' + S.me.id), function () { return { name: S.me.name }; });
}

function addNote(note) {
  var id = newId();
  note.doc = DOC_ID;
  note.hint = hintOf(blockAt(note.anchor)) || '';
  if (S.me.instructor) {
    if (S.mode === 'shared') note.by = S.me.id;
    S.guide = Object.assign({}, S.guide); S.guide[id] = note; saveGuide();
  } else {
    S.mine.notes[id] = note; saveMine();
  }
}
function deleteNote(n) {
  var hasReplies = allNotes().some(function (r) { return r.parent === n.id && !r.deleted; });
  var store = n.instr ? S.guide : S.mine.notes;
  if (!store[n.id]) return;
  if (hasReplies) store[n.id] = Object.assign({}, store[n.id], { deleted: true, body: '', quote: '' });
  else delete store[n.id];
  n.instr ? saveGuide() : saveMine();
}
function canDelete(n) {
  if (S.mode === 'loading') return false;
  if (n.instr) return S.me.instructor && (S.mode === 'local' || n.author === S.me.id || !n.author);
  return n.author === S.me.id;
}

/* ==================== active reading ==================== */
var lastAct = Date.now();
['pointermove', 'pointerdown', 'keydown', 'scroll', 'wheel', 'touchstart'].forEach(function (ev) {
  addEventListener(ev, function () { lastAct = Date.now(); }, { passive: true, capture: true });
});
setInterval(function () {
  if (S.mode === 'loading' || !S.me.canWrite || S.view !== 'read') return;
  if (document.visibilityState === 'visible' && Date.now() - lastAct < 60000) {
    S.pending[DOC_ID] = (S.pending[DOC_ID] || 0) + 5;
  }
}, 5000);
function flushReading() {
  var ks = Object.keys(S.pending);
  if (!ks.length) return;
  ks.forEach(function (k) { S.mine.reading[k] = (S.mine.reading[k] || 0) + S.pending[k]; });
  S.pending = {};
  saveMine();
}
setInterval(flushReading, 60000);
document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') flushReading(); });

/* ==================== names ==================== */
function nameOf(uid) {
  if (!uid) return 'Instructor';
  if (uid === S.me.id) return S.me.name || 'You';
  return S.names[uid] || 'A reader';
}
function myNameKnown() { return S.mode !== 'shared' || !!S.me.name; }

/* ==================== styles ==================== */
function injectStyle() {
  var css = `
.mg-block { cursor: pointer; border-radius: 4px; transition: background .12s; position: relative; }
.mg-block:hover { background: #e8f4f2; }
.mg-block.mg-sel { background: #d6ece8; box-shadow: inset 3px 0 0 #007777; }
.mg-block.mg-has { box-shadow: inset 3px 0 0 rgba(0,119,119,.45); }
.mg-mark { position: absolute; right: 4px; top: 2px; font: 600 11px/1.4 Lato, sans-serif; color: #007777;
  background: #e3f0ee; border-radius: 8px; padding: 1px 6px; }
.mg-mark .mg-tick { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #a5312a; margin-right: 4px; }
.mg-toggle { position: fixed; right: 18px; bottom: 18px; z-index: 9000; font: 600 14px Lato, sans-serif;
  background: #007777; color: #fff; border: 0; border-radius: 22px; padding: 10px 18px; cursor: pointer;
  box-shadow: 0 3px 12px rgba(0,0,0,.25); }
.mg-toggle .mg-count { background: rgba(255,255,255,.25); border-radius: 10px; padding: 0 8px; margin-left: 6px; }
.mg-panel { position: fixed; top: 0; right: 0; bottom: 0; width: min(94vw, 400px); z-index: 9001;
  background: #fff; border-left: 1px solid #cfd8d6; box-shadow: -4px 0 18px rgba(0,0,0,.18);
  transform: translateX(105%); transition: transform .18s ease-out;
  display: flex; flex-direction: column; font: 14px/1.5 Lato, sans-serif; color: #1b2130; }
.mg-panel.mg-open { transform: translateX(0); }
.mg-scroll { overflow-y: auto; padding: 18px 18px 40px; flex: 1; }
.mg-top { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; margin-bottom: 10px; }
.mg-title { font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: #5a6374; font-weight: 700; margin: 0; }
.mg-panel button { font: inherit; color: inherit; background: none; border: 0; padding: 0; cursor: pointer; }
.mg-textbtn { color: #007777; font-size: 12px; font-weight: 700; }
.mg-textbtn:hover { text-decoration: underline; }
.mg-x { font-size: 20px; line-height: 1; color: #5a6374; padding: 2px 6px; }
.mg-target { font-family: 'Libre Baskerville', Georgia, serif; font-size: 14px; line-height: 1.45; margin: 0 0 12px;
  padding: 2px 0 2px 12px; border-left: 2px solid #007777; max-height: 9em; overflow: auto; }
.mg-target small { display: block; font: 10px 'Lato', sans-serif; letter-spacing: .08em; text-transform: uppercase; color: #5a6374; margin-bottom: 3px; }
.mg-lede { color: #5a6374; font-size: 13px; margin: 0 0 10px; }
.mg-note { border-top: 1px solid #e2e6ea; padding: 12px 0; display: flex; flex-direction: column; gap: 5px; }
.mg-note:first-child { border-top: 0; padding-top: 0; }
.mg-meta { display: flex; flex-wrap: wrap; align-items: baseline; gap: 3px 8px; font-size: 12px; }
.mg-who { font-weight: 700; }
.mg-who.mg-instr, .mg-badge { color: #a5312a; }
.mg-badge { font-size: 10px; letter-spacing: .08em; text-transform: uppercase; font-weight: 700;
  background: #f7e5e2; padding: 1px 6px; border-radius: 3px; }
.mg-when { color: #5a6374; font-size: 11px; margin-left: auto; }
.mg-kind { font-size: 11px; font-weight: 700; padding: 1px 8px; border-radius: 999px; }
.mg-k-comment { color: #4a5263; background: #eceef2; }
.mg-k-question { color: #2345a3; background: #e3e8f7; }
.mg-k-gloss { color: #7d5c10; background: #f3ead0; }
.mg-k-connection { color: #1d6c59; background: #ddf0ea; }
.mg-k-performance { color: #7a3a8e; background: #efe3f4; }
.mg-k-response { color: #9b3b59; background: #f8e4eb; }
.mg-quote { font-family: 'Libre Baskerville', Georgia, serif; font-style: italic; color: #5a6374; font-size: 13px; margin: 0; }
.mg-body { margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; font-size: 13.5px; }
.mg-body.mg-gone { color: #5a6374; font-style: italic; }
.mg-acts { display: flex; gap: 14px; font-size: 12px; }
.mg-acts button { color: #5a6374; font-weight: 700; }
.mg-acts button:hover { color: #007777; }
.mg-acts .mg-danger, .mg-danger { color: #a5312a; }
.mg-replies { margin-left: 4px; padding-left: 12px; border-left: 1px solid #e2e6ea; display: flex; flex-direction: column; gap: 10px; margin-top: 4px; }
.mg-replies .mg-note { border: 0; padding: 0; }
.mg-composer { display: flex; flex-direction: column; gap: 9px; padding-top: 14px; border-top: 1px solid #e2e6ea; margin-top: 12px; }
.mg-kinds { display: flex; flex-wrap: wrap; gap: 6px; }
.mg-kbtn { font-size: 11.5px; font-weight: 700; padding: 4px 10px; border-radius: 999px; border: 1px solid #cfd8d6; color: #5a6374; }
.mg-kbtn[aria-checked="true"] { color: #007777; border-color: #007777; background: #e3f0ee; }
.mg-hint { color: #5a6374; font-size: 12px; margin: 0; }
.mg-qchip { display: flex; align-items: baseline; gap: 8px; font-size: 12px; background: #e3f0ee; padding: 6px 10px; border-radius: 6px; }
.mg-qchip span { font-family: 'Libre Baskerville', Georgia, serif; font-style: italic; flex: 1; min-width: 0; overflow-wrap: anywhere; }
.mg-panel textarea, .mg-panel input[type="text"], .mg-panel input[type="number"] { width: 100%; font: inherit; font-size: 13px;
  color: #1b2130; background: #f7f8f9; border: 1px solid #cfd8d6; border-radius: 6px; padding: 8px 10px; resize: vertical; }
.mg-panel input[type="number"] { width: 5rem; }
.mg-panel textarea:focus, .mg-panel input:focus { outline: 2px solid #007777; outline-offset: -1px; }
.mg-row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.mg-primary { background: #007777; color: #fff; font-weight: 700; font-size: 13px; padding: 7px 14px; border-radius: 6px; }
.mg-primary:hover { filter: brightness(1.12); }
.mg-primary:disabled { opacity: .45; cursor: not-allowed; }
.mg-msg { font-size: 12px; color: #a5312a; margin: 0; }
.mg-ro { font-size: 12.5px; color: #5a6374; border-top: 1px solid #e2e6ea; padding-top: 12px; margin: 10px 0 0; }
.mg-empty { color: #5a6374; font-size: 13px; margin: 0; }
.mg-progress { display: flex; flex-direction: column; gap: 5px; font-size: 12.5px; margin-bottom: 12px; }
.mg-meter { display: flex; gap: 4px; }
.mg-meter i { flex: 1; height: 5px; border-radius: 3px; background: #e2e6ea; }
.mg-meter i.on { background: #007777; }
.mg-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.mg-chip { font-size: 11.5px; padding: 3px 9px; border-radius: 999px; border: 1px solid #cfd8d6; color: #5a6374; }
.mg-chip[aria-pressed="true"] { border-color: #1b2130; color: #1b2130; background: #eef0f2; }
.mg-ov { text-align: left; display: block; width: 100%; padding: 9px 6px; border-top: 1px solid #e2e6ea; }
.mg-ov:first-child { border-top: 0; }
.mg-ov:hover { background: #eef5f4; }
.mg-ov-ln { font-size: 10.5px; color: #5a6374; letter-spacing: .06em; text-transform: uppercase; }
.mg-ov-txt { display: block; font-family: 'Libre Baskerville', Georgia, serif; font-size: 13px; line-height: 1.35; margin: 1px 0; }
.mg-ov-meta { display: flex; flex-wrap: wrap; gap: 5px; align-items: center; font-size: 11.5px; color: #5a6374; }
.mg-ov-prev { display: block; font-size: 12px; color: #5a6374; overflow-wrap: anywhere; margin-top: 2px; }
.mg-dash-row { border-top: 1px solid #e2e6ea; padding: 10px 0; font-size: 12.5px; }
.mg-dash-row:first-child { border-top: 0; }
.mg-dash-name { font-weight: 700; text-align: left; }
.mg-dash-name:hover { color: #007777; text-decoration: underline; }
.mg-bar { display: inline-block; width: 70px; height: 6px; background: #e2e6ea; border-radius: 3px; overflow: hidden; vertical-align: middle; margin-right: 7px; }
.mg-bar span { display: block; height: 100%; background: #007777; }
.mg-pill { font-size: 10px; font-weight: 700; padding: 1px 7px; border-radius: 999px; margin-left: 6px; }
.mg-pill.mg-ok { color: #24704f; background: #ddf0e6; }
.mg-pill.mg-short { color: #9a5b0c; background: #f8ecd9; }
.mg-facts { display: grid; grid-template-columns: 1fr auto; gap: 4px 12px; font-size: 12.5px; margin: 0 0 10px; }
.mg-facts dd { margin: 0; color: #5a6374; }
.mg-section { display: flex; flex-direction: column; gap: 8px; margin-top: 16px; }
.mg-section h3 { font-size: 13px; margin: 0; }
.mg-section p { margin: 0; font-size: 12.5px; color: #5a6374; }
.mg-check { display: flex; align-items: center; gap: 8px; font-size: 13px; }
.mg-foot { padding: 10px 18px; border-top: 1px solid #e2e6ea; font-size: 11.5px; color: #5a6374;
  display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.mg-seg { display: inline-flex; border: 1px solid #cfd8d6; border-radius: 6px; overflow: hidden; }
.mg-seg button { padding: 3px 9px; font-size: 11.5px; }
.mg-seg button[aria-pressed="true"] { background: #1b2130; color: #fff; }
@media (prefers-reduced-motion: reduce) { .mg-panel { transition: none; } }
@media (max-width: 760px) { .mg-panel { width: 100vw; border-left: 0; } }
`;
  var st = document.createElement('style');
  st.id = 'mg-style'; st.textContent = css;
  document.head.appendChild(st);
}

/* ==================== DOM shell ==================== */
function injectShell() {
  var t = document.createElement('button');
  t.id = 'mg-toggle'; t.className = 'mg-toggle'; t.setAttribute('data-act', 'toggle');
  t.setAttribute('aria-expanded', 'false'); t.setAttribute('aria-controls', 'mg-panel');
  document.body.appendChild(t);

  var p = document.createElement('aside');
  p.id = 'mg-panel'; p.className = 'mg-panel'; p.setAttribute('aria-label', 'Margin notes');
  p.innerHTML = '<div class="mg-scroll" id="mg-scroll"></div><div class="mg-foot" id="mg-foot"></div>';
  document.body.appendChild(p);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && S.open) { S.open = false; render(); }
  });
}
function openPanel() { S.open = true; }
function closePanel() { S.open = false; }

/* ==================== block marks ==================== */
function renderBadges() {
  var counts = {};
  allNotes().forEach(function (n) {
    if (n.deleted) return;
    var a = resolveAnchor(n);
    var m = counts[a] || (counts[a] = { n: 0, instr: false });
    m.n++; if (n.instr) m.instr = true;
  });
  blocks.forEach(function (el, i) {
    var m = counts[i + 1], el2 = el.querySelector('.mg-mark');
    if (m) {
      el.classList.add('mg-has');
      if (!el2) {
        el2 = document.createElement('span');
        el2.className = 'mg-mark'; el2.setAttribute('aria-hidden', 'true');
        el.appendChild(el2);
      }
      el2.innerHTML = (m.instr ? '<i class="mg-tick"></i>' : '') + m.n;
    } else {
      el.classList.remove('mg-has');
      if (el2) el2.remove();
    }
    el.classList.toggle('mg-sel', S.anchor === i + 1);
  });
}

/* ==================== panel rendering ==================== */
var raf = 0, lastCtx = '';
function schedule() { if (!raf) raf = requestAnimationFrame(function () { raf = 0; render(); }); }
function render() {
  var ae = document.activeElement, fid = ae && ae.id, s0 = null, s1 = null;
  try { if (ae && typeof ae.selectionStart === 'number') { s0 = ae.selectionStart; s1 = ae.selectionEnd; } } catch (e) {}
  var sc = $('mg-scroll'), st = sc ? sc.scrollTop : 0;
  var ctx = [S.view, S.anchor, S.person, S.open].join('|'), keep = ctx === lastCtx;
  lastCtx = ctx;

  renderBadges();
  var toggle = $('mg-toggle');
  var count = allNotes().filter(function (n) { return !n.deleted; }).length;
  toggle.innerHTML = 'Margin' + (count ? '<span class="mg-count">' + count + '</span>' : '');
  toggle.setAttribute('aria-expanded', String(S.open));

  var panel = $('mg-panel');
  panel.classList.toggle('mg-open', S.open);

  if (S.view === 'dash') renderDash();
  else renderRead();
  renderFoot();

  if (keep && sc) sc.scrollTop = st;
  if (fid) {
    var el = $(fid);
    if (el) { el.focus({ preventScroll: true }); if (s0 !== null) try { el.setSelectionRange(s0, s1); } catch (e) {} }
  }
}

function kindTag(k) { return KIND[k] ? '<span class="mg-kind mg-k-' + k + '">' + esc(KIND[k].label) + '</span>' : ''; }

function noteHTML(n, replies) {
  var who = n.instr && !n.author
    ? '<span class="mg-who mg-instr">Instructor</span>'
    : '<span class="mg-who">' + esc(nameOf(n.author)) + '</span>' + (n.instr ? '<span class="mg-badge">Instructor</span>' : '');
  var confirm = S.confirmDel === n.id;
  var acts = n.deleted ? '' : '<div class="mg-acts">' +
    (!n.parent && S.me.canWrite && S.mode !== 'loading' ? '<button data-act="reply" data-id="' + esc(n.id) + '" id="mg-rp-' + esc(n.id) + '">Reply</button>' : '') +
    (canDelete(n) ? (confirm
      ? '<span>Delete this note?</span><button class="mg-danger" data-act="del-yes" data-id="' + esc(n.id) + '" id="mg-dy">Delete</button><button data-act="del-no" id="mg-dn">Keep</button>'
      : '<button data-act="del" data-id="' + esc(n.id) + '" id="mg-dl-' + esc(n.id) + '">Delete</button>') : '') +
    '</div>';
  var replyBox = S.replyTo === n.id ? '<div class="mg-composer">' +
    '<textarea id="mg-reply-draft" rows="2" placeholder="Reply to this note" aria-label="Reply">' + esc(S.replyDraft) + '</textarea>' +
    '<div class="mg-row"><button class="mg-primary" data-act="post-reply" data-id="' + esc(n.id) + '" id="mg-post-reply">Post reply</button>' +
    '<button class="mg-textbtn" data-act="cancel-reply" id="mg-cancel-reply">Cancel</button></div></div>' : '';
  return '<article class="mg-note">' +
    '<div class="mg-meta">' + who + (n.parent ? '' : kindTag(n.kind)) + '<span class="mg-when">' + fmtDate(n.at) + '</span></div>' +
    (n.quote ? '<p class="mg-quote">&ldquo;' + esc(n.quote) + '&rdquo;</p>' : '') +
    '<p class="mg-body' + (n.deleted ? ' mg-gone' : '') + '">' + (n.deleted ? 'This note was deleted.' : esc(n.body)) + '</p>' +
    acts +
    (replies && replies.length ? '<div class="mg-replies">' + replies.map(function (r) { return noteHTML(r); }).join('') + '</div>' : '') +
    replyBox +
    '</article>';
}

function threadsFor(anchor) {
  var notes = allNotes().filter(function (n) { return resolveAnchor(n) === anchor; });
  var replies = {};
  notes.filter(function (n) { return n.parent; }).sort(byTime).forEach(function (r) {
    if (!r.deleted) (replies[r.parent] = replies[r.parent] || []).push(r);
  });
  var roots = notes.filter(function (n) { return !n.parent && !(n.deleted && !replies[n.id]); })
    .sort(function (a, b) { return (b.instr - a.instr) || byTime(a, b); });
  return { roots: roots, replies: replies };
}

function progressHTML() {
  if (S.me.instructor || !S.settings.required || S.mode === 'loading') return '';
  var req = S.settings.required;
  var mine = Object.keys(S.mine.notes).map(function (k) { return S.mine.notes[k]; })
    .filter(function (n) { return n.doc === DOC_ID && !n.parent && !n.deleted && S.settings.counts.indexOf(n.kind) !== -1; }).length;
  var cells = '';
  for (var i = 0; i < req; i++) cells += '<i class="' + (i < mine ? 'on' : '') + '"></i>';
  return '<div class="mg-progress"><span>Your notes on this text: <b>' + Math.min(mine, req) + ' of ' + req + '</b>' +
    (mine >= req ? ' · requirement met' : '') + '</span><div class="mg-meter" aria-hidden="true">' + cells + '</div></div>';
}

function composerHTML() {
  if (S.mode === 'loading') return '<p class="mg-ro">Opening the margin&hellip;</p>';
  if (!S.me.canWrite) return '<p class="mg-ro">You can read this margin. Your access to the page does not include writing in it.</p>' + (S.msg ? '<p class="mg-msg">' + esc(S.msg) + '</p>' : '');
  var k = KIND[S.kind];
  var nameRow = '';
  if (!myNameKnown()) {
    nameRow = '<input type="text" id="mg-name" maxlength="40" placeholder="Your name for the margin (shown on your notes)" aria-label="Display name">';
  }
  return '<div class="mg-composer">' +
    '<div class="mg-kinds" role="radiogroup" aria-label="Kind of note">' +
      KINDS.map(function (x) {
        return '<button class="mg-kbtn" role="radio" aria-checked="' + (S.kind === x.id) + '" data-act="kind" data-kind="' + x.id + '" id="mg-kind-' + x.id + '">' + esc(x.label) + '</button>';
      }).join('') +
    '</div>' +
    '<p class="mg-hint">' + esc(k.hint) + '</p>' +
    (S.quote ? '<div class="mg-qchip">On the words <span>&ldquo;' + esc(S.quote) + '&rdquo;</span><button class="mg-textbtn" data-act="clear-quote" id="mg-clear-quote">Whole passage</button></div>' : '') +
    nameRow +
    '<textarea id="mg-draft" rows="4" placeholder="Write in the margin" aria-label="Your note">' + esc(S.draft) + '</textarea>' +
    '<div class="mg-row"><button class="mg-primary" data-act="post" id="mg-post">Post to the margin</button>' +
      (S.me.instructor ? '<span class="mg-hint">Posts as instructor</span>' : '') + '</div>' +
    (S.msg ? '<p class="mg-msg">' + esc(S.msg) + '</p>' : '') +
    '</div>';
}

function renderRead() {
  var sc = $('mg-scroll');
  var title = (document.querySelector('.page-header h2') || {}).textContent || document.title;

  if (S.anchor) {
    var t = threadsFor(S.anchor);
    var el = blockAt(S.anchor);
    var txt = el ? norm(el.textContent).slice(0, 300) : '(passage moved)';
    sc.innerHTML =
      '<div class="mg-top"><p class="mg-title">Margin · passage ' + S.anchor + '</p>' +
      '<span><button class="mg-textbtn" data-act="close-anchor" id="mg-close-anchor">All notes</button> ' +
      '<button class="mg-x" data-act="toggle" aria-label="Close margin">&times;</button></span></div>' +
      '<p class="mg-target"><small>' + esc(title) + ', passage ' + S.anchor + '</small>' + esc(txt) + '</p>' +
      '<div>' + (t.roots.length ? t.roots.map(function (r) { return noteHTML(r, t.replies[r.id]); }).join('')
        : '<p class="mg-empty">No one has written beside this passage yet.</p>') + '</div>' +
      composerHTML();
    return;
  }

  var notes = allNotes().filter(function (n) { return !n.deleted; });
  var roots = notes.filter(function (n) { return !n.parent; });
  var readers = {};
  notes.forEach(function (n) { readers[n.author || 'instr'] = 1; });
  var nReaders = Object.keys(readers).length;
  var kindCounts = {};
  roots.forEach(function (n) { kindCounts[n.kind] = (kindCounts[n.kind] || 0) + 1; });
  var shown = roots.filter(function (n) { return S.filter === 'all' || n.kind === S.filter; });
  var anchors = [];
  shown.forEach(function (n) { var a = resolveAnchor(n); if (anchors.indexOf(a) === -1) anchors.push(a); });
  anchors.sort(function (a, b) { return a - b; });

  sc.innerHTML =
    '<div class="mg-top"><p class="mg-title">The margin</p>' +
    '<span>' + (S.me.instructor ? '<button class="mg-textbtn" data-act="dash" id="mg-dash">Class view</button> ' : '') +
    '<button class="mg-x" data-act="toggle" aria-label="Close margin">&times;</button></span></div>' +
    '<p class="mg-lede">' + (S.mode === 'loading' ? 'Opening the margin&hellip;' : notes.length
      ? plural(notes.length, 'note') + ' on this text from ' + plural(nReaders, 'reader') + '. Select a passage to join in.'
      : 'No notes on this text yet. Select a passage to write the first one.') + '</p>' +
    progressHTML() +
    (roots.length ? '<div class="mg-chips" role="group" aria-label="Show kinds">' +
      '<button class="mg-chip" aria-pressed="' + (S.filter === 'all') + '" data-act="filter" data-kind="all">All ' + roots.length + '</button>' +
      KINDS.filter(function (k) { return kindCounts[k.id]; }).map(function (k) {
        return '<button class="mg-chip" aria-pressed="' + (S.filter === k.id) + '" data-act="filter" data-kind="' + k.id + '">' + esc(k.label) + ' ' + kindCounts[k.id] + '</button>';
      }).join('') + '</div>' : '') +
    '<div>' + anchors.map(function (a) {
      var here = shown.filter(function (n) { return resolveAnchor(n) === a; })
        .sort(function (x, y) { return (y.instr - x.instr) || byTime(x, y); });
      var replyCount = notes.filter(function (n) { return n.parent && resolveAnchor(n) === a; }).length;
      var first = here[0];
      var txt = blockAt(a) ? norm(blockAt(a).textContent).slice(0, 90) : '(moved)';
      return '<button class="mg-ov" data-act="anchor" data-anchor="' + a + '" id="mg-ov-' + a + '">' +
        '<span class="mg-ov-ln">Passage ' + a + '</span>' +
        '<span class="mg-ov-txt">' + esc(txt) + (blockAt(a) && norm(blockAt(a).textContent).length > 90 ? '&hellip;' : '') + '</span>' +
        '<span class="mg-ov-meta">' +
          here.map(function (n) { return n.kind; }).filter(function (v, i, arr) { return arr.indexOf(v) === i; }).map(kindTag).join('') +
          '<span>' + plural(here.length, 'note') + (replyCount ? ', ' + plural(replyCount, 'reply').replace('replys', 'replies') : '') + '</span></span>' +
        '<span class="mg-ov-prev">' + esc(first.instr && !first.author ? 'Instructor' : nameOf(first.author)) + ': ' +
          esc(first.body.length > 110 ? first.body.slice(0, 110) + '…' : first.body) + '</span>' +
        '</button>';
    }).join('') + '</div>';
}

/* ---------- class view ---------- */
function statsFor(uid, d) {
  var notes = Object.keys(d.notes).map(function (k) { return d.notes[k]; })
    .filter(function (n) { return !n.deleted && n.doc === DOC_ID; });
  var roots = notes.filter(function (n) { return !n.parent; });
  var counted = roots.filter(function (n) { return S.settings.counts.indexOf(n.kind) !== -1; }).length;
  var kinds = {};
  roots.forEach(function (n) { kinds[n.kind] = (kinds[n.kind] || 0) + 1; });
  var secs = d.reading[DOC_ID] || 0;
  var last = notes.map(function (n) { return n.at; }).sort().pop() || '';
  return { uid: uid, counted: counted, replies: notes.length - roots.length, kinds: kinds, secs: secs, last: last, req: S.settings.required };
}
function renderDash() {
  var sc = $('mg-scroll');
  var p = people(), rows = [];
  for (var uid in p) { if (S.mode === 'shared' && uid === S.me.id) continue; rows.push(statsFor(uid, p[uid])); }
  rows.sort(function (a, b) { return b.secs - a.secs; });
  var maxS = Math.max(60, Math.max.apply(null, rows.map(function (r) { return r.secs; }).concat([60])));
  var secs = rows.map(function (r) { return r.secs; }).sort(function (a, b) { return a - b; });
  var median = secs.length ? (secs.length % 2 ? secs[(secs.length - 1) / 2] : (secs[secs.length / 2 - 1] + secs[secs.length / 2]) / 2) : 0;
  var short = rows.filter(function (r) { return r.req && r.counted < r.req; }).length;

  if (S.person) {
    var d = p[S.person] || { notes: {}, reading: {} };
    var ns = Object.keys(d.notes).map(function (k) { return Object.assign({ id: k, author: S.person, instr: false }, d.notes[k]); })
      .filter(function (n) { return !n.deleted && n.doc === DOC_ID; }).sort(byTime).reverse();
    sc.innerHTML =
      '<div class="mg-top"><p class="mg-title">Reader</p>' +
      '<span><button class="mg-textbtn" data-act="person-back" id="mg-person-back">Requirements</button> ' +
      '<button class="mg-x" data-act="toggle" aria-label="Close margin">&times;</button></span></div>' +
      '<h2 style="font-family:\'Libre Baskerville\',Georgia,serif;font-weight:400;font-size:1.3rem;margin:0 0 8px">' + esc(nameOf(S.person)) + '</h2>' +
      '<dl class="mg-facts"><dt>Active reading on this text</dt><dd>' + fmtMin((d.reading[DOC_ID] || 0)) + '</dd></dl>' +
      '<div>' + (ns.length ? ns.map(function (n) {
        return '<article class="mg-note">' +
          '<div class="mg-meta">' + (n.parent ? '<span style="color:#5a6374">Reply</span>' : kindTag(n.kind)) + '<span class="mg-when">' + fmtDate(n.at) + '</span></div>' +
          (n.quote ? '<p class="mg-quote">&ldquo;' + esc(n.quote) + '&rdquo;</p>' : '') +
          '<p class="mg-body">' + esc(n.body) + '</p>' +
          '<div class="mg-acts"><button data-act="goto" data-anchor="' + resolveAnchor(n) + '" id="mg-go-' + esc(n.id) + '">Passage ' + resolveAnchor(n) + '</button></div>' +
          '</article>';
      }).join('') : '<p class="mg-empty">No notes yet.</p>') + '</div>';
    return;
  }

  var sd = S.sd || S.settings;
  sc.innerHTML =
    '<div class="mg-top"><p class="mg-title">Class view · this text</p>' +
    '<span><button class="mg-textbtn" data-act="read-view" id="mg-read-view">The margin</button> ' +
    '<button class="mg-x" data-act="toggle" aria-label="Close margin">&times;</button></span></div>' +
    '<p class="mg-lede">' + rows.length + ' ' + (rows.length === 1 ? 'reader' : 'readers') + ' · ' +
      rows.reduce(function (a, r) { return a + r.counted; }, 0) + ' notes that count · median ' + fmtMin(median) + ' active · ' +
      short + ' short of the requirement</p>' +
    (rows.length ? '<div>' + rows.map(function (r) {
      var met = r.counted >= r.req;
      return '<div class="mg-dash-row">' +
        '<button class="mg-dash-name" data-act="person" data-uid="' + esc(r.uid) + '">' + esc(nameOf(r.uid)) + '</button>' +
        '<span class="mg-pill ' + (met ? 'mg-ok' : 'mg-short') + '">' + (met ? 'Met' : (r.req - r.counted) + ' short') + '</span><br>' +
        '<span class="mg-bar"><span style="width:' + Math.round(r.secs / maxS * 100) + '%"></span></span>' + fmtMin(r.secs) +
        ' · ' + r.counted + '/' + r.req + ' notes · ' + r.replies + ' replies' +
        (r.last ? ' · last ' + fmtDate(r.last) : '') + '<br>' +
        '<span class="mg-ov-meta">' + Object.keys(r.kinds).map(kindTag).join('') + '</span>' +
        '</div>';
    }).join('') + '</div>'
    : '<p class="mg-empty">No students have opened this text yet. They appear here once they start reading.</p>') +
    '<div class="mg-section"><h3>Notes required per text</h3>' +
      '<label class="mg-check" for="mg-req"><input type="number" id="mg-req" min="0" max="20" value="' + sd.required + '"> per text</label>' +
      '<fieldset style="border:0;padding:0;margin:0;display:flex;flex-direction:column;gap:6px"><legend style="font-size:12.5px;font-weight:700;margin-bottom:4px;padding:0">Kinds that count toward it</legend>' +
        KINDS.map(function (k) {
          return '<label class="mg-check"><input type="checkbox" id="mg-cnt-' + k.id + '" data-kind="' + k.id + '"' + (sd.counts.indexOf(k.id) !== -1 ? ' checked' : '') + '>' + esc(k.label) + '</label>';
        }).join('') + '</fieldset>' +
      '<div class="mg-row"><button class="mg-primary" data-act="save-settings" id="mg-save-settings"' + (S.sd ? '' : ' disabled') + '>Save requirements</button>' +
        (S.sd ? '' : '<span class="mg-hint">Saved</span>') + '</div>' +
      (S.msg ? '<p class="mg-msg">' + esc(S.msg) + '</p>' : '') + '</div>' +
    '<div class="mg-section"><h3>How active reading is measured</h3>' +
      '<p>A reader\'s clock runs in five-second steps while the text is on screen and they have scrolled, typed, clicked or moved the pointer within the last minute. Leaving the tab open in the background does not count.</p>' +
      '<p>Students see their own note count against the requirement in the margin. They do not see this page.</p></div>';
}

function renderFoot() {
  var f = $('mg-foot');
  var status = S.mode === 'shared' ? 'Shared with everyone who opens this page.'
    : S.mode === 'local' ? 'Preview mode: notes are saved in this browser only.'
    : 'Opening the margin…';
  f.innerHTML = '<span>' + status + '</span>' +
    (S.mode === 'local' ? '<span class="mg-seg" role="group" aria-label="View as">' +
      '<button data-act="role" data-role="student" aria-pressed="' + !S.me.instructor + '">Student</button>' +
      '<button data-act="role" data-role="instructor" aria-pressed="' + S.me.instructor + '">Instructor</button></span>' : '');
}

/* ==================== interaction ==================== */
function selectAnchor(n, el) {
  var q = '';
  var sel = getSelection();
  if (el && el.classList && el.classList.contains('mg-block') && sel && !sel.isCollapsed) {
    var box = function (node) {
      if (!node) return null;
      var e = node.nodeType === 1 ? node : node.parentElement;
      return e && e.closest ? e.closest('.mg-block') : null;
    };
    if (box(sel.anchorNode) === el && box(sel.focusNode) === el) q = norm(sel.toString()).slice(0, 200);
  }
  if (S.anchor !== n) { S.replyTo = null; S.confirmDel = null; }
  S.anchor = n; S.quote = q; S.msg = '';
  openPanel(); render();
  if (el) el.scrollIntoView({ block: 'nearest' });
}

document.addEventListener('click', function (e) {
  var t = e.target.closest ? e.target.closest('[data-act]') : null;
  // clicks on annotatable blocks select them (unless they hit a link or control inside)
  var blk = e.target.closest ? e.target.closest('.mg-block') : null;
  if (!t && blk) {
    if (e.target.closest && e.target.closest('a, button, input, textarea, select')) return;
    selectAnchor(Number(blk.dataset.mga), blk);
    return;
  }
  if (!t) return;
  var a = t.dataset.act, id = t.dataset.id;
  var find = function () { return allNotes().find(function (n) { return n.id === id; }); };
  switch (a) {
    case 'toggle': S.open ? closePanel() : openPanel(); break;
    case 'anchor': selectAnchor(Number(t.dataset.anchor), blockAt(Number(t.dataset.anchor))); break;
    case 'close-anchor': S.anchor = null; S.quote = ''; S.replyTo = null; break;
    case 'dash': flushReading(); S.view = 'dash'; S.person = null; S.msg = ''; break;
    case 'read-view': S.view = 'read'; S.person = null; break;
    case 'kind': S.kind = t.dataset.kind; break;
    case 'filter': S.filter = t.dataset.kind; break;
    case 'clear-quote': S.quote = ''; break;
    case 'post': {
      var text = S.draft.trim();
      if (!text) { S.msg = 'Write something before posting.'; break; }
      if (!S.anchor) { S.msg = 'Select a passage first.'; break; }
      if (!myNameKnown()) {
        var nm = norm(($('mg-name') || {}).value || '');
        if (!nm) { S.msg = 'Add the name your notes should show.'; break; }
        S.me.name = nm; saveProfile();
      }
      var note = { doc: DOC_ID, anchor: S.anchor, kind: S.kind, body: text, at: new Date().toISOString() };
      if (S.quote) note.quote = S.quote;
      S.msg = ''; addNote(note); S.draft = ''; S.quote = '';
      break;
    }
    case 'reply': S.replyTo = id; S.replyDraft = ''; render(); var rd = $('mg-reply-draft'); if (rd) rd.focus(); return;
    case 'cancel-reply': S.replyTo = null; break;
    case 'post-reply': {
      var rtext = S.replyDraft.trim(), parent = find();
      if (!rtext || !parent) break;
      if (!myNameKnown()) {
        var nm2 = norm(($('mg-name') || {}).value || '');
        if (nm2) { S.me.name = nm2; saveProfile(); }
      }
      addNote({ doc: DOC_ID, anchor: parent.anchor, parent: parent.id, body: rtext, at: new Date().toISOString() });
      S.replyTo = null; S.replyDraft = '';
      break;
    }
    case 'del': S.confirmDel = id; break;
    case 'del-no': S.confirmDel = null; break;
    case 'del-yes': { var n = find(); if (n) deleteNote(n); S.confirmDel = null; break; }
    case 'role': S.me.instructor = t.dataset.role === 'instructor'; if (!S.me.instructor) S.view = 'read'; saveLocal(); break;
    case 'person': S.person = t.dataset.uid; break;
    case 'person-back': S.person = null; break;
    case 'goto': S.view = 'read'; var ga = Number(t.dataset.anchor); selectAnchor(ga, blockAt(ga)); break;
    case 'save-settings': if (S.sd) { S.settings = Object.assign({}, S.sd); S.sd = null; saveSettings(); } break;
  }
  render();
});

document.addEventListener('keydown', function (e) {
  var t = e.target;
  if (t && t.classList && t.classList.contains('mg-block') && (e.key === 'Enter' || e.key === ' ')) {
    e.preventDefault(); selectAnchor(Number(t.dataset.mga), t);
  }
  if (t && t.id === 'mg-draft' && e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
    e.preventDefault(); var b = $('mg-post'); if (b) b.click();
  }
});
document.addEventListener('input', function (e) {
  var t = e.target;
  if (t.id === 'mg-draft') S.draft = t.value;
  else if (t.id === 'mg-reply-draft') S.replyDraft = t.value;
  else if (t.id === 'mg-req' || (t.id && t.id.indexOf('mg-cnt-') === 0)) {
    var required = Math.max(0, Math.min(20, parseInt(($('mg-req') || {}).value, 10) || 0));
    var counts = KINDS.filter(function (k) { var c = $('mg-cnt-' + k.id); return c && c.checked; }).map(function (k) { return k.id; });
    S.sd = { required: required, counts: counts };
    var btn = $('mg-save-settings'); if (btn) btn.disabled = false;
  }
});

/* ==================== startup ==================== */
function loadScript(src) {
  return new Promise(function (res, rej) {
    var s = document.createElement('script');
    s.src = src; s.onload = res; s.onerror = rej;
    document.head.appendChild(s);
  });
}
function startLocal() {
  S.mode = 'local'; S.me = { id: 'local', instructor: false, canWrite: true, name: 'You' };
  try {
    var saved = JSON.parse(localStorage.getItem(LS_KEY) || 'null');
    if (saved) {
      S.mine = cleanPerson(saved.mine);
      S.guide = cleanNotes(saved.guide);
      S.settings = cleanSettings(saved.settings);
      S.me.instructor = !!saved.instructor;
      if (saved.name) S.me.name = saved.name;
    }
  } catch (e) {}
  render();
}
async function startShared() {
  var base = 'https://www.gstatic.com/firebasejs/' + FB_VERSION + '/';
  await loadScript(base + 'firebase-app-compat.js');
  await loadScript(base + 'firebase-auth-compat.js');
  await loadScript(base + 'firebase-firestore-compat.js');
  firebase.initializeApp(MARGINS_FIREBASE);
  db = firebase.firestore();
  var auth = firebase.auth();
  var cred = await auth.signInAnonymously();
  var uid = cred.user.uid;
  S.me = { id: uid, instructor: MARGINS_INSTRUCTORS.indexOf(uid) !== -1, canWrite: true, name: '' };
  myRef = db.doc('readers/' + uid);
  var snap = await myRef.get();
  S.mine = snap.exists ? cleanPerson(snap.data()) : { notes: {}, reading: {} };

  db.collection('readers').onSnapshot(function (qs) {
    var next = {};
    qs.docs.forEach(function (d) {
      if (d.id === S.me.id) {
        var w = writers.mine;
        if (!(d.metadata.hasPendingWrites || (w && (w.busy || w.dirty)))) S.mine = cleanPerson(d.data());
      } else next[d.id] = cleanPerson(d.data());
    });
    S.people = next; schedule();
  }, function () { S.msg = 'Live updates stopped. Reload the page to reconnect.'; schedule(); });
  db.doc('guide/notes').onSnapshot(function (s) {
    var w = writers.guide;
    if (!(w && (w.busy || w.dirty))) S.guide = s.exists ? cleanNotes(s.data().notes) : {};
    schedule();
  }, function () {});
  db.doc('guide/settings').onSnapshot(function (s) {
    var w = writers.settings;
    if (!(w && (w.busy || w.dirty))) S.settings = s.exists ? cleanSettings(s.data()) : { required: DEFAULT_SETTINGS.required, counts: DEFAULT_SETTINGS.counts.slice() };
    schedule();
  }, function () {});
  db.collection('profiles').onSnapshot(function (qs) {
    var changed = false;
    qs.docs.forEach(function (d) {
      var nm = d.data() && d.data().name ? String(d.data().name).slice(0, 40) : '';
      if (d.id === S.me.id) { if (nm && S.me.name !== nm) { S.me.name = nm; changed = true; } }
      else if (S.names[d.id] !== nm) { S.names[d.id] = nm; changed = true; }
    });
    if (changed) schedule();
  }, function () {});

  S.mode = 'shared';
  render();
}
function start() {
  injectStyle(); injectShell(); scanBlocks(); render();
  if (MARGINS_FIREBASE.apiKey.indexOf('PASTE_') === 0 || typeof Promise === 'undefined') { startLocal(); return; }
  startShared().catch(function () { startLocal(); });
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
else start();

})();

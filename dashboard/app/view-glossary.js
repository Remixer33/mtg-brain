/* ============================================================================
   REMY'S LAIR — app/view-glossary.js
   VIEW: "Glossary" (#/glossary, #/glossary/<term>) — the official terms, plus
   Omar's beginner glossary.

   What this view is FOR: 735 official glossary entries, each of which points at
   the Comprehensive Rules — and those pointers are dead text in the CLI. Here
   every "see rule 601.2b" inside a definition is a real link into the Rules
   view, checked against the rules index before it is drawn (the linker lives in
   view-rules.js and is borrowed through window.RLRules). Alongside it sits
   Omar's own hand-written working glossary from learning/GLOSSARY.md.

   Constraints honoured:
     C1  zero LLM spend  — pure rendering of data/rules.js (glossary + doc).
     C2  never invent    — definitions and the doc are inserted verbatim; the only
                           thing layered on is <a> around a rule reference that
                           EXISTS in the index. If the rules linker is absent, the
                           text degrades to plain, not to a broken link.
     C5  offline-first   — no fetch, no CDN.
     C6/no-build         — plain ES2019-ish script.
     C3  Commander only  — no other format is named anywhere in this file.
   ========================================================================== */
(function (window, document) {
  'use strict';

  var RL = window.RL;
  if (!RL) return;

  RL.icons.az = '<path d="M4 16.5 7 8l3 8.5"/><path d="M5 14h4"/>' +
                '<path d="M14 8.5h5l-5 8h5"/>';

  function rules() { return window.RLRules || null; }

  /* Linkify rule references inside a text string. Uses the verified linker from
     view-rules.js if present; otherwise a plain text node (honest fallback). */
  function withRefs(text) {
    var R = rules();
    if (R && R.linkify) return R.linkify(text);
    return document.createTextNode(text || '');
  }

  /* ==========================================================================
     1. INDEX
     ====================================================================== */
  var idx = null;
  function buildIndex() {
    if (idx) return idx;
    var payload = RL.data('rules');
    if (!payload) return null;
    var terms = (payload.glossary || []).map(function (row, i) {
      return { term: String(row[0]), def: String(row[1] == null ? '' : row[1]), i: i };
    });
    terms.sort(function (a, b) { return a.term.localeCompare(b.term); });
    var lower = terms.map(function (t) { return (t.term + ' ' + t.def).toLowerCase(); });
    idx = { terms: terms, lower: lower, doc: (payload.docs && payload.docs.glossary) || null };
    return idx;
  }

  function search(query) {
    var i = buildIndex();
    var raw = String(query || '').trim().toLowerCase();
    if (!i) return { hits: [], terms: [] };
    if (!raw) return { hits: i.terms.slice(), terms: [] };
    var words = raw.split(/\s+/).filter(function (w) { return w.length >= 2; });
    if (!words.length) return { hits: i.terms.slice(), terms: [] };
    var hits = [];
    for (var k = 0; k < i.terms.length; k++) {
      var hay = i.lower[k], ok = true;
      for (var w = 0; w < words.length; w++) { if (hay.indexOf(words[w]) === -1) { ok = false; break; } }
      if (ok) hits.push(i.terms[k]);
    }
    return { hits: hits, terms: words };
  }

  /* ==========================================================================
     2. STATE + RENDER
     ====================================================================== */
  var dom = null, selectedTerm = null, mode = 'terms';

  function termHref(term) { return RL.href('glossary', term); }

  function renderList(res) {
    var host = dom.list;
    RL.clear(host);
    dom.count.textContent = res.terms.length
      ? RL.fmt.plural(res.hits.length, 'match', 'matches')
      : RL.fmt.plural(res.hits.length, 'term');
    if (!res.hits.length) {
      host.appendChild(RL.el('p', { class: 'gloss__empty', text: 'No glossary term matches that.' }));
      return;
    }
    var ul = RL.el('ul', { class: 'gloss__terms' });
    res.hits.forEach(function (t) {
      var a = RL.el('a', {
        class: ['gloss__term', selectedTerm === t.term ? 'is-selected' : ''],
        href: termHref(t.term), 'data-term': t.term
      },
        RL.el('span', { class: 'gloss__termname', text: t.term }),
        RL.svgIcon('chevron-right', 16));
      if (res.terms.length) highlight(a.querySelector('.gloss__termname'), res.terms);
      ul.appendChild(RL.el('li', null, a));
    });
    host.appendChild(ul);
  }

  function highlight(node, terms) {
    var R = rules();
    if (R && R.highlight) R.highlight(node, terms);
  }

  function renderDetail(term) {
    var host = dom.detail;
    RL.clear(host);
    var i = buildIndex();
    if (!term || !i) { host.appendChild(detailPlaceholder()); return; }

    var entry = null;
    for (var k = 0; k < i.terms.length; k++) {
      if (i.terms[k].term.toLowerCase() === String(term).toLowerCase()) { entry = i.terms[k]; break; }
    }
    if (!entry) {
      host.appendChild(RL.el('div', { class: 'panel state' },
        RL.el('div', { class: 'state__icon' }, RL.svgIcon('alert-triangle', 28)),
        RL.el('h2', { class: 'state__title', text: 'not in my data: glossary ‘' + term + '’' }),
        RL.el('p', { class: 'state__body', text: 'There is no glossary entry with that exact name.' })));
      return;
    }

    var def = RL.el('div', { class: 'glossdetail__def' });
    def.appendChild(withRefs(entry.def));

    host.appendChild(RL.el('article', { class: 'panel glossdetail' },
      RL.el('h2', { class: 'glossdetail__term', text: entry.term }),
      def,
      RL.el('p', { class: 'glossdetail__cli mono' },
        RL.svgIcon('terminal', 14),
        RL.el('span', { text: './bin/mtg glossary "' + entry.term + '"' }))));
  }

  function detailPlaceholder() {
    return RL.el('div', { class: 'gloss__placeholder' },
      RL.svgIcon('bookmark', 28),
      RL.el('p', { text: 'Pick a term to read its official definition. Rule references inside it are links.' }));
  }

  /* ---- Omar's beginner glossary (learning/GLOSSARY.md) ------------------ */
  function renderDoc(host) {
    RL.clear(host);
    var i = buildIndex();
    if (!i || !i.doc) {
      host.appendChild(RL.el('div', { class: 'panel state' },
        RL.el('div', { class: 'state__icon' }, RL.svgIcon('bookmark', 28)),
        RL.el('h2', { class: 'state__title', text: 'No beginner glossary yet' }),
        RL.el('p', { class: 'state__body' },
          RL.el('code', { class: 'md-code', text: 'learning/GLOSSARY.md' }),
          ' is not in this build. It is the hand-written, Commander-facing glossary.')));
      return;
    }
    var md = RL.mdEl(i.doc);
    var R = rules();
    if (R && R.linkifyElement) R.linkifyElement(md); // turn rule refs into links
    host.appendChild(RL.el('article', { class: 'panel glossdoc' },
      RL.el('p', { class: 'docmeta', text: 'From learning/GLOSSARY.md — Omar’s own working glossary, verbatim.' }),
      md));
  }

  /* ==========================================================================
     3. MOUNT
     ====================================================================== */
  var timer = null;
  function schedule() { window.clearTimeout(timer); timer = window.setTimeout(runSearch, 130); }
  function runSearch() { if (dom) renderList(search(dom.input.value)); }

  function setMode(next) {
    mode = next;
    dom.tabTerms.setAttribute('aria-selected', String(mode === 'terms'));
    dom.tabDoc.setAttribute('aria-selected', String(mode === 'doc'));
    dom.termsPane.hidden = mode !== 'terms';
    dom.docPane.hidden = mode !== 'doc';
    if (mode === 'doc' && !dom.docPane.dataset.built) {
      renderDoc(dom.docPane); dom.docPane.dataset.built = '1';
    }
  }

  var keyHandler = null;

  function mount(el) {
    var i = buildIndex();
    if (!i || !i.terms.length) {
      el.appendChild(RL.el('div', { class: 'panel state' },
        RL.el('div', { class: 'state__icon' }, RL.svgIcon('bookmark', 28)),
        RL.el('h2', { class: 'state__title', text: 'The glossary has not been built' }),
        RL.el('p', { class: 'state__body' },
          RL.el('code', { class: 'md-code', text: 'dashboard/data/rules.js' }),
          ' did not register a glossary. Run ',
          RL.el('code', { class: 'md-code', text: './bin/mtg dashboard --build' }), ' and reload.')));
      return;
    }

    el.appendChild(RL.el('h1', { class: 'section-title', text: 'Glossary' }));
    el.appendChild(RL.el('p', { class: 'section-sub' },
      RL.fmt.int(i.terms.length) + ' official glossary terms, each linked into the rules it cites' +
      (i.doc ? ', plus Omar’s own beginner glossary.' : '.')));

    // tabs
    var tabTerms = RL.el('button', { class: 'doctab', type: 'button', role: 'tab', 'aria-selected': 'true',
      on: { click: function () { setMode('terms'); } } },
      RL.el('span', { text: 'Official terms' }));
    var tabDoc = RL.el('button', { class: 'doctab', type: 'button', role: 'tab', 'aria-selected': 'false',
      on: { click: function () { setMode('doc'); } } },
      RL.el('span', { text: 'Beginner’s glossary' }));
    if (!i.doc) tabDoc.disabled = true;
    el.appendChild(RL.el('div', { class: 'doctabs', role: 'tablist', 'aria-label': 'Glossary source' },
      tabTerms, tabDoc));

    // terms pane: search + list + detail
    var input = RL.el('input', { class: 'input', type: 'search', id: 'gloss-search',
      placeholder: 'Search 735 terms…', autocomplete: 'off', spellcheck: 'false',
      on: { input: schedule, keydown: function (e) {
        if (e.key === 'Escape' && input.value) { e.preventDefault(); input.value = ''; runSearch(); }
        else if (e.key === 'Enter') {
          e.preventDefault();
          var res = search(input.value);
          if (res.hits.length) RL.navigate('glossary', res.hits[0].term);
        }
      } } });
    var clear = RL.el('button', { class: 'icon-btn', type: 'button', aria: { label: 'Clear the search' },
      on: { click: function () { input.value = ''; runSearch(); input.focus(); } } }, RL.svgIcon('x', 18));
    var count = RL.el('p', { class: 'cardsearch__count', role: 'status', 'aria-live': 'polite' });
    var list = RL.el('div', { class: 'gloss__list' });
    var detail = RL.el('div', { class: 'gloss__detail' });

    var termsPane = RL.el('div', { class: 'gloss' },
      RL.el('aside', { class: 'gloss__left' },
        RL.el('div', { class: 'rsearch__field cards__field' }, RL.svgIcon('search', 18), input, clear),
        count, list),
      RL.el('div', { class: 'gloss__right' }, detail));

    var docPane = RL.el('div', { hidden: true });

    el.appendChild(termsPane);
    el.appendChild(docPane);

    dom = { input: input, count: count, list: list, detail: detail,
            tabTerms: tabTerms, tabDoc: tabDoc, termsPane: termsPane, docPane: docPane };

    runSearch();
    renderDetail(null);
  }

  function select(term) {
    selectedTerm = term || null;
    renderDetail(selectedTerm);
    if (dom && dom.list) {
      Array.prototype.forEach.call(dom.list.querySelectorAll('.gloss__term'), function (a) {
        if (a.getAttribute('data-term') === term) a.classList.add('is-selected');
        else a.classList.remove('is-selected');
      });
      var active = dom.list.querySelector('.gloss__term.is-selected');
      if (active && active.scrollIntoView) active.scrollIntoView({ block: 'nearest' });
    }
  }

  RL.registerView({
    id: 'glossary', label: 'Glossary', icon: 'bookmark', mount: mount,
    onEnter: function (params) {
      if (!dom) return;
      if (params[0]) { if (mode !== 'terms') setMode('terms'); select(params[0]); }
      else select(null);
      if (!keyHandler) {
        keyHandler = function (e) {
          if (e.key !== '/' || e.metaKey || e.ctrlKey || e.altKey) return;
          var t = e.target;
          if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable)) return;
          e.preventDefault(); if (mode === 'terms') { dom.input.focus(); dom.input.select(); }
        };
        document.addEventListener('keydown', keyHandler);
      }
    },
    onLeave: function () {
      if (keyHandler) { document.removeEventListener('keydown', keyHandler); keyHandler = null; }
    }
  });

})(window, document);

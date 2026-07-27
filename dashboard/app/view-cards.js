/* ============================================================================
   REMY'S LAIR — app/view-cards.js
   VIEW: "Cards" (#/cards, #/cards/<query>) — search all 38,351 cards.

   What this view is FOR: it is the browser twin of `mtg search`. The same query
   language — t: c:/id: cmc<=N rarity: legal:commander is:<type> deck:<slug> plus
   free text — runs here, client-side, over the card payload that is loaded ONCE,
   lazily, the first time you open this section (it is ~9.6MB in a real build, so
   it must never be paid for on first paint).

   Constraints honoured:
     C1  zero LLM spend  — pure filtering + rendering. No inference.
     C2  never invent    — every field shown is read from the row the exporter
                           wrote; oracle text is inserted verbatim as a text node.
                           cards.js carries no art or rulings, so this view shows
                           neither — it does not fabricate a picture it lacks.
     C5  offline-first   — the payload arrives via RL.loadLazy injecting one more
                           <script>, never fetch(). Nothing else is loaded.
     C6/no-build         — plain ES2019-ish script.
     C3  Commander only  — legality is legal:commander; no other format is named.
   ========================================================================== */
(function (window, document) {
  'use strict';

  var RL = window.RL;
  if (!RL) return;

  var COL = { name: 0, mana_cost: 1, type_line: 2, cmc: 3, color_identity: 4,
              rarity: 5, edhrec_rank: 6, oracle_text: 7, price_usd: 8, pt: 9,
              legal_commander: 10 };
  var COLOR_LETTERS = { w: 1, u: 1, b: 1, r: 1, g: 1, c: 1 };
  var MAX_RESULTS = 120;

  /* ==========================================================================
     1. QUERY LANGUAGE  (a small, honest subset of `mtg search`)
     ====================================================================== */
  function tokenize(query) {
    var out = [], re = /"([^"]*)"|(\S+)/g, m;
    while ((m = re.exec(query)) !== null) out.push(m[1] !== undefined ? m[1] : m[2]);
    return out;
  }

  var CMP = {
    '<=': function (a, b) { return a <= b; }, '>=': function (a, b) { return a >= b; },
    '<': function (a, b) { return a < b; }, '>': function (a, b) { return a > b; },
    '=': function (a, b) { return a === b; }, ':': function (a, b) { return a === b; }
  };

  /* -> {preds:[fn(row)->bool], terms:[string], note:string|null} */
  function parseQuery(query) {
    var preds = [], terms = [], note = null;
    tokenize(query).forEach(function (tok) {
      var lower = tok.toLowerCase();

      // field:value / field OP value  (cmc<=3, mv>=5, cmc=2)
      var mvMatch = lower.match(/^(cmc|mv|manavalue)\s*(<=|>=|<|>|=|:)\s*(\d+(?:\.\d+)?)$/);
      if (mvMatch) {
        var op = CMP[mvMatch[2]] || CMP['='], val = parseFloat(mvMatch[3]);
        preds.push(function (r) { return op(r[COL.cmc], val); });
        return;
      }

      var kv = tok.match(/^([a-z]+):(.*)$/i);
      if (kv) {
        var key = kv[1].toLowerCase(), value = kv[2];
        var vlow = value.toLowerCase();
        if (key === 't' || key === 'type') {
          preds.push(function (r) { return (r[COL.type_line] || '').toLowerCase().indexOf(vlow) >= 0; });
          return;
        }
        if (key === 'is') {
          preds.push(function (r) { return (r[COL.type_line] || '').toLowerCase().indexOf(vlow) >= 0; });
          return;
        }
        if (key === 'c' || key === 'color' || key === 'id' || key === 'identity') {
          var want = vlow.split('').filter(function (ch) { return COLOR_LETTERS[ch]; });
          // subset semantics: the card fits a deck of the named identity
          preds.push(function (r) {
            var ci = (r[COL.color_identity] || []).map(function (x) { return x.toLowerCase(); });
            if (!want.length) return ci.length === 0; // c: (empty) -> colourless
            if (ci.length === 0) return true; // colourless fits any identity
            return ci.every(function (x) { return want.indexOf(x) >= 0; });
          });
          return;
        }
        if (key === 'r' || key === 'rarity') {
          preds.push(function (r) { return (r[COL.rarity] || '').toLowerCase().indexOf(vlow) === 0; });
          return;
        }
        if (key === 'legal') {
          // Commander is the only format modelled (C3).
          preds.push(function (r) { return (r[COL.legal_commander] || '') === 'legal'; });
          if (vlow !== 'commander') note = 'Only legal:commander is modelled here — this system is Commander-only.';
          return;
        }
        if (key === 'deck') {
          var names = deckNameSet(vlow);
          if (names) preds.push(function (r) { return names[r[COL.name].toLowerCase()] === 1; });
          else note = 'deck:' + value + ' — no such deck is loaded (tidus, bumbleflower, dogmeat).';
          return;
        }
        // unknown key: fall through to a free-text match on the whole token
      }

      terms.push(lower);
    });

    if (terms.length) {
      preds.push(function (r) {
        var hay = (r[COL.name] + ' ' + (r[COL.type_line] || '') + ' ' + (r[COL.oracle_text] || '')).toLowerCase();
        return terms.every(function (t) { return hay.indexOf(t) >= 0; });
      });
    }
    return { preds: preds, terms: terms, note: note };
  }

  /* deck:<slug> support — the deck payloads are already loaded eagerly. */
  var deckNameCache = {};
  function deckNameSet(slug) {
    if (deckNameCache[slug] !== undefined) return deckNameCache[slug];
    var d = RL.data('deck:' + slug);
    if (!d || !d.cards) {
      // allow a prefix (tid -> tidus)
      var core = RL.data('core');
      var hit = core && (core.decks || []).filter(function (x) { return x.slug.indexOf(slug) === 0; })[0];
      d = hit ? RL.data('deck:' + hit.slug) : null;
    }
    var set = null;
    if (d && d.cards) { set = {}; d.cards.forEach(function (c) { set[c.name.toLowerCase()] = 1; }); }
    deckNameCache[slug] = set;
    return set;
  }

  function runSearch(payload, query) {
    var rows = payload.rows || [];
    var parsed = parseQuery(query);
    var out = { query: query, terms: parsed.terms, note: parsed.note, hits: [], total: 0 };
    if (!parsed.preds.length) return out;
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i], ok = true;
      for (var p = 0; p < parsed.preds.length; p++) { if (!parsed.preds[p](r)) { ok = false; break; } }
      if (!ok) continue;
      out.total++;
      if (out.hits.length < MAX_RESULTS) out.hits.push(r);
    }
    out.hits.sort(function (a, b) {
      return (a[COL.edhrec_rank] || 1e9) - (b[COL.edhrec_rank] || 1e9) || a[COL.name].localeCompare(b[COL.name]);
    });
    return out;
  }

  /* ==========================================================================
     2. RENDER
     ====================================================================== */
  var dom = null, payload = null, selected = null, lastQuery = '';

  function snippet(text, terms) {
    text = text || '';
    if (text.length <= 160) return text;
    var low = text.toLowerCase(), at = -1;
    (terms || []).forEach(function (t) { var p = low.indexOf(t); if (p >= 0 && (at < 0 || p < at)) at = p; });
    if (at < 0) at = 0;
    var from = Math.max(0, at - 60);
    return (from > 0 ? '…' : '') + text.slice(from, from + 160).trim() + (from + 160 < text.length ? '…' : '');
  }

  function resultRow(r, terms) {
    var legal = r[COL.legal_commander] === 'legal';
    var btn = RL.el('button', {
      class: ['cardrow', selected === r ? 'is-selected' : ''], type: 'button',
      on: { click: function () { select(r, btn); } }
    },
      RL.el('span', { class: 'cardrow__top' },
        RL.el('span', { class: 'cardrow__name', text: r[COL.name] }),
        r[COL.mana_cost] ? RL.manaCost(r[COL.mana_cost]) : null),
      RL.el('span', { class: 'cardrow__type', text: r[COL.type_line] || '' }),
      r[COL.oracle_text] ? RL.el('span', { class: 'cardrow__snip', text: snippet(r[COL.oracle_text], terms) }) : null,
      RL.el('span', { class: 'cardrow__meta' },
        r[COL.pt] ? RL.el('span', { class: 'mono', text: r[COL.pt] }) : null,
        RL.el('span', { class: ['cardrow__rarity', 'is-' + (r[COL.rarity] || '')], text: r[COL.rarity] || '—' }),
        r[COL.price_usd] ? RL.el('span', { class: 'mono', text: RL.fmt.price(r[COL.price_usd]) }) : null,
        legal ? null : RL.el('span', { class: 'chip chip--bad', text: 'not legal' }))
    );
    return btn;
  }

  function renderResults(res) {
    var host = dom.results;
    RL.clear(host);
    if (!res.query) {
      dom.count.textContent = '';
      host.appendChild(helpPanel());
      return;
    }
    if (res.note) {
      host.appendChild(RL.el('p', { class: 'cardsearch__note' }, RL.svgIcon('info', 16),
        RL.el('span', { text: res.note })));
    }
    if (!res.hits.length) {
      dom.count.textContent = 'no matches';
      host.appendChild(RL.el('p', { class: 'cards__empty' },
        'Nothing matches ', RL.el('strong', { text: res.query }),
        '. Every filter has to hold at once — try dropping one.'));
      return;
    }
    dom.count.textContent = res.total > res.hits.length
      ? 'showing ' + res.hits.length + ' of ' + RL.fmt.int(res.total) + ' matches'
      : RL.fmt.plural(res.total, 'match', 'matches');

    var list = RL.el('div', { class: 'cardrows' });
    res.hits.forEach(function (r) { list.appendChild(resultRow(r, res.terms)); });
    host.appendChild(list);
    if (res.total > res.hits.length) {
      host.appendChild(RL.el('p', { class: 'cards__more', text:
        'Refine the search to see the other ' + RL.fmt.int(res.total - res.hits.length) +
        ' — only the top ' + MAX_RESULTS + ' by EDHREC rank are drawn.' }));
    }
  }

  function fact(k, v, cls) {
    return RL.el('div', { class: 'fact' },
      RL.el('span', { class: 'fact__k', text: k }),
      RL.el('span', { class: ['fact__v', cls || ''] }, v instanceof Node ? v : RL.el('span', { text: v })));
  }

  function renderDetail(r) {
    var host = dom.detail;
    RL.clear(host);
    if (!r) {
      host.appendChild(RL.el('div', { class: 'cards__placeholder' },
        RL.svgIcon('search', 28),
        RL.el('p', { text: 'Pick a card on the left to read its full text.' })));
      return;
    }
    var legal = r[COL.legal_commander] === 'legal';
    var art = RL.el('article', { class: 'panel carddetail' },
      RL.el('header', { class: 'carddetail__head' },
        RL.el('h2', { class: 'carddetail__name', text: r[COL.name] }),
        r[COL.mana_cost] ? RL.manaCost(r[COL.mana_cost]) : null),
      RL.el('p', { class: 'carddetail__type', text: r[COL.type_line] || '' }));

    if (r[COL.oracle_text]) {
      art.appendChild(RL.el('div', { class: 'carddetail__oracle', text: r[COL.oracle_text] }));
    } else {
      art.appendChild(RL.el('p', { class: 'muted', text: 'This card has no rules text.' }));
    }

    var identity = (r[COL.color_identity] || []);
    var facts = RL.el('div', { class: 'drawer__facts' },
      fact('Mana value', RL.fmt.num(r[COL.cmc], 0)),
      r[COL.pt] ? fact('P/T or loyalty', r[COL.pt]) : null,
      fact('Rarity', (r[COL.rarity] || '—'), r[COL.rarity] ? 'fact__v--' + r[COL.rarity] : ''),
      fact('Price', r[COL.price_usd] ? RL.fmt.price(r[COL.price_usd]) : RL.fmt.dash),
      fact('EDHREC rank', r[COL.edhrec_rank] ? '#' + RL.fmt.int(r[COL.edhrec_rank]) : RL.fmt.dash),
      fact('Commander legal', legal ? 'Yes' : 'No', legal ? '' : 'fact__v--bad'),
      fact('Colour identity', identity.length
        ? (function () { var s = RL.el('span', { class: 'mana' }); identity.forEach(function (c) { s.appendChild(RL.colorChip(c)); }); return s; })()
        : 'Colourless'));
    // filter out the null P/T fact node
    Array.prototype.slice.call(facts.childNodes).forEach(function (n) { if (!n.nodeType) facts.removeChild(n); });
    art.appendChild(facts);

    art.appendChild(RL.el('p', { class: 'carddetail__cli mono' },
      RL.svgIcon('terminal', 14),
      RL.el('span', { text: './bin/mtg card "' + r[COL.name] + '"' })));
    art.appendChild(RL.el('p', { class: 'muted carddetail__foot', text:
      'Card art and official rulings are not in this payload — run the command above for the rulings.' }));

    host.appendChild(art);
  }

  function helpPanel() {
    function ex(q, why) {
      return RL.el('li', null,
        RL.el('button', { class: 'cards__ex', type: 'button',
          on: { click: function () { dom.input.value = q; schedule(); dom.input.focus(); } } },
          RL.el('code', { class: 'mono', text: q })),
        RL.el('span', { class: 'cards__exwhy', text: why }));
    }
    return RL.el('div', { class: 'panel panel--quiet cards__help' },
      RL.el('h2', { class: 'panel__title' }, RL.svgIcon('search', 20),
        RL.el('span', { text: 'The same query language as the terminal' })),
      RL.el('p', { class: 'panel__sub', text:
        'Filters combine with AND. Type a few words, or use a field. Press / to focus search.' }),
      RL.el('ul', { class: 'cards__examples' },
        ex('t:instant c:u', 'Blue instants (identity fits mono-blue).'),
        ex('cmc<=2 t:creature', 'Two-drops and cheaper creatures.'),
        ex('id:wug legal:commander', 'Cards that fit a Bant (W/U/G) deck.'),
        ex('deck:tidus t:land', 'Just the lands in the Tidus deck.'),
        ex('draw a card', 'Free text matches name, type and rules text.'),
        ex('r:mythic cmc>=6', 'Big mythics.')));
  }

  /* ==========================================================================
     3. MOUNT + LAZY LOAD
     ====================================================================== */
  var timer = null;
  function schedule() { window.clearTimeout(timer); timer = window.setTimeout(doSearch, 140); }

  function doSearch() {
    if (!dom || !payload) return;
    lastQuery = dom.input.value.trim();
    var res = runSearch(payload, lastQuery);
    // keep selection only if it still matches
    if (selected && res.hits.indexOf(selected) < 0) { selected = null; renderDetail(null); }
    renderResults(res);
    dom.pane.classList.toggle('is-searching', !!res.query);
  }

  function select(r, btn) {
    selected = r;
    renderDetail(r);
    Array.prototype.forEach.call(dom.results.querySelectorAll('.cardrow.is-selected'),
      function (b) { b.classList.remove('is-selected'); });
    if (btn) btn.classList.add('is-selected');
  }

  var keyHandler = null;

  function mount(el) {
    el.appendChild(RL.el('h1', { class: 'section-title', text: 'Cards' }));
    el.appendChild(RL.el('p', { class: 'section-sub' },
      'Every card in the database, searchable with the ',
      RL.el('code', { class: 'md-code', text: 'mtg search' }),
      ' query language. The card data loads once, the first time you open this section.'));

    var input = RL.el('input', {
      class: 'input', type: 'search', id: 'cards-search',
      placeholder: 'e.g. t:creature c:g cmc<=3', autocomplete: 'off', spellcheck: 'false',
      on: { input: schedule, keydown: function (e) {
        if (e.key === 'Escape' && input.value) { e.preventDefault(); input.value = ''; doSearch(); }
      } }
    });
    var clear = RL.el('button', { class: 'icon-btn', type: 'button', aria: { label: 'Clear the search' },
      on: { click: function () { input.value = ''; doSearch(); input.focus(); } } }, RL.svgIcon('x', 18));
    var count = RL.el('p', { class: 'cardsearch__count', role: 'status', 'aria-live': 'polite' });

    var results = RL.el('div', { class: 'cards__results' });
    var detail = RL.el('div', { class: 'cards__detail' });

    var pane = RL.el('div', { class: 'cards' },
      RL.el('aside', { class: 'cards__left' },
        RL.el('div', { class: 'rsearch__field cards__field' }, RL.svgIcon('search', 18), input, clear),
        count, results),
      RL.el('div', { class: 'cards__right' }, detail));
    el.appendChild(pane);

    dom = { input: input, count: count, results: results, detail: detail, pane: pane };
    renderDetail(null);

    // loading state, then lazy-load the payload
    if (RL.has('cards')) { payload = RL.data('cards'); afterLoad(); }
    else {
      results.appendChild(RL.el('div', { class: 'cards__loading' },
        RL.el('span', { class: 'spinner', 'aria-hidden': 'true' }),
        RL.el('span', { text: 'Loading the card database…' })));
      RL.loadLazy('cards', 'cards.js', function (data, err) {
        RL.clear(results);
        if (err || !data) {
          results.appendChild(RL.el('div', { class: 'panel state state--bad' },
            RL.el('div', { class: 'state__icon' }, RL.svgIcon('alert-triangle', 28)),
            RL.el('h2', { class: 'state__title', text: 'The card data did not load' }),
            RL.el('p', { class: 'state__body' },
              'Expected ', RL.el('code', { class: 'md-code', text: 'dashboard/data/cards.js' }),
              '. Run ', RL.el('code', { class: 'md-code', text: './bin/mtg dashboard --build' }),
              ' and reload.'),
            err ? RL.el('pre', { class: 'state__pre', text: String(err.message || err) }) : null));
          return;
        }
        payload = data;
        afterLoad();
      });
    }
  }

  function afterLoad() {
    var initial = (RL.route().params[0] || '');
    if (initial) dom.input.value = initial;
    doSearch();
  }

  RL.registerView({
    id: 'cards', label: 'Cards', icon: 'search', mount: mount,
    onEnter: function (params) {
      if (!dom) return;
      if (params[0] && params[0] !== lastQuery && payload) { dom.input.value = params[0]; doSearch(); }
      if (!keyHandler) {
        keyHandler = function (e) {
          if (e.key !== '/' || e.metaKey || e.ctrlKey || e.altKey) return;
          var t = e.target;
          if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable)) return;
          e.preventDefault(); dom.input.focus(); dom.input.select();
        };
        document.addEventListener('keydown', keyHandler);
      }
    },
    onLeave: function () {
      if (keyHandler) { document.removeEventListener('keydown', keyHandler); keyHandler = null; }
    }
  });

})(window, document);

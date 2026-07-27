/* ============================================================================
   REMY'S LAIR — app/view-decks.js
   VIEW: "Decks" (#/decks, #/decks/<slug>) — one precon, fully opened up.

   What this view is FOR: the CLI can print a decklist, its stats, and its
   bracket in three separate calls. This puts all three on one page and adds the
   thing a terminal cannot — the cards as cards, and their official rulings one
   tap away. Header and charts come from the SAME numbers `mtg deck stats` /
   `mtg deck bracket` compute (core.js reused the CLI code path); the grid, the
   drawer and the documents come from the per-deck payload.

   Constraints honoured:
     C1  zero LLM spend  — pure rendering. No inference.
     C2  never invent    — oracle text and rulings are inserted verbatim as text
                           nodes; nothing is reworded or summarised. Every stat is
                           a field the payload carries. A Game Changer is named,
                           never described.
     C5  offline-first   — no fetch; art is a local <img> with a card-shaped
                           placeholder fallback.
     C6/no-build         — plain ES2019-ish script.
     C3  Commander only  — no other format is named anywhere in this file.

   Styling contract: assets/views-deck.css already defines every class here.
   Exports window.RLDeck (cardFrame + slug resolver) for the Merge view.
   ========================================================================== */
(function (window, document) {
  'use strict';

  var RL = window.RL;
  if (!RL) return;

  RL.icons.grid = '<rect x="3.5" y="3.5" width="7" height="7" rx="1.4"/>' +
                  '<rect x="13.5" y="3.5" width="7" height="7" rx="1.4"/>' +
                  '<rect x="3.5" y="13.5" width="7" height="7" rx="1.4"/>' +
                  '<rect x="13.5" y="13.5" width="7" height="7" rx="1.4"/>';
  RL.icons.list = '<path d="M8 6h12"/><path d="M8 12h12"/><path d="M8 18h12"/>' +
                  '<path d="M3.6 6h.01"/><path d="M3.6 12h.01"/><path d="M3.6 18h.01"/>';
  RL.icons.coin = RL.icons.coins;

  var COLOR_ORDER = ['W', 'U', 'B', 'R', 'G'];
  var COLOR_NAMES = { W: 'White', U: 'Blue', B: 'Black', R: 'Red', G: 'Green', C: 'Colorless' };
  var TYPE_ORDER = ['Commander', 'Creature', 'Planeswalker', 'Instant', 'Sorcery',
                    'Artifact', 'Enchantment', 'Battle', 'Land', 'Other'];
  var ROLE_ORDER = ['ramp', 'draw', 'removal', 'boardwipe', 'interaction', 'recursion', 'tutor', 'wincon'];

  /* ---- the card frame (shared with Lair / Merge) ------------------------ */
  function cardFrame(name, manaCost, image, opts) {
    opts = opts || {};
    var frame = RL.el('div', { class: ['cardframe', opts.className || ''] });
    frame.appendChild(RL.el('div', { class: 'cardframe__ph' },
      RL.el('span', { class: 'cardframe__phname', text: name || 'Unknown card' }),
      manaCost ? RL.manaCost(manaCost) : null,
      RL.el('span', { class: 'cardframe__phnote', text: opts.note || 'art offline' })));
    if (image) {
      var img = RL.el('img', {
        class: 'cardframe__img', src: image, alt: opts.alt || (name || 'card') + ' card art',
        loading: 'lazy', decoding: 'async',
        on: { error: function () { if (img.parentNode) img.parentNode.removeChild(img); } }
      });
      frame.appendChild(img);
    }
    return frame;
  }

  function bracketBadgeButton(deck, onClick) {
    var n = deck.bracket;
    var cls = ['bracketbadge'];
    if (n) cls.push('bracketbadge--' + n);
    return RL.el('button', {
      class: cls, type: 'button', 'aria-expanded': 'false',
      aria: { label: 'Bracket ' + (n == null ? 'unknown' : n) + ' — press for the reasoning' },
      on: { click: onClick }
    },
      RL.svgIcon('shield', 14),
      RL.el('span', null, 'Bracket ',
        RL.el('span', { class: 'bracketbadge__n', text: n == null ? '?' : String(n) }),
        deck.bracket_detail && deck.bracket_detail.name ? ' · ' + deck.bracket_detail.name : ''),
      RL.svgIcon('chevron-down', 14));
  }

  function commanderCard(deckData) {
    if (!deckData || !deckData.cards) return null;
    for (var i = 0; i < deckData.cards.length; i++) {
      if (deckData.cards[i].board === 'commander') return deckData.cards[i];
    }
    return null;
  }

  /* ==========================================================================
     1. HEADER
     ====================================================================== */
  function deckHeader(deck, deckData) {
    var cmd = commanderCard(deckData);
    var art = RL.el('div', { class: 'deckhead__art' },
      cardFrame(cmd ? cmd.name : deck.commander, cmd ? cmd.mana_cost : '',
        cmd ? cmd.image : null, { alt: (cmd ? cmd.name : deck.commander) + ' card art' }));

    var reveal = RL.el('div', { class: 'reveal', hidden: true },
      RL.el('h3', { class: 'reveal__title', text: 'Why Bracket ' + (deck.bracket || '?') }));
    var bd = deck.bracket_detail;
    if (bd) {
      if (bd.summary) reveal.appendChild(RL.el('p', { class: 'dim', text: bd.summary }));
      var ul = RL.el('ul');
      (bd.reasoning || []).forEach(function (r) { ul.appendChild(RL.el('li', { text: r })); });
      reveal.appendChild(ul);
      if ((bd.caveats || []).length) {
        reveal.appendChild(RL.el('p', { class: 'verdict__heur', text: 'Needs a human eye: ' + bd.caveats.join(' ') }));
      }
    } else {
      reveal.appendChild(RL.el('p', { class: 'muted', text:
        'Bracket detail is not in this build. Run `mtg deck bracket ' + deck.slug + '` to see it.' }));
    }

    var badge = bracketBadgeButton(deck, function () {
      var open = reveal.hidden;
      reveal.hidden = !open;
      badge.setAttribute('aria-expanded', open ? 'true' : 'false');
      var chev = badge.querySelector('.icon--chevron-down, .icon--chevron-up');
      if (chev) chev.replaceWith(RL.svgIcon(open ? 'chevron-up' : 'chevron-down', 14));
    });

    var pips = RL.el('span', { class: 'row row--tight', aria: { label: 'Colour identity' } });
    (deck.color_identity || []).forEach(function (c) { pips.appendChild(RL.colorChip(c)); });
    if (!(deck.color_identity || []).length) pips.appendChild(RL.colorChip('C'));

    var meta = RL.el('div', { class: 'deckhead__meta' }, badge, pips,
      RL.el('span', { class: 'chip' }, RL.svgIcon('layers', 14),
        RL.el('span', { text: (deck.set_code || '—') + ' · ' + RL.fmt.date(deck.release_date) })));

    var right = RL.el('div', null,
      RL.el('h1', { class: 'deckhead__title', text: deck.name }),
      RL.el('div', { class: 'deckhead__cmdr', text: deck.commander }),
      cmd ? RL.el('div', { class: 'deckhead__type', text: cmd.type_line }) : null,
      meta, reveal);

    if (cmd && cmd.oracle_text) {
      right.appendChild(RL.el('div', { class: 'deckhead__oracle', text: cmd.oracle_text }));
    }

    return RL.el('div', { class: 'deckhead' }, art, right);
  }

  /* ==========================================================================
     2. STATS + CHARTS + VERDICT
     ====================================================================== */
  function statRow(deck) {
    var t = deck.totals || {}, mv = deck.mana_value || {}, roles = deck.roles || {};
    var row = RL.el('div', { class: 'statrow' },
      RL.stat('Maindeck', RL.fmt.int(t.maindeck), { note: RL.fmt.int(t.commander) + ' commander' }),
      RL.stat('Lands', RL.fmt.int(t.lands), { tone: 'fel',
        note: RL.fmt.int(t.nonlands) + ' non-lands' }),
      RL.stat('Avg MV', mv.avg_nonland != null ? RL.fmt.num(mv.avg_nonland, 2) : RL.fmt.dash,
        { note: 'non-lands' }),
      RL.stat('Removal + wipes', RL.fmt.int((roles.removal || 0) + (roles.boardwipe || 0)),
        { note: RL.fmt.int(roles.ramp || 0) + ' ramp · ' + RL.fmt.int(roles.draw || 0) + ' draw' })
    );
    return row;
  }

  function curveChart(deck) {
    var buckets = (deck.curve && deck.curve.buckets) || {};
    var data = ['0', '1', '2', '3', '4', '5', '6', '7+'].map(function (b) {
      return { label: b, value: buckets[b] || 0 };
    });
    return RL.chart.bar({
      title: 'Mana curve', data: data,
      categoryLabel: 'Mana value', valueLabel: 'Cards', height: 220,
      description: 'Maindeck non-lands. The commander is available every turn, so it is not on the curve.'
    });
  }

  function colorChart(deck) {
    var colors = deck.colors || {};
    var identity = (colors.identity && colors.identity.length ? colors.identity : COLOR_ORDER);
    var sources = colors.sources_per_color || {};
    var data = identity.map(function (c) {
      return { label: COLOR_NAMES[c] || c, value: sources[c] || 0, color: RL.manaVar(c) };
    });
    return RL.chart.hbar({
      title: 'Colour sources (lands)', data: data,
      categoryLabel: 'Colour', valueLabel: 'Land sources',
      description: 'How many lands can produce each colour. Any-colour lands count toward every colour.'
    });
  }

  function rolesChart(deck) {
    var roles = deck.roles || {};
    var data = ROLE_ORDER.map(function (r) {
      return { label: r.charAt(0).toUpperCase() + r.slice(1), value: roles[r] || 0 };
    }).filter(function (d) { return d.value > 0; });
    if (!data.length) return null;
    return RL.chart.hbar({
      title: 'Roles', data: data, categoryLabel: 'Role', valueLabel: 'Cards',
      description: 'A card can hold several roles, so these do not sum to the deck size.'
    });
  }

  function verdictBlock(deck) {
    var a = deck.assessment;
    if (!a) return null;
    var warn = !a.land_count_ok;
    var block = RL.el('div', { class: ['verdict', warn ? 'verdict--warn' : ''] },
      RL.el('div', { class: 'verdict__head' },
        RL.svgIcon(warn ? 'alert-triangle' : 'check', 16),
        RL.el('span', { text: 'Mana base: ' + (a.verdict || 'assessed') })));
    (a.notes || []).forEach(function (n) { block.appendChild(RL.el('p', { text: n })); });
    block.appendChild(RL.el('p', { class: 'verdict__heur', text:
      'This is the usual EDH land heuristic, not a rule. Re-run `mtg deck stats ' +
      deck.slug + '` for the live numbers.' }));
    return block;
  }

  function statsSection(deck) {
    var charts = RL.el('div', { class: 'chartgrid' });
    charts.appendChild(curveChart(deck));
    charts.appendChild(colorChart(deck));
    var roles = rolesChart(deck);
    if (roles) charts.appendChild(roles);

    var sec = RL.el('section', { class: 'panel' },
      RL.el('div', { class: 'panel__head' },
        RL.el('h2', { class: 'panel__title' },
          RL.svgIcon('chart-bar', 20), RL.el('span', { text: 'By the numbers' }))),
      statRow(deck), charts);
    var v = verdictBlock(deck);
    if (v) sec.appendChild(v);
    return sec;
  }

  /* ==========================================================================
     3. CARD GRID + FILTER TOOLBAR
     ====================================================================== */
  function typeGroupOf(card) {
    if (card.board === 'commander') return 'Commander';
    return TYPE_ORDER.indexOf(card.type_group) >= 0 ? card.type_group : 'Other';
  }

  var SORTS = {
    cmc: function (a, b) { return (a.cmc - b.cmc) || a.name.localeCompare(b.name); },
    name: function (a, b) { return a.name.localeCompare(b.name); },
    edhrec: function (a, b) { return (a.edhrec_rank || 1e9) - (b.edhrec_rank || 1e9) || a.name.localeCompare(b.name); },
    price: function (a, b) { return (parseFloat(b.price_usd) || 0) - (parseFloat(a.price_usd) || 0) || a.name.localeCompare(b.name); }
  };

  function cardMatches(card, state) {
    if (state.q) {
      var hay = (card.name + ' ' + (card.type_line || '') + ' ' + (card.oracle_text || '')).toLowerCase();
      if (hay.indexOf(state.q) === -1) return false;
    }
    if (state.colors.length) {
      var ci = card.color_identity || [];
      var colorless = ci.length === 0;
      var ok = state.colors.some(function (c) {
        return c === 'C' ? colorless : ci.indexOf(c) >= 0;
      });
      if (!ok) return false;
    }
    return true;
  }

  function cardTile(card, onOpen) {
    var qty = card.count > 1
      ? RL.el('span', { class: 'cardtile__qty', text: '×' + card.count }) : null;
    return RL.el('button', {
      class: 'cardtile', type: 'button',
      aria: { label: card.name + (card.count > 1 ? ', ' + card.count + ' copies' : '') + ' — open details' },
      on: { click: function () { onOpen(card); } }
    },
      cardFrame(card.name, card.mana_cost, card.image, { alt: card.name + ' card art' }),
      RL.el('span', { class: 'cardtile__cap' },
        RL.el('span', { class: 'cardtile__name', text: card.name }), qty));
  }

  function buildGrid(cards, state, onOpen) {
    var wrap = RL.el('div');
    var matched = cards.filter(function (c) { return cardMatches(c, state); });
    matched.sort(SORTS[state.sort] || SORTS.cmc);

    if (!matched.length) {
      wrap.appendChild(RL.el('div', { class: 'emptyfilter' },
        RL.el('p', null, 'No cards in this deck match those filters.'),
        RL.el('button', { class: 'btn btn--ghost', type: 'button',
          on: { click: state.onClear } }, RL.el('span', { text: 'Clear filters' }))));
      return wrap;
    }

    if (state.mode === 'list') {
      wrap.appendChild(buildList(matched, state, onOpen));
      return wrap;
    }

    // grouped-by-type grid
    var groups = {};
    matched.forEach(function (c) { (groups[typeGroupOf(c)] || (groups[typeGroupOf(c)] = [])).push(c); });
    TYPE_ORDER.forEach(function (type) {
      var list = groups[type];
      if (!list || !list.length) return;
      var count = list.reduce(function (a, c) { return a + c.count; }, 0);
      var grid = RL.el('ul', { class: 'cardgrid' });
      list.forEach(function (c) { grid.appendChild(RL.el('li', null, cardTile(c, onOpen))); });
      wrap.appendChild(RL.el('section', { class: 'cardgroup' },
        RL.el('div', { class: 'cardgroup__head' },
          RL.el('h3', { class: 'cardgroup__title', text: type }),
          RL.el('span', { class: 'cardgroup__count', text: RL.fmt.plural(count, 'card') }),
          RL.el('span', { class: 'cardgroup__rule', 'aria-hidden': 'true' })),
        grid));
    });
    return wrap;
  }

  function buildList(cards, state, onOpen) {
    var cols = [
      { key: 'name', label: 'Card', num: false },
      { key: 'cmc', label: 'MV', num: true },
      { key: 'type', label: 'Type', num: false },
      { key: 'role', label: 'Role', num: false },
      { key: 'price', label: 'Price', num: true }
    ];
    var thead = RL.el('tr');
    cols.forEach(function (col) {
      var sortable = SORTS[col.key];
      var th = RL.el('th', { scope: 'col', class: col.num ? 'num' : '' });
      if (sortable) {
        var arrow = state.sort === col.key ? ' ↓' : '';
        th.setAttribute('aria-sort', state.sort === col.key ? 'descending' : 'none');
        th.appendChild(RL.el('button', { type: 'button',
          on: { click: function () { state.setSort(col.key); } } },
          RL.el('span', { text: col.label }),
          RL.el('span', { class: 'sortarrow', text: arrow })));
      } else {
        th.appendChild(RL.el('span', { text: col.label }));
      }
      thead.appendChild(th);
    });

    var tbody = RL.el('tbody');
    cards.forEach(function (c) {
      var priceCls = 'fact__v--' + (c.rarity || '');
      tbody.appendChild(RL.el('tr', null,
        RL.el('td', null,
          RL.el('button', { class: 'namecell', type: 'button',
            on: { click: function () { onOpen(c); } } },
            RL.el('span', { text: (c.count > 1 ? c.count + '× ' : '') + c.name }))),
        RL.el('td', { class: 'num mono', text: RL.fmt.num(c.cmc, 0) }),
        RL.el('td', { text: c.type_group || (c.type_line || '').split('—')[0].trim() }),
        RL.el('td', { class: 'rolecell', text: (c.roles && c.roles.length) ? c.roles.join(', ') : '—' }),
        RL.el('td', { class: 'num mono', text: c.price_usd ? RL.fmt.price(c.price_usd) : RL.fmt.dash })));
    });

    return RL.el('div', { class: 'tablewrap' },
      RL.el('table', { class: 'data-table cardlist' },
        RL.el('thead', null, thead), tbody));
  }

  /* ---- toolbar ---------------------------------------------------------- */
  function buildToolbar(deck, state, rerender) {
    var count = RL.el('span', { class: 'cardtoolbar__count', role: 'status', 'aria-live': 'polite' });

    var search = RL.el('input', {
      class: 'input', type: 'search', placeholder: 'Filter this deck…',
      autocomplete: 'off', spellcheck: 'false', 'aria-label': 'Filter cards in this deck',
      on: { input: function () { state.q = search.value.trim().toLowerCase(); rerender(); } }
    });

    var colorFilter = RL.el('div', { class: 'colorfilter', role: 'group', 'aria-label': 'Filter by colour identity' });
    COLOR_ORDER.concat(['C']).forEach(function (c) {
      var btn = RL.el('button', {
        class: 'colorfilter__btn', type: 'button', 'aria-pressed': 'false',
        aria: { label: COLOR_NAMES[c] },
        on: { click: function () {
          var i = state.colors.indexOf(c);
          if (i >= 0) state.colors.splice(i, 1); else state.colors.push(c);
          btn.setAttribute('aria-pressed', state.colors.indexOf(c) >= 0 ? 'true' : 'false');
          rerender();
        } }
      },
        RL.el('span', { class: 'colorfilter__swatch', 'aria-hidden': 'true',
          style: { '--swatch': RL.manaVar(c) } }),
        RL.el('span', { text: c }));
      colorFilter.appendChild(btn);
    });

    var sortSel = RL.el('select', { class: 'select', 'aria-label': 'Sort cards',
      on: { change: function () { state.sort = sortSel.value; rerender(); } } });
    [['cmc', 'Mana value'], ['name', 'Name'], ['edhrec', 'EDHREC rank'], ['price', 'Price']].forEach(function (o) {
      var opt = RL.el('option', { value: o[0], text: o[1] });
      if (o[0] === state.sort) opt.selected = true;
      sortSel.appendChild(opt);
    });

    function modeBtn(mode, icon, label) {
      var b = RL.el('button', { class: 'icon-btn', type: 'button', 'aria-pressed': String(state.mode === mode),
        aria: { label: label }, on: { click: function () { state.mode = mode; rerender(); } } },
        RL.svgIcon(icon, 18));
      return b;
    }

    state.countEl = count;
    return RL.el('div', { class: 'cardtoolbar' },
      RL.el('div', { class: 'field' },
        RL.el('span', { class: 'field__label', text: 'Find' }), search),
      RL.el('div', { class: 'cardtoolbar__group' }, colorFilter),
      RL.el('div', { class: 'field' },
        RL.el('span', { class: 'field__label', text: 'Sort' }), sortSel),
      RL.el('span', { class: 'cardtoolbar__spacer' }),
      count,
      RL.el('div', { class: 'cardtoolbar__group', role: 'group', 'aria-label': 'View mode' },
        modeBtn('grid', 'grid', 'Grid view'), modeBtn('list', 'list', 'List view')));
  }

  /* ==========================================================================
     4. DETAIL DRAWER
     ====================================================================== */
  var activeDrawer = null;

  function closeDrawer() {
    if (!activeDrawer) return;
    var d = activeDrawer;
    activeDrawer = null;
    document.removeEventListener('keydown', d.onKey, true);
    if (d.back && d.back.parentNode) d.back.parentNode.removeChild(d.back);
    if (d.el && d.el.parentNode) d.el.parentNode.removeChild(d.el);
    if (d.restore && d.restore.focus && document.contains(d.restore)) d.restore.focus();
  }

  function rarityClass(r) { return r ? 'fact__v--' + r : ''; }

  function fact(k, v, cls) {
    return RL.el('div', { class: 'fact' },
      RL.el('span', { class: 'fact__k', text: k }),
      RL.el('span', { class: ['fact__v', cls || ''] }, v instanceof Node ? v : RL.el('span', { text: v })));
  }

  function openDrawer(card) {
    closeDrawer();
    var restore = document.activeElement;
    var back = RL.el('div', { class: 'drawer-back', on: { click: closeDrawer } });

    var title = RL.el('h2', { class: 'drawer__title', id: 'drawer-title', text: card.name });
    var close = RL.el('button', { class: 'icon-btn drawer__close', type: 'button',
      aria: { label: 'Close card details' }, on: { click: closeDrawer } }, RL.svgIcon('x', 20));

    var body = RL.el('div', { class: 'drawer__body' });
    body.appendChild(RL.el('div', { class: 'drawer__art' },
      cardFrame(card.name, card.mana_cost, card.image, { alt: card.name + ' card art' })));

    if (card.mana_cost) {
      body.appendChild(RL.el('div', { class: 'row', style: { marginBottom: 'var(--s-4)' } },
        RL.el('span', { class: 'field__label', text: 'Cost' }), RL.manaCost(card.mana_cost)));
    }
    if (card.oracle_text) {
      body.appendChild(RL.el('div', { class: 'drawer__oracle', text: card.oracle_text }));
    }

    var identity = (card.color_identity || []);
    var facts = RL.el('div', { class: 'drawer__facts' },
      fact('Type', card.type_line || '—'),
      fact('Mana value', RL.fmt.num(card.cmc, 0)),
      fact('Rarity', card.rarity ? card.rarity.charAt(0).toUpperCase() + card.rarity.slice(1) : '—', rarityClass(card.rarity)),
      fact('Price', card.price_usd ? RL.fmt.price(card.price_usd) : RL.fmt.dash),
      fact('EDHREC rank', card.edhrec_rank ? '#' + RL.fmt.int(card.edhrec_rank) : RL.fmt.dash),
      fact('Colour identity', identity.length
        ? (function () { var s = RL.el('span', { class: 'mana' }); identity.forEach(function (c) { s.appendChild(RL.colorChip(c)); }); return s; })()
        : 'Colourless')
    );
    if (card.power != null && card.toughness != null) {
      facts.appendChild(fact('Power / toughness', card.power + ' / ' + card.toughness));
    } else if (card.loyalty != null) {
      facts.appendChild(fact('Loyalty', String(card.loyalty)));
    }
    body.appendChild(facts);

    // rulings — verbatim, oldest first
    body.appendChild(RL.el('h3', { class: 'drawer__subhead' },
      RL.fmt.plural((card.rulings || []).length, 'official ruling')));
    if ((card.rulings || []).length) {
      var ul = RL.el('ul', { class: 'rulings' });
      card.rulings.forEach(function (r) {
        ul.appendChild(RL.el('li', { class: 'ruling' },
          RL.el('span', { class: 'ruling__date', text: RL.fmt.date(r.published_at) }),
          RL.el('span', { class: 'ruling__text', text: r.comment })));
      });
      body.appendChild(ul);
    } else {
      body.appendChild(RL.el('p', { class: 'norulings', text:
        'No official rulings for this card in the data on this machine.' }));
    }

    body.appendChild(RL.el('p', { class: 'verdict__heur', style: { marginTop: 'var(--s-5)' } },
      RL.svgIcon('terminal', 14), ' ',
      RL.el('code', { class: 'mono', text: './bin/mtg card "' + card.name + '"' })));

    var drawer = RL.el('aside', { class: 'drawer', role: 'dialog', 'aria-modal': 'true',
      'aria-labelledby': 'drawer-title' },
      RL.el('div', { class: 'drawer__head' }, title, close), body);

    function onKey(e) {
      if (e.key === 'Escape') { e.preventDefault(); closeDrawer(); return; }
      if (e.key !== 'Tab') return;
      var f = drawer.querySelectorAll('a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }

    document.body.appendChild(back);
    document.body.appendChild(drawer);
    document.addEventListener('keydown', onKey, true);
    activeDrawer = { el: drawer, back: back, onKey: onKey, restore: restore };
    close.focus();
  }

  /* ==========================================================================
     5. DOCUMENTS (PRIMER / CARDS / UPGRADES) with a table of contents
     ====================================================================== */
  var DOC_TABS = [
    { key: 'primer', label: 'Primer' },
    { key: 'cards', label: 'Card by card' },
    { key: 'upgrades', label: 'Upgrades' }
  ];

  function slugifyHeading(text) { return 'doc-' + RL.slug(text); }

  function renderDoc(deckData, which, host) {
    RL.clear(host);
    var docs = (deckData && deckData.docs) || {};
    var src = docs[which];
    if (!src) {
      host.appendChild(RL.el('div', { class: 'emptyfilter' },
        RL.el('p', null, 'No ', RL.el('strong', { text: which }), ' document has been written for this deck yet.'),
        RL.el('p', { class: 'muted', text: 'It would live in decks/' + (deckData && deckData.slug) + '/' +
          which.toUpperCase() + '.md.' })));
      return;
    }

    var mdEl = RL.mdEl(src);
    // Build a TOC from the h2/h3 the markdown produced, and give each a stable id.
    var toc = RL.el('ul', { class: 'doctoc__list' });
    var heads = mdEl.querySelectorAll('.md-h2, .md-h3');
    var seen = {};
    var hasHeads = false;
    Array.prototype.forEach.call(heads, function (h) {
      var base = slugifyHeading(h.textContent);
      var id = base; var n = 1;
      while (seen[id]) { id = base + '-' + (++n); }
      seen[id] = true; h.id = id;
      hasHeads = true;
      var isL3 = h.classList.contains('md-h3');
      toc.appendChild(RL.el('li', null,
        RL.el('a', { class: ['doctoc__link', isL3 ? 'doctoc__link--l3' : ''],
          href: '#', 'data-target': id,
          on: { click: function (e) {
            e.preventDefault();
            var target = document.getElementById(id);
            if (target) target.scrollIntoView({ behavior: RL.reducedMotion() ? 'auto' : 'smooth', block: 'start' });
          } } },
          RL.el('span', { text: h.textContent }))));
    });

    var docBody = RL.el('div', { class: 'docbody' },
      RL.el('p', { class: 'docmeta' },
        'From decks/' + deckData.slug + '/' + which.toUpperCase() + '.md — rendered verbatim.'),
      mdEl);

    if (hasHeads) {
      host.appendChild(RL.el('div', { class: 'docwrap' },
        RL.el('nav', { class: 'doctoc', aria: { label: 'On this page' } },
          RL.el('div', { class: 'doctoc__title', text: 'On this page' }), toc),
        docBody));
    } else {
      host.appendChild(docBody);
    }
  }

  function documentsSection(deckData) {
    var state = { which: 'primer' };
    var body = RL.el('div');
    var tabs = RL.el('div', { class: 'doctabs', role: 'tablist', 'aria-label': 'Deck documents' });
    var docs = (deckData && deckData.docs) || {};

    var buttons = {};
    DOC_TABS.forEach(function (t) {
      var has = !!docs[t.key];
      var btn = RL.el('button', {
        class: 'doctab', type: 'button', role: 'tab',
        'aria-selected': String(t.key === state.which),
        on: { click: function () {
          state.which = t.key;
          DOC_TABS.forEach(function (o) { buttons[o.key].setAttribute('aria-selected', String(o.key === t.key)); });
          renderDoc(deckData, t.key, body);
        } }
      }, RL.el('span', { text: t.label }), has ? null : RL.el('span', { class: 'muted', text: ' ·' }));
      buttons[t.key] = btn;
      tabs.appendChild(btn);
    });

    renderDoc(deckData, state.which, body);

    return RL.el('section', { class: 'panel' },
      RL.el('div', { class: 'panel__head' },
        RL.el('h2', { class: 'panel__title' },
          RL.svgIcon('scroll', 20), RL.el('span', { text: 'The written deck' }))),
      RL.el('p', { class: 'panel__sub', text:
        'Omar’s own notes for this deck, straight from the repository — the game plan, ' +
        'the card-by-card, and the upgrade path.' }),
      tabs, body);
  }

  /* ==========================================================================
     6. DECK SWITCHER + ROUTING
     ====================================================================== */
  var dom = null;
  var currentSlug = null;

  function buildSwitcher(core) {
    var wrap = RL.el('div', { class: 'deckswitch', role: 'group', 'aria-label': 'Choose a deck' });
    (core.decks || []).forEach(function (d) {
      wrap.appendChild(RL.el('a', { class: 'btn', href: RL.href('decks', d.slug), 'data-slug': d.slug },
        RL.svgIcon('layers', 16), RL.el('span', { text: d.name })));
    });
    return wrap;
  }

  function markSwitcher(slug) {
    if (!dom) return;
    var links = dom.switcher.querySelectorAll('[data-slug]');
    for (var i = 0; i < links.length; i++) {
      if (links[i].getAttribute('data-slug') === slug) links[i].setAttribute('aria-current', 'page');
      else links[i].removeAttribute('aria-current');
    }
  }

  function notInData(slug, core) {
    var valid = (core.decks || []).map(function (d) { return d.slug; }).join(', ');
    return RL.el('div', { class: 'panel state' },
      RL.el('div', { class: 'state__icon' }, RL.svgIcon('alert-triangle', 28)),
      RL.el('h2', { class: 'state__title', text: 'not in my data: deck ‘' + slug + '’' }),
      RL.el('p', { class: 'state__body' },
        'There is no deck with that slug. Valid slugs: ',
        RL.el('strong', { text: valid || '(none loaded)' }), '.'),
      RL.el('p', { class: 'state__body' },
        RL.el('a', { class: 'btn btn--ghost', href: RL.href('lair') },
          RL.svgIcon('home', 16), RL.el('span', { text: 'Back to the Lair' }))));
  }

  function renderDeck(slug) {
    var core = RL.data('core');
    var deck = (core.decks || []).filter(function (d) { return d.slug === slug; })[0];
    var body = dom.body;
    RL.clear(body);
    closeDrawer();
    markSwitcher(deck ? slug : null);

    if (!deck) { body.appendChild(notInData(slug, core)); return; }

    var deckData = RL.data('deck:' + slug);

    body.appendChild(RL.el('section', { class: 'panel' }, deckHeader(deck, deckData)));
    body.appendChild(statsSection(deck));

    // card grid
    if (deckData && deckData.cards && deckData.cards.length) {
      var state = {
        q: '', colors: [], sort: 'cmc', mode: 'grid', countEl: null,
        onClear: null, setSort: null
      };
      var gridHost = RL.el('div');
      function rerender() {
        RL.clear(gridHost);
        gridHost.appendChild(buildGrid(deckData.cards, state, openDrawer));
        if (state.countEl) {
          var matched = deckData.cards.filter(function (c) { return cardMatches(c, state); });
          var total = matched.reduce(function (a, c) { return a + c.count; }, 0);
          state.countEl.textContent = RL.fmt.plural(total, 'card') +
            (matched.length !== deckData.cards.length ? ' of ' + deckData.cards.length : '');
        }
      }
      state.onClear = function () { state.q = ''; state.colors = []; rerender();
        // reset visible controls
        var pressed = toolbar.querySelectorAll('[aria-pressed="true"].colorfilter__btn');
        Array.prototype.forEach.call(pressed, function (b) { b.setAttribute('aria-pressed', 'false'); });
        var s = toolbar.querySelector('input[type="search"]'); if (s) s.value = '';
      };
      state.setSort = function (key) { state.sort = key; rerender(); };
      var toolbar = buildToolbar(deck, state, rerender);
      body.appendChild(RL.el('section', { class: 'panel' },
        RL.el('div', { class: 'panel__head' },
          RL.el('h2', { class: 'panel__title' },
            RL.svgIcon('search', 20), RL.el('span', { text: 'The 100 cards' }))),
        toolbar, gridHost));
      rerender();
    } else {
      body.appendChild(RL.el('section', { class: 'panel' },
        RL.el('div', { class: 'emptyfilter' },
          RL.el('p', null, 'The card list for this deck did not load. Expected ',
            RL.el('code', { class: 'md-code', text: 'dashboard/data/deck-' + slug + '.js' }), '.'))));
    }

    // documents
    if (deckData) body.appendChild(documentsSection(deckData));
  }

  function mount(el) {
    var core = RL.data('core');
    if (!core || !core.decks || !core.decks.length) {
      el.appendChild(RL.el('div', { class: 'panel state' },
        RL.el('div', { class: 'state__icon' }, RL.svgIcon('layers', 28)),
        RL.el('h2', { class: 'state__title', text: 'No decks are loaded' }),
        RL.el('p', { class: 'state__body' },
          'Run ', RL.el('code', { class: 'md-code', text: './bin/mtg dashboard --build' }), ' and reload.')));
      return;
    }
    el.appendChild(RL.el('h1', { class: 'section-title', text: 'Decks' }));
    el.appendChild(RL.el('p', { class: 'section-sub', text:
      'Each precon in full: the commander, the numbers behind the curve and the bracket, ' +
      'every card with its rulings, and the written primer.' }));
    var switcher = buildSwitcher(core);
    var body = RL.el('div');
    el.appendChild(switcher);
    el.appendChild(body);
    dom = { switcher: switcher, body: body };
  }

  RL.registerView({
    id: 'decks', label: 'Decks', icon: 'layers', mount: mount,
    onEnter: function (params) {
      if (!dom) return;
      var core = RL.data('core');
      var slug = params[0];
      if (!slug) {
        var first = (core.decks || [])[0];
        if (first) { RL.replace('decks', first.slug); return; }
      }
      if (slug !== currentSlug) {
        currentSlug = slug;
        renderDeck(slug);
      }
    },
    onLeave: function () { closeDrawer(); }
  });

  window.RLDeck = { cardFrame: cardFrame, openDrawer: openDrawer };

})(window, document);

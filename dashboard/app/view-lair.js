/* ============================================================================
   REMY'S LAIR — app/view-lair.js
   VIEW: "Lair" (#/lair) — the overview. The shelf, at a glance.

   What this view is FOR: three precons live here, and the one thing a beginner
   cannot see from any single deck page is how they compare. So the Lair leads
   with the three decks as cards you can walk into, then puts their mana curves
   side by side on one shared scale, then answers the question that decides every
   pre-game conversation — "what bracket is each of these, and why" — straight
   from the bracket data. It closes with an honest system panel: what is loaded,
   built when, and the promise that none of it touched the network.

   Constraints honoured:
     C1  zero LLM spend  — pure rendering of data/core.js + the deck payloads.
     C2  never invent    — every number is read from the payload the CLI wrote;
                           a Game Changer is only ever NAMED, never described,
                           because core.js carries the name and not the text.
     C5  offline-first   — no fetch, no CDN. Deck art is a local <img> that
                           degrades to a card-shaped placeholder on error.
     C6/no-build         — plain ES2019-ish script, no modules.
     C3  Commander only  — no other format is named anywhere in this file.

   Styling contract: assets/views-deck.css already defines every class used here
   (.decktile, .smalls, .gcwatch, .sysgrid, ...). This file produces the DOM that
   sheet expects; it invents no class names of its own.
   ========================================================================== */
(function (window, document) {
  'use strict';

  var RL = window.RL;
  if (!RL) return;

  RL.icons.bolt = '<path d="M13 2 4.5 13.2h6.2L10 22l8.5-11.2h-6.2z"/>';
  RL.icons.wifi = '<path d="M5 12.5a10 10 0 0 1 14 0"/><path d="M8.5 16a5 5 0 0 1 7 0"/>' +
                  '<path d="M2 9a15 15 0 0 1 20 0"/><path d="M12 20h.01"/>';

  var COLOR_KEYS = ['W', 'U', 'B', 'R', 'G'];

  /* ---- the card frame: a local <img>, or a card-shaped placeholder --------
     Shared visual language with the Decks grid and the Merge list. The <img>
     is optimistic; if the file is not on disk (art was never cached, or this
     is a fresh clone) it removes itself and the placeholder — which carries the
     card's real name and mana cost, the information the picture stood in for —
     is what remains. Never a broken-image glyph. */
  function cardFrame(name, manaCost, image, opts) {
    opts = opts || {};
    var frame = RL.el('div', { class: ['cardframe', opts.className || ''] });
    var ph = RL.el('div', { class: 'cardframe__ph' },
      RL.el('span', { class: 'cardframe__phname', text: name || 'Unknown card' }),
      manaCost ? RL.manaCost(manaCost) : null,
      RL.el('span', { class: 'cardframe__phnote', text: opts.note || 'art offline' })
    );
    frame.appendChild(ph);
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

  /* The commander card behind a deck slug — its image + mana cost live in the
     eagerly-loaded deck payload, not in core.js. Missing payload -> nulls, and
     the placeholder falls back to just the commander's name from core. */
  function commanderOf(slug) {
    var d = RL.data('deck:' + slug);
    if (!d || !d.cards) return null;
    for (var i = 0; i < d.cards.length; i++) {
      if (d.cards[i].board === 'commander') return d.cards[i];
    }
    return null;
  }

  function bracketBadge(n, opts) {
    opts = opts || {};
    var cls = ['bracketbadge'];
    if (n) cls.push('bracketbadge--' + n);
    return RL.el(opts.tag || 'span', { class: cls.concat(opts.className || []) },
      RL.svgIcon('shield', 14),
      RL.el('span', null, 'Bracket ',
        RL.el('span', { class: 'bracketbadge__n', text: n == null ? '?' : String(n) })));
  }

  /* ---- one deck tile ---------------------------------------------------- */
  function deckTile(deck) {
    var cmd = commanderOf(deck.slug);
    var art = cardFrame(
      cmd ? cmd.name : deck.commander,
      cmd ? cmd.mana_cost : '',
      cmd ? cmd.image : null,
      { alt: deck.commander + ', the commander of ' + deck.name }
    );

    var totals = deck.totals || {};
    var mv = deck.mana_value || {};
    var stats = RL.el('div', { class: 'decktile__stats' },
      statCell(RL.fmt.int(totals.lands), 'lands'),
      statCell(mv.avg_nonland != null ? RL.fmt.num(mv.avg_nonland, 2) : RL.fmt.dash, 'avg MV'),
      statCell(RL.fmt.int((deck.roles && deck.roles.ramp) || 0), 'ramp')
    );

    var pips = RL.el('div', { class: 'decktile__pips', aria: { label: 'Colour identity' } });
    (deck.color_identity || []).forEach(function (c) { pips.appendChild(RL.colorChip(c)); });

    return RL.el('a', {
      class: 'decktile', href: RL.href('decks', deck.slug),
      aria: { label: deck.name + ' — ' + deck.commander + ', Bracket ' + (deck.bracket || '?') }
    },
      RL.el('div', { class: 'decktile__art' }, art,
        RL.el('span', { class: 'decktile__badge' }, bracketBadge(deck.bracket))),
      RL.el('div', null,
        RL.el('div', { class: 'decktile__name', text: deck.name }),
        RL.el('div', { class: 'decktile__cmdr', text: deck.commander }),
        RL.el('div', { class: 'decktile__set', text:
          (deck.set_code || '—') + ' · released ' + RL.fmt.date(deck.release_date) }),
        pips),
      stats,
      RL.el('div', { class: 'decktile__go' },
        RL.el('span', { text: 'Open the deck' }), RL.svgIcon('chevron-right', 16))
    );
  }

  function statCell(value, label) {
    return RL.el('div', { class: 'decktile__stat' },
      RL.el('span', { class: 'decktile__statv', text: value }),
      RL.el('span', { class: 'decktile__statl', text: label }));
  }

  /* The merge is a PLAN, not a fourth box on the shelf. Dashed frame, plain
     ribbon, and a link into the Merge view rather than a deck page. */
  function mergeTile() {
    var merged = RL.data('merged');
    if (!merged) return null;
    var cmd = (merged.decklist || [])[0] || {};
    var art = cardFrame(cmd.name || 'Tidus, Yuna’s Guardian', cmd.mana_cost || '',
      cmd.image || null, { alt: 'The Bant merge', note: 'a plan' });
    var totals = merged.totals || {};
    return RL.el('a', {
      class: ['decktile', 'decktile--plan'], href: RL.href('merge'),
      aria: { label: 'The Bant merge — one deck built from two boxes' }
    },
      RL.el('span', { class: 'decktile__ribbon' },
        RL.svgIcon('git-merge', 12), RL.el('span', { text: 'A plan, not a box' })),
      RL.el('div', { class: 'decktile__art' }, art),
      RL.el('div', null,
        RL.el('div', { class: 'decktile__name', text: merged.name || 'Merged Bant' }),
        RL.el('div', { class: 'decktile__plannote', text:
          'Tidus and Bumbleflower share an exact colour identity, so their two boxes ' +
          'combine into one ' + RL.fmt.int(totals.cards || 100) + '-card deck with nothing bought.' })),
      RL.el('div', { class: 'decktile__go' },
        RL.el('span', { text: 'See the merge' }), RL.svgIcon('chevron-right', 16))
    );
  }

  /* ---- small-multiple mana curves, ONE shared scale --------------------- */
  var BUCKETS = ['0', '1', '2', '3', '4', '5', '6', '7+'];

  function curveSmall(deck, sharedMax) {
    var buckets = (deck.curve && deck.curve.buckets) || {};
    var W = 240, H = 96, padL = 4, padR = 4, padT = 8, padB = 16;
    var plotW = W - padL - padR, plotH = H - padT - padB;
    var n = BUCKETS.length;
    var gap = 6, barW = (plotW - gap * (n - 1)) / n;
    var top = sharedMax || 1;

    var svg = RL.svgEl('svg', {
      class: 'small__svg', viewBox: '0 0 ' + W + ' ' + H,
      preserveAspectRatio: 'xMidYMid meet', role: 'img',
      aria: { label: deck.name + ' mana curve — ' + BUCKETS.map(function (b) {
        return (buckets[b] || 0) + ' at ' + b; }).join(', ') }
    });
    svg.appendChild(RL.svgEl('title', { text: deck.name + ' mana curve' }));

    var baseY = padT + plotH;
    svg.appendChild(RL.svgEl('line', {
      x1: padL, x2: W - padR, y1: baseY, y2: baseY, stroke: 'var(--chart-axis)', 'stroke-width': 1 }));

    BUCKETS.forEach(function (b, i) {
      var v = buckets[b] || 0;
      var x = padL + i * (barW + gap);
      var h = top > 0 ? (v / top) * plotH : 0;
      var isPeak = deck.curve && deck.curve.peak_bucket === b && v > 0;
      if (h > 0.5) {
        svg.appendChild(RL.svgEl('rect', {
          x: x, y: baseY - h, width: barW, height: h, rx: 2,
          fill: isPeak ? 'var(--fel)' : 'var(--chart-single)' }));
      }
      svg.appendChild(RL.svgEl('text', {
        x: x + barW / 2, y: H - 4, 'text-anchor': 'middle',
        class: 'chart__catlabel', style: 'font-size:10px', text: b }));
    });
    return svg;
  }

  function smallsPanel(decks) {
    var sharedMax = 1;
    decks.forEach(function (d) {
      var b = (d.curve && d.curve.buckets) || {};
      BUCKETS.forEach(function (k) { sharedMax = Math.max(sharedMax, b[k] || 0); });
    });

    var grid = RL.el('div', { class: 'smalls' });
    decks.forEach(function (d) {
      var mv = d.mana_value || {};
      grid.appendChild(RL.el('div', { class: 'small' },
        RL.el('div', { class: 'small__head' },
          RL.el('span', { class: 'small__name', text: d.name }),
          RL.el('span', { class: 'small__note', text:
            'avg ' + (mv.avg_nonland != null ? RL.fmt.num(mv.avg_nonland, 2) : '—') })),
        curveSmall(d, sharedMax)));
    });

    return RL.el('section', { class: 'panel' },
      RL.el('div', { class: 'panel__head' },
        RL.el('h2', { class: 'panel__title' },
          RL.svgIcon('chart-bar', 20), RL.el('span', { text: 'Curves, side by side' }))),
      RL.el('p', { class: 'panel__sub' },
        'The maindeck non-land curve of each deck, drawn on one shared scale so the shapes ' +
        'compare honestly. The brightest bar is that deck’s peak.'),
      grid,
      RL.el('p', { class: 'scale-note', text:
        'Same vertical scale across all three (tallest bar = ' + sharedMax + ' cards). ' +
        'Lands and the commander are excluded, exactly as `mtg deck stats` reports them.' })
    );
  }

  /* ---- bracket watch ---------------------------------------------------- */
  function bracketWatch(decks) {
    var flagged = decks.filter(function (d) { return (d.game_changers || []).length; });
    var topDeck = decks.slice().sort(function (a, b) { return (b.bracket || 0) - (a.bracket || 0); })[0];
    var cmd = topDeck ? commanderOf(topDeck.slug) : null;

    var lead;
    if (flagged.length) {
      lead = RL.el('p', { class: 'gcwatch__lead' },
        'Brackets 1 and 2 both require ', RL.el('strong', { text: 'zero Game Changers' }),
        '. ',
        flagged.length === 1
          ? RL.frag(RL.el('strong', { text: flagged[0].name }), ' is the only deck here that runs one — ',
              RL.el('strong', { text: flagged[0].game_changers.join(', ') }),
              ' — which lifts it to Bracket ' + flagged[0].bracket + '. Cut that one card and it drops to Bracket 2.')
          : RL.el('span', { text: flagged.length + ' decks carry a Game Changer; see the list below.' })
      );
    } else {
      lead = RL.el('p', { class: 'gcwatch__lead' },
        'None of the three decks runs a Game Changer, so every one of them sits at ',
        RL.el('strong', { text: 'Bracket 2 or below' }),
        ' on that signal alone.');
    }

    var list = RL.el('ul', { class: 'gcwatch__list' });
    decks.forEach(function (d) {
      var gc = (d.game_changers || []);
      list.appendChild(RL.el('li', null,
        RL.el('a', { href: RL.href('decks', d.slug), text: d.name }),
        ' — Bracket ' + (d.bracket == null ? '?' : d.bracket) +
        (gc.length ? ' · ' + RL.fmt.plural(gc.length, 'Game Changer') + ': ' + gc.join(', ')
                   : ' · no Game Changers')));
    });

    var body = RL.el('div', null, lead, list,
      RL.el('p', { class: 'scale-note', text:
        'Bracket and Game-Changer counts come straight from `mtg deck bracket`. ' +
        'Verify any of them live before you repeat it at the table.' }));

    var art = cmd
      ? RL.el('div', { class: 'gcwatch__art' },
          cardFrame(cmd.name, cmd.mana_cost, cmd.image, { alt: cmd.name }))
      : null;

    return RL.el('section', { class: 'panel' },
      RL.el('div', { class: 'panel__head' },
        RL.el('h2', { class: 'panel__title' },
          RL.svgIcon('shield', 20), RL.el('span', { text: 'Bracket watch' }))),
      RL.el('div', { class: 'gcwatch' }, art || RL.el('div'), body)
    );
  }

  /* ---- system panel ----------------------------------------------------- */
  function systemPanel(core) {
    var tables = (core.db && core.db.tables) || {};
    var counts = [
      ['cards', tables.cards], ['rulings', tables.rulings], ['rules', tables.rules],
      ['glossary terms', tables.glossary], ['decks', tables.decks]
    ];
    var rowcounts = RL.el('ul', { class: 'rowcounts' });
    counts.forEach(function (pair) {
      if (pair[1] == null) return;
      rowcounts.appendChild(RL.el('li', null,
        RL.el('strong', { text: RL.fmt.int(pair[1]) }), ' ' + pair[0]));
    });

    var grid = RL.el('div', { class: 'sysgrid' },
      RL.stat('Database', RL.fmt.bytes((core.db && core.db.size_bytes) || 0), { note: 'local SQLite' }),
      RL.stat('Built', RL.fmt.date(core.generated_at), { note: 'from the database', tone: 'fel' }),
      RL.stat('Cost to run', '$0.00', { note: 'no API, no inference' })
    );

    return RL.el('section', { class: 'panel panel--quiet' },
      RL.el('div', { class: 'panel__head' },
        RL.el('h2', { class: 'panel__title' },
          RL.svgIcon('database', 20), RL.el('span', { text: 'The brain, offline' })),
        RL.el('div', { class: 'panel__actions' },
          RL.el('span', { class: 'offline-badge' },
            RL.svgIcon('wifi', 14), RL.el('span', { text: 'network off · nothing billed' })))),
      RL.el('p', { class: 'panel__sub' },
        'Everything Remy’s Lair draws is sitting in one local database. The page never ' +
        'opens a socket — it renders files that ',
        RL.el('code', { class: 'md-code', text: 'mtg dashboard --build' }), ' wrote.'),
      grid,
      rowcounts
    );
  }

  /* ==========================================================================
     mount
     ====================================================================== */
  function mount(el) {
    var core = RL.data('core');
    if (!core || !core.decks || !core.decks.length) {
      el.appendChild(RL.el('div', { class: 'panel state' },
        RL.el('div', { class: 'state__icon' }, RL.svgIcon('home', 28)),
        RL.el('h2', { class: 'state__title', text: 'The Lair has no decks to show' }),
        RL.el('p', { class: 'state__body' },
          RL.el('code', { class: 'md-code', text: 'dashboard/data/core.js' }),
          ' did not register any decks. Run ',
          RL.el('code', { class: 'md-code', text: './bin/mtg dashboard --build' }),
          ' and reload.')));
      return;
    }

    var decks = core.decks;
    el.appendChild(RL.el('h1', { class: 'section-title', text: 'Remy’s Lair' }));
    el.appendChild(RL.el('p', { class: 'lair__lede', text:
      'Three preconstructed Commander decks, one shelf. Walk into any of them for the full ' +
      'list, the curve, and the primer — or compare all three below before you pick one up.' }));

    var tiles = RL.el('div', { class: 'decktiles' });
    decks.forEach(function (d) { tiles.appendChild(deckTile(d)); });
    var plan = mergeTile();
    if (plan) tiles.appendChild(plan);
    el.appendChild(tiles);

    el.appendChild(smallsPanel(decks));
    el.appendChild(bracketWatch(decks));
    el.appendChild(systemPanel(core));
  }

  RL.registerView({ id: 'lair', label: 'Lair', icon: 'home', mount: mount });

})(window, document);

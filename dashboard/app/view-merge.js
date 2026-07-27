/* ============================================================================
   REMY'S LAIR — app/view-merge.js
   VIEW: "Merge" (#/merge) — the Bant merge, one deck out of two boxes.

   What this view is FOR: Tidus and Bumbleflower share an EXACT colour identity,
   so their two precons combine into a single 100-card deck with nothing bought.
   That merge is a PLAN, not a database deck — `mtg deck merged-bant` correctly
   answers "not in my data". This view renders the plan the exporter read out of
   decks/merged-bant/: the 100-card list grouped by type, the write-up, and a
   copy-paste block for a deck-builder.

   Constraints honoured:
     C1  zero LLM spend  — pure rendering of data/merged.js.
     C2  never invent    — a card the exporter could NOT resolve against the DB is
                           shown as an explicit "not in my data" row, never as a
                           plausible-looking card. Prices and ranks are payload
                           fields, never estimated.
     C5  offline-first   — no fetch; art is a local <img> with a placeholder.
     C6/no-build         — plain ES2019-ish script.
     C3  Commander only  — singleton, one commander; no other format named.
   ========================================================================== */
(function (window, document) {
  'use strict';

  var RL = window.RL;
  if (!RL) return;

  var TYPE_ORDER = ['Commander', 'Creature', 'Planeswalker', 'Instant', 'Sorcery',
                    'Artifact', 'Enchantment', 'Battle', 'Land', 'Other'];

  function cardFrame(name, manaCost, image, opts) {
    opts = opts || {};
    if (window.RLDeck && window.RLDeck.cardFrame) return window.RLDeck.cardFrame(name, manaCost, image, opts);
    var frame = RL.el('div', { class: 'cardframe' });
    frame.appendChild(RL.el('div', { class: 'cardframe__ph' },
      RL.el('span', { class: 'cardframe__phname', text: name || 'Unknown card' }),
      manaCost ? RL.manaCost(manaCost) : null,
      RL.el('span', { class: 'cardframe__phnote', text: opts.note || 'art offline' })));
    return frame;
  }

  function totalPrice(decklist) {
    var sum = 0, missing = 0;
    decklist.forEach(function (e) {
      if (e.unresolved) return;
      var p = parseFloat(e.price_usd);
      if (isFinite(p)) sum += p * (e.count || 1); else missing++;
    });
    return { sum: sum, missing: missing };
  }

  function copyLines(decklist) {
    return decklist.map(function (e) { return (e.count || 1) + ' ' + e.name; }).join('\n');
  }

  /* ---- the grouped 100-card list ---------------------------------------- */
  function decklistSection(merged) {
    var decklist = merged.decklist || [];
    var byType = merged.by_type || {};
    var order = TYPE_ORDER.filter(function (t) { return byType[t]; })
      .concat(Object.keys(byType).filter(function (t) { return TYPE_ORDER.indexOf(t) < 0; }));

    var groups = {};
    decklist.forEach(function (e) {
      var g = e.type_group || (e.unresolved ? 'Unresolved' : 'Other');
      (groups[g] || (groups[g] = [])).push(e);
    });
    if (groups.Unresolved && order.indexOf('Unresolved') < 0) order.push('Unresolved');

    var wrap = RL.el('div', { class: 'mergelist' });
    order.forEach(function (type) {
      var entries = groups[type];
      if (!entries || !entries.length) return;
      var count = entries.reduce(function (a, e) { return a + (e.count || 1); }, 0);
      var list = RL.el('ul', { class: 'mergegroup__items' });
      entries.forEach(function (e) { list.appendChild(mergeRow(e)); });
      wrap.appendChild(RL.el('section', { class: 'mergegroup' },
        RL.el('div', { class: 'cardgroup__head' },
          RL.el('h3', { class: 'cardgroup__title', text: type }),
          RL.el('span', { class: 'cardgroup__count', text: RL.fmt.plural(count, 'card') }),
          RL.el('span', { class: 'cardgroup__rule', 'aria-hidden': 'true' })),
        list));
    });
    return wrap;
  }

  function mergeRow(e) {
    if (e.unresolved) {
      return RL.el('li', { class: 'mergerow mergerow--unresolved' },
        RL.svgIcon('alert-triangle', 16),
        RL.el('span', { class: 'mergerow__name', text: e.name }),
        RL.el('span', { class: 'mergerow__gap', text: 'not in my data — the exporter could not match this name to a card' }));
    }
    return RL.el('li', { class: 'mergerow' },
      RL.el('span', { class: 'mergerow__qty mono', text: (e.count || 1) + '×' }),
      RL.el('a', { class: 'mergerow__name', href: RL.href('cards', e.name),
        title: 'Look this card up in Cards' }, e.name),
      e.mana_cost ? RL.manaCost(e.mana_cost) : RL.el('span'),
      RL.el('span', { class: 'mergerow__price mono', text: e.price_usd ? RL.fmt.price(e.price_usd) : RL.fmt.dash }));
  }

  /* ---- the write-up (MERGED-BANT.md) ------------------------------------ */
  function docSection(merged) {
    if (!merged.doc) return null;
    return RL.el('section', { class: 'panel' },
      RL.el('div', { class: 'panel__head' },
        RL.el('h2', { class: 'panel__title' },
          RL.svgIcon('scroll', 20), RL.el('span', { text: 'The merge, explained' }))),
      RL.el('p', { class: 'panel__sub', text: 'From decks/merged-bant/MERGED-BANT.md — rendered verbatim.' }),
      RL.mdEl(merged.doc));
  }

  function copyButton(text, label) {
    var btn = RL.el('button', { class: 'btn btn--ghost', type: 'button',
      on: { click: function () {
        RL.copy(text).then(function (ok) {
          RL.clear(btn);
          btn.appendChild(RL.svgIcon(ok ? 'check' : 'alert-triangle', 16));
          btn.appendChild(RL.el('span', { text: ok ? 'Copied' : 'Copy failed' }));
          RL.toast(ok ? 'The decklist is on your clipboard' : 'Could not reach the clipboard — select the text instead',
            { tone: ok ? 'good' : 'bad' });
          window.setTimeout(function () {
            RL.clear(btn); btn.appendChild(RL.svgIcon('copy', 16)); btn.appendChild(RL.el('span', { text: label }));
          }, 2000);
        });
      } } },
      RL.svgIcon('copy', 16), RL.el('span', { text: label }));
    return btn;
  }

  /* ==========================================================================
     mount
     ====================================================================== */
  function mount(el) {
    var merged = RL.data('merged');
    if (!merged || !merged.decklist) {
      el.appendChild(RL.el('div', { class: 'panel state' },
        RL.el('div', { class: 'state__icon' }, RL.svgIcon('git-merge', 28)),
        RL.el('h2', { class: 'state__title', text: 'The merge has not been built' }),
        RL.el('p', { class: 'state__body' },
          RL.el('code', { class: 'md-code', text: 'dashboard/data/merged.js' }),
          ' did not register. It comes from decks/merged-bant/DECKLIST.md via ',
          RL.el('code', { class: 'md-code', text: './bin/mtg dashboard --build' }), '.')));
      return;
    }

    var totals = merged.totals || {};
    var price = totalPrice(merged.decklist);
    var unresolved = (merged.decklist || []).filter(function (e) { return e.unresolved; });
    var cmd = (merged.decklist || [])[0] || {};

    el.appendChild(RL.el('h1', { class: 'section-title', text: merged.name || 'The Bant Merge' }));
    el.appendChild(RL.el('p', { class: 'section-sub' },
      'One deck built from the Tidus and Bumbleflower boxes — they share an exact colour ' +
      'identity, so nothing needs buying. This is a plan on disk, not a loaded deck: ',
      RL.el('code', { class: 'md-code', text: 'mtg deck merged-bant' }),
      ' answers ', RL.el('em', { text: '“not in my data.”' })));

    // header: commander art + totals + actions
    var stats = RL.el('div', { class: 'statrow' },
      RL.stat('Cards', RL.fmt.int(totals.cards), { tone: 'fel',
        note: RL.fmt.int(totals.lands) + ' lands · ' + RL.fmt.int(totals.nonlands) + ' non-lands' }),
      RL.stat('Distinct entries', RL.fmt.int(totals.entries || (merged.decklist || []).length)),
      RL.stat('Rough price', RL.fmt.price(price.sum),
        { note: price.missing ? price.missing + ' without a price' : 'from the card table' })
    );

    var actions = RL.el('div', { class: 'row', style: { marginTop: 'var(--s-4)' } },
      copyButton(copyLines(merged.decklist), 'Copy decklist'));

    var header = RL.el('section', { class: 'panel' },
      RL.el('div', { class: 'gcwatch' },
        RL.el('div', { class: 'gcwatch__art' },
          cardFrame(cmd.name || 'Commander', cmd.mana_cost || '', cmd.image || null,
            { alt: (cmd.name || 'commander') + ' card art', note: 'the merge’s commander' })),
        RL.el('div', null,
          RL.el('p', { class: 'gcwatch__lead' },
            RL.el('strong', { text: cmd.name || 'The commander' }),
            ' leads a ', RL.el('strong', { text: RL.fmt.int(totals.cards) + '-card' }),
            ' singleton deck. Every card below is a real row in the database — except any ',
            'flagged as ', RL.el('em', { text: 'not in my data' }), ', which the exporter could not match.'),
          stats, actions)));
    el.appendChild(header);

    if (unresolved.length) {
      el.appendChild(RL.el('div', { class: 'panel verdict verdict--warn', style: { marginTop: 'var(--s-5)' } },
        RL.el('div', { class: 'verdict__head' }, RL.svgIcon('alert-triangle', 16),
          RL.el('span', { text: RL.fmt.plural(unresolved.length, 'unresolved card') })),
        RL.el('p', null, 'The list names ' + RL.fmt.plural(unresolved.length, 'card') +
          ' the exporter could not find in the cards table: ',
          RL.el('strong', { text: unresolved.map(function (e) { return e.name; }).join(', ') }),
          '. They are shown below exactly as written, not guessed at.')));
    }

    // the list
    el.appendChild(RL.el('section', { class: 'panel' },
      RL.el('div', { class: 'panel__head' },
        RL.el('h2', { class: 'panel__title' },
          RL.svgIcon('git-merge', 20), RL.el('span', { text: 'The 100 cards' })),
        RL.el('div', { class: 'panel__actions' },
          RL.el('span', { class: 'chip', text: 'grouped by type' }))),
      RL.el('p', { class: 'panel__sub', text:
        'Card names link into the Cards search, where the full text and legality live.' }),
      decklistSection(merged)));

    // the write-up
    var doc = docSection(merged);
    if (doc) el.appendChild(doc);
  }

  RL.registerView({ id: 'merge', label: 'Merge', icon: 'git-merge', mount: mount });

})(window, document);

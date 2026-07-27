/* ============================================================================
   REMY'S LAIR — app/view-learning.js
   VIEW: "Learning" (#/learning) — the loop that compounds.

   What this view is FOR: MTG Brain logs every rule Omar gets wrong and every
   game he plays. The CLI writes those to the database and regenerates two study
   documents; this view reads the structured records back and does the one thing
   a flat document cannot — RANK the missed rules by how often he trips on each,
   surface the worst offender, and link every rule number straight into the Rules
   view with its verbatim text already attached.

   Constraints honoured:
     C1  zero LLM spend  — pure rendering of core.learning. No inference.
     C2  never invent    — the Comprehensive Rules text beside each miss is the
                           verbatim `rule_text` the exporter attached; where the
                           rule was not found it says "not in my data", never a
                           paraphrase. Notes are Omar's own words, shown as-is.
     C5  offline-first   — no fetch, no CDN.
     C6/no-build         — plain ES2019-ish script.
     C3  Commander only  — game results are win/loss/draw in a Commander pod.
   ========================================================================== */
(function (window, document) {
  'use strict';

  var RL = window.RL;
  if (!RL) return;

  RL.icons.trophy = '<path d="M7 4h10v4a5 5 0 0 1-10 0z"/><path d="M7 6H4.5a2.5 2.5 0 0 0 2.5 2.5"/>' +
                    '<path d="M17 6h2.5A2.5 2.5 0 0 1 17 8.5"/><path d="M9.5 13.5h5"/>' +
                    '<path d="M12 13.5V17"/><path d="M8.5 20.5h7"/><path d="M10 17h4v3.5h-4z"/>';
  RL.icons.target = '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.6"/><circle cx="12" cy="12" r="1"/>';

  var RESULT_META = {
    win: { label: 'Win', chip: 'chip--good', icon: 'trophy' },
    loss: { label: 'Loss', chip: 'chip--bad', icon: 'x' },
    draw: { label: 'Draw', chip: 'chip--warn', icon: 'info' }
  };

  function deckName(slug) {
    var core = RL.data('core');
    var d = core && (core.decks || []).filter(function (x) { return x.slug === slug; })[0];
    return d ? d.name : slug;
  }

  /* ---- group misses by rule number, ranked by frequency ----------------- */
  function rankMisses(missed) {
    var by = {};
    missed.forEach(function (m) {
      var key = m.rule_number;
      if (!by[key]) by[key] = { rule_number: key, rule_text: m.rule_text, count: 0, notes: [] };
      by[key].count += 1;
      // keep any non-null rule_text we see
      if (!by[key].rule_text && m.rule_text) by[key].rule_text = m.rule_text;
      by[key].notes.push({ note: m.what_i_got_wrong, at: m.logged_at });
    });
    return Object.keys(by).map(function (k) { return by[k]; })
      .sort(function (a, b) { return b.count - a.count || String(a.rule_number).localeCompare(String(b.rule_number)); });
  }

  function ruleLink(n, text) {
    var R = window.RLRules;
    var href = R && R.href ? R.href(n) : RL.href('rules', n);
    return RL.el('a', { class: 'learn__rulelink', href: href }, RL.el('span', { class: 'mono', text: text || ('rule ' + n) }));
  }

  /* ---- one missed-rule card --------------------------------------------- */
  function missCard(m, rank) {
    var head = RL.el('div', { class: 'miss__head' },
      RL.el('span', { class: ['miss__rank', rank === 0 ? 'is-top' : ''], text: '#' + (rank + 1) }),
      ruleLink(m.rule_number, 'Rule ' + m.rule_number),
      RL.el('span', { class: ['chip', m.count >= 2 ? 'chip--warn' : ''],
        text: RL.fmt.plural(m.count, 'miss', 'misses') }));

    var card = RL.el('article', { class: ['miss', m.count >= 2 ? 'miss--repeat' : ''] }, head);

    // verbatim CR text, or an honest gap
    if (m.rule_text) {
      card.appendChild(RL.el('div', { class: 'miss__ruletext' },
        window.RLRules && window.RLRules.linkify ? window.RLRules.linkify(m.rule_text)
                                                  : document.createTextNode(m.rule_text)));
    } else {
      card.appendChild(RL.el('p', { class: 'miss__gap' },
        RL.svgIcon('alert-triangle', 14),
        RL.el('span', { text: 'not in my data: rule ' + m.rule_number + ' has no text in this build.' })));
    }

    // Omar's notes, one per occurrence
    var notes = RL.el('ul', { class: 'miss__notes' });
    m.notes.forEach(function (n) {
      notes.appendChild(RL.el('li', null,
        RL.el('span', { class: 'miss__notedate mono', text: RL.fmt.date(n.at) }),
        RL.el('span', { class: 'miss__notetext', text: n.note || '—' })));
    });
    card.appendChild(notes);
    return card;
  }

  function missesPanel(missed) {
    var ranked = rankMisses(missed);
    var panel = RL.el('section', { class: 'panel' },
      RL.el('div', { class: 'panel__head' },
        RL.el('h2', { class: 'panel__title' },
          RL.svgIcon('target', 20), RL.el('span', { text: 'Rules I keep missing' })),
        RL.el('div', { class: 'panel__actions' },
          RL.el('span', { class: 'chip', text: RL.fmt.plural(ranked.length, 'distinct rule') }))));

    if (!ranked.length) {
      panel.appendChild(RL.el('div', { class: 'emptyfilter' },
        RL.el('p', null, 'Nothing logged yet — a clean sheet.'),
        RL.el('p', { class: 'muted' }, 'Log one with ',
          RL.el('code', { class: 'md-code', text: 'mtg log rule --rule 903.4 --note "…"' }), '.')));
      return panel;
    }

    var top = ranked[0];
    if (top.count >= 2) {
      panel.appendChild(RL.el('p', { class: 'learn__lede' },
        'The one to study first is ', ruleLink(top.rule_number, 'rule ' + top.rule_number),
        ' — missed ', RL.el('strong', { text: RL.fmt.plural(top.count, 'time') }),
        '. It is at the top of the study plan until it stops coming up.'));
    } else {
      panel.appendChild(RL.el('p', { class: 'panel__sub', text:
        'Every rule logged as missed, most-missed first, with the Comprehensive Rules text verbatim.' }));
    }

    var list = RL.el('div', { class: 'misslist' });
    ranked.forEach(function (m, i) { list.appendChild(missCard(m, i)); });
    panel.appendChild(list);
    return panel;
  }

  /* ---- game log --------------------------------------------------------- */
  function gamesPanel(games) {
    var w = 0, l = 0, d = 0;
    games.forEach(function (g) {
      if (g.result === 'win') w++; else if (g.result === 'loss') l++; else if (g.result === 'draw') d++;
    });

    var panel = RL.el('section', { class: 'panel' },
      RL.el('div', { class: 'panel__head' },
        RL.el('h2', { class: 'panel__title' },
          RL.svgIcon('activity', 20), RL.el('span', { text: 'Game log' })),
        RL.el('div', { class: 'panel__actions' },
          RL.el('span', { class: 'chip chip--good', text: w + 'W' }),
          RL.el('span', { class: 'chip chip--bad', text: l + 'L' }),
          RL.el('span', { class: 'chip chip--warn', text: d + 'D' }))));

    if (!games.length) {
      panel.appendChild(RL.el('div', { class: 'emptyfilter' },
        RL.el('p', null, 'No games logged yet.'),
        RL.el('p', { class: 'muted' }, 'Log one with ',
          RL.el('code', { class: 'md-code', text: 'mtg log game --deck tidus --result win …' }), '.')));
      return panel;
    }

    panel.appendChild(RL.el('p', { class: 'panel__sub', text:
      RL.fmt.plural(games.length, 'game') + ' recorded, newest first. The notes are Omar’s own.' }));

    var list = RL.el('ul', { class: 'gamelog' });
    games.forEach(function (g) {
      var meta = RESULT_META[g.result] || { label: g.result || '—', chip: '', icon: 'info' };
      var row = RL.el('li', { class: 'game' },
        RL.el('div', { class: 'game__top' },
          RL.el('span', { class: ['chip', meta.chip, 'game__result'] },
            RL.svgIcon(meta.icon, 14), RL.el('span', { text: meta.label })),
          g.deck_id
            ? RL.el('a', { class: 'game__deck', href: RL.href('decks', g.deck_id), text: deckName(g.deck_id) })
            : RL.el('span', { class: 'game__deck', text: '—' }),
          RL.el('span', { class: 'game__date mono', text: RL.fmt.date(g.played_at) })),
        g.opponents ? RL.el('div', { class: 'game__vs' },
          RL.el('span', { class: 'game__vslabel', text: 'vs' }),
          RL.el('span', { text: g.opponents })) : null,
        g.notes ? RL.el('p', { class: 'game__notes', text: g.notes }) : null);
      list.appendChild(row);
    });
    panel.appendChild(list);
    return panel;
  }

  /* ==========================================================================
     mount
     ====================================================================== */
  function mount(el) {
    var core = RL.data('core');
    var learning = core && core.learning;
    if (!learning) {
      el.appendChild(RL.el('div', { class: 'panel state' },
        RL.el('div', { class: 'state__icon' }, RL.svgIcon('activity', 28)),
        RL.el('h2', { class: 'state__title', text: 'The learning log has not been built' }),
        RL.el('p', { class: 'state__body' },
          RL.el('code', { class: 'md-code', text: 'dashboard/data/core.js' }),
          ' carries no learning record. Run ',
          RL.el('code', { class: 'md-code', text: './bin/mtg dashboard --build' }), ' and reload.')));
      return;
    }

    var missed = learning.rules_missed || [];
    var games = learning.game_log || [];

    el.appendChild(RL.el('h1', { class: 'section-title', text: 'Learning' }));
    el.appendChild(RL.el('p', { class: 'section-sub' },
      'The part that compounds. Every missed rule and every game is captured, so the ' +
      'weak spots surface on their own — this is the study plan, ranked by what keeps catching you out.'));

    var stats = RL.el('div', { class: 'statrow' },
      RL.stat('Games logged', RL.fmt.int(games.length),
        { note: games.length ? RL.fmt.date(games[0].played_at) + ' — latest' : 'none yet' }),
      RL.stat('Rules missed', RL.fmt.int(missed.length),
        { tone: missed.length ? 'warn' : undefined,
          note: RL.fmt.plural(rankMisses(missed).length, 'distinct rule') }),
      RL.stat('Study first', rankMisses(missed).length ? 'Rule ' + rankMisses(missed)[0].rule_number : '—',
        { tone: 'fel', note: 'top of the plan' })
    );
    el.appendChild(RL.el('section', { class: 'panel panel--quiet' }, stats));

    el.appendChild(missesPanel(missed));
    el.appendChild(gamesPanel(games));
  }

  RL.registerView({ id: 'learning', label: 'Learning', icon: 'activity', mount: mount });

})(window, document);

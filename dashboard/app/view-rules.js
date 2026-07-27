/* ============================================================================
   REMY'S LAIR — app/view-rules.js
   VIEW: "Rules" (#/rules, #/rules/<number>) — the 3,309 Comprehensive Rules.

   What this view is FOR: the CLI can print one rule at a time. A browser can
   show you where that rule LIVES — its section, its parent, its subrules, and
   every rule it points at. That last part is the whole point: the CR is a
   hypertext document that has never been hyperlinked. Here it is.

   Constraints honoured:
     C1  zero LLM spend  — pure rendering of data/rules.js. No inference.
     C5  offline-first   — no fetch, no CDN, no remote anything.
     C6/no-build         — plain ES2019-ish script, no modules.
     C3  Commander only  — no other format is named anywhere in this file.

   VERBATIM RULE: rule text is never reworded, trimmed, or summarised. It is
   inserted as text nodes; the only thing layered on top is <a> around a
   cross-reference and <mark> around a search hit. Both wrap the SAME
   characters that were already there.

   Cross-reference linking is VERIFIED, never optimistic: a reference is only
   turned into a link if that exact rule number is present in the index. An
   unresolvable reference stays plain text, which is the honest outcome.

   Exports window.RLRules for the Glossary view (index + linkifier). If this
   file is absent, Glossary degrades to plain text — it checks.
   ========================================================================== */
(function (window, document) {
  'use strict';

  var RL = window.RL;
  if (!RL) return;

  /* Extend the shared icon set — never an emoji, never an image. */
  RL.icons.hash = '<path d="M9.8 3.6 7.6 20.4"/><path d="M16.6 3.6 14.4 20.4"/>' +
                  '<path d="M4.2 8.9h15.6"/><path d="M3.4 15.3h15.6"/>';
  RL.icons.link = '<path d="M10.4 13.6a4.2 4.2 0 0 0 6 0l3-3a4.2 4.2 0 1 0-6-6l-1.7 1.7"/>' +
                  '<path d="M13.6 10.4a4.2 4.2 0 0 0-6 0l-3 3a4.2 4.2 0 1 0 6 6l1.7-1.7"/>';
  RL.icons.compass = '<circle cx="12" cy="12" r="9"/><path d="m15.6 8.4-2 5.2-5.2 2 2-5.2z"/>';

  /* ==========================================================================
     1. THE INDEX
     data/rules.js gives us rows of [number, section, parent, text]. Everything
     below is derived from that once, on first use, and then reused.
     ====================================================================== */
  var idx = null;

  function buildIndex() {
    if (idx) return idx;
    var payload = RL.data('rules');
    if (!payload || !payload.rules || !payload.rules.length) return null;

    var by = Object.create(null);
    var kids = Object.create(null);
    var roots = [];
    var lower = [];
    var all = [];

    payload.rules.forEach(function (row, i) {
      var o = {
        number: String(row[0]),
        section: row[1] === null || row[1] === undefined ? '' : String(row[1]),
        parent: row[2] === null || row[2] === undefined ? null : String(row[2]),
        text: String(row[3] === null || row[3] === undefined ? '' : row[3]),
        i: i
      };
      by[o.number] = o;
      all.push(o);
      lower.push((o.number + ' ' + o.text).toLowerCase());
    });

    all.forEach(function (o) {
      if (o.parent && by[o.parent]) (kids[o.parent] || (kids[o.parent] = [])).push(o.number);
      else roots.push(o.number);
    });

    idx = {
      by: by, kids: kids, roots: roots, all: all, lower: lower,
      glossary: payload.glossary || [],
      docs: payload.docs || {}
    };
    return idx;
  }

  /* "Rule 601.2A." / "CR 601.2a" / " 601.2a " all normalise to "601.2a". */
  function normNum(s) {
    return String(s === null || s === undefined ? '' : s)
      .trim().toLowerCase()
      .replace(/^(?:cr|rules?|sections?)\s*/, '')
      .replace(/[.,;:'"\u201c\u201d]+$/, '')
      .replace(/\s+/g, '');
  }

  function getRule(n) {
    var i = buildIndex();
    if (!i) return null;
    var k = normNum(n);
    return Object.prototype.hasOwnProperty.call(i.by, k) ? i.by[k] : null;
  }

  function childrenOf(n) {
    var i = buildIndex();
    return (i && i.kids[n]) || [];
  }

  function ancestorsOf(n) {
    var chain = [], r = getRule(n), guard = 0;
    while (r && r.parent && guard++ < 12) {
      var p = getRule(r.parent);
      if (!p) break;
      chain.unshift(p);
      r = p;
    }
    return chain;
  }

  /* A section heading ("Casting Spells") vs a rule body. Roots and subsections
     carry short titles; everything deeper is prose. Used only for layout. */
  function isHeading(rule) {
    return !!rule && rule.text.length < 60 && rule.text.indexOf('.') === -1;
  }

  function shortText(rule, n) {
    var t = rule.text;
    return t.length > n ? t.slice(0, n - 1).replace(/\s+\S*$/, '') + '\u2026' : t;
  }

  /* ==========================================================================
     2. CROSS-REFERENCE LINKING
     The CR is riddled with "see rule 601.2b", "rule 702.64, “Absorb,”" and bare
     "601.2f". All three forms are matched, and EVERY match is checked against
     the index before it becomes a link. 1,031 references inside rule text and
     768 inside the glossary currently resolve; anything that does not stays as
     plain text rather than becoming a dead link.
     ====================================================================== */
  var REF_SRC = '\\b(rules?|sections?)\\s+(\\d{1,3}(?:\\.\\d+[a-z]?)?)|(\\d{3}\\.\\d+[a-z]?)';

  function isWordish(ch) { return ch !== '' && /[0-9A-Za-z]/.test(ch); }

  /* -> DocumentFragment. Text nodes stay verbatim; only <a> is added. */
  function linkifyText(str) {
    var frag = document.createDocumentFragment();
    var text = String(str === null || str === undefined ? '' : str);
    var i = buildIndex();
    if (!i || !text) {
      if (text) frag.appendChild(document.createTextNode(text));
      return frag;
    }

    var re = new RegExp(REF_SRC, 'gi');
    var last = 0, m;

    while ((m = re.exec(text)) !== null) {
      var whole = m[0];
      var start = m.index;
      var after = text.charAt(start + whole.length);
      var num, label;

      if (m[3] !== undefined) {
        // bare "601.2f" — reject if glued to another token on either side
        var prev = start > 0 ? text.charAt(start - 1) : '';
        if (isWordish(prev) || prev === '.' || isWordish(after)) continue;
        num = normNum(m[3]);
        label = m[3];
      } else {
        if (isWordish(after)) continue;      // "rule 6013" is not rule 601
        num = normNum(m[2]);
        label = whole;                        // link the whole "rule 601.2b" phrase
      }

      var target = Object.prototype.hasOwnProperty.call(i.by, num) ? i.by[num] : null;
      if (!target) continue;                  // VERIFY BEFORE LINKING — else plain text

      if (start > last) frag.appendChild(document.createTextNode(text.slice(last, start)));
      frag.appendChild(RL.el('a', {
        class: 'xref',
        href: RL.href('rules', target.number),
        title: target.number + ' \u2014 ' + shortText(target, 90)
      }, label));
      last = start + whole.length;
    }

    if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
    return frag;
  }

  var SKIP_TAGS = { A: 1, CODE: 1, PRE: 1, MARK: 1, BUTTON: 1, TEXTAREA: 1 };

  function inSkipped(node, root) {
    for (var p = node.parentNode; p && p !== root; p = p.parentNode) {
      if (p.nodeType === 1 && SKIP_TAGS[p.tagName]) return true;
    }
    return false;
  }

  function collectTextNodes(root) {
    var walker = document.createTreeWalker(root, window.NodeFilter.SHOW_TEXT, null, false);
    var out = [], n;
    while ((n = walker.nextNode())) {
      if (n.nodeValue && n.nodeValue.trim() && !inSkipped(n, root)) out.push(n);
    }
    return out;
  }

  /* Linkify rule references inside already-rendered HTML (used for Omar's
     markdown glossary). Walks text nodes only, so no markup can be corrupted. */
  function linkifyElement(root) {
    if (!root) return root;
    collectTextNodes(root).forEach(function (node) {
      var frag = linkifyText(node.nodeValue);
      if (frag.childNodes.length > 1) node.parentNode.replaceChild(frag, node);
    });
    return root;
  }

  /* ==========================================================================
     3. SEARCH-TERM HIGHLIGHTING
     <mark> wraps the exact characters already present. Nothing is rewritten.
     ====================================================================== */
  function escapeRe(s) { return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  function highlight(root, terms) {
    if (!root || !terms || !terms.length) return root;
    var re = new RegExp('(' + terms.map(escapeRe).join('|') + ')', 'gi');
    collectTextNodes(root).forEach(function (node) {
      var text = node.nodeValue;
      re.lastIndex = 0;
      if (!re.test(text)) return;
      re.lastIndex = 0;
      var frag = document.createDocumentFragment();
      var last = 0, m;
      while ((m = re.exec(text)) !== null) {
        if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)));
        frag.appendChild(RL.el('mark', { class: 'hit', text: m[0] }));
        last = m.index + m[0].length;
      }
      if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
    return root;
  }

  /* ==========================================================================
     4. SEARCH
     ====================================================================== */
  var MAX_RESULTS = 150;

  function search(query) {
    var i = buildIndex();
    var raw = String(query || '').trim();
    var out = { query: raw, terms: [], hits: [], total: 0, jump: null };
    if (!i || !raw) return out;

    var direct = normNum(raw);
    if (/^\d{1,3}(\.\d+[a-z]?)?$/.test(direct) &&
        Object.prototype.hasOwnProperty.call(i.by, direct)) {
      out.jump = i.by[direct];
    }

    out.terms = raw.toLowerCase().split(/\s+/).filter(function (t) { return t.length >= 2; });
    if (!out.terms.length) return out;

    for (var k = 0; k < i.all.length; k++) {
      var hay = i.lower[k], ok = true;
      for (var t = 0; t < out.terms.length; t++) {
        if (hay.indexOf(out.terms[t]) === -1) { ok = false; break; }
      }
      if (!ok) continue;
      out.total++;
      if (out.hits.length < MAX_RESULTS) out.hits.push(i.all[k]);
    }
    return out;
  }

  function snippet(rule, terms) {
    var text = rule.text;
    if (text.length <= 190) return text;
    var low = text.toLowerCase(), at = -1;
    for (var t = 0; t < terms.length; t++) {
      var p = low.indexOf(terms[t]);
      if (p !== -1 && (at === -1 || p < at)) at = p;
    }
    if (at === -1) at = 0;
    var from = Math.max(0, at - 70);
    var to = Math.min(text.length, from + 190);
    return (from > 0 ? '\u2026' : '') + text.slice(from, to).trim() + (to < text.length ? '\u2026' : '');
  }

  /* ==========================================================================
     5. "START HERE" — the rules a new Commander player actually needs.
     Every number below is resolved against the index at render time. One that
     does not resolve is DROPPED and reported, never silently shown.
     Labels are the rule's own verbatim heading; the one-liner underneath is
     navigation copy ("this is where X is defined"), not a rules claim.
     ====================================================================== */
  var START_HERE = [
    { group: 'Before the first turn', items: [
      { n: '103.5c', why: 'Your first mulligan in a multiplayer game.' }
    ]},
    { group: 'Who acts, and when', items: [
      { n: '117', why: 'Priority — the reason you ever get to do anything.' },
      { n: '601', why: 'The seven steps of putting a spell on the stack.' },
      { n: '405', why: 'The stack itself: what sits on it and in what order.' },
      { n: '608', why: 'What happens when the top of the stack finally resolves.' },
      { n: '603', why: 'Triggered abilities — the ones you keep forgetting.' }
    ]},
    { group: 'Combat, step by step', items: [
      { n: '506', why: 'The combat phase as a whole.' },
      { n: '507', why: 'Beginning of combat.' },
      { n: '508', why: 'Declaring attackers.' },
      { n: '509', why: 'Declaring blockers.' },
      { n: '510', why: 'Damage.' },
      { n: '511', why: 'End of combat.' }
    ]},
    { group: 'The invisible machinery', items: [
      { n: '704', why: 'State-based actions — the game cleaning up without being asked.' },
      { n: '613', why: 'Layers — why two effects on one creature resolve the way they do.' }
    ]},
    { group: 'Your format', items: [
      { n: '903', why: 'Commander: the whole section.' }
    ]}
  ];

  /* ==========================================================================
     6. VIEW
     ====================================================================== */
  var dom = null;          // cached DOM after mount
  var currentNum = '';     // rule showing in the detail pane
  var lastSearch = { terms: [] };
  var keyHandler = null;

  function ruleHref(n) { return RL.href('rules', n); }

  function citationFor(rule) {
    return 'Magic: The Gathering Comprehensive Rules \u2014 rule ' + rule.number + '\n' + rule.text;
  }

  /* ---- tree ------------------------------------------------------------- */
  /* Children are built on first expand. 3,309 rows up front would be a lot of
     DOM for a pane you mostly use three levels of. */
  function treeItem(num, depth) {
    var rule = getRule(num);
    if (!rule) return null;
    var kids = childrenOf(num);
    var li = RL.el('li', { class: 'rtree__item', 'data-num': num });
    var row = RL.el('div', { class: ['rtree__row', 'rtree__row--d' + Math.min(depth, 3)] });
    var group = null;

    if (kids.length) {
      group = RL.el('ul', { class: 'rtree__group', id: 'rtree-' + num, hidden: true });
      var twisty = RL.el('button', {
        class: 'rtree__twisty', type: 'button',
        'aria-expanded': 'false', 'aria-controls': 'rtree-' + num,
        aria: { label: 'Show the ' + kids.length + ' subrule' + (kids.length === 1 ? '' : 's') +
                       ' of rule ' + num },
        on: { click: function () { toggle(li, !isOpen(li)); } }
      }, RL.svgIcon('chevron-right', 16));
      row.appendChild(twisty);
    } else {
      row.appendChild(RL.el('span', { class: 'rtree__spacer', 'aria-hidden': 'true' }));
    }

    row.appendChild(RL.el('a', {
      class: ['rtree__link', isHeading(rule) ? 'rtree__link--head' : ''],
      href: ruleHref(num)
    },
      RL.el('span', { class: 'rtree__num', text: num }),
      RL.el('span', { class: 'rtree__txt', text: shortText(rule, 130) })
    ));

    li.appendChild(row);
    if (group) li.appendChild(group);
    return li;
  }

  function isOpen(li) {
    var t = li.querySelector(':scope > .rtree__row > .rtree__twisty');
    return !!t && t.getAttribute('aria-expanded') === 'true';
  }

  function toggle(li, open) {
    var twisty = li.querySelector(':scope > .rtree__row > .rtree__twisty');
    var group = li.querySelector(':scope > .rtree__group');
    if (!twisty || !group) return;
    if (open && !group.dataset.built) {
      var num = li.getAttribute('data-num');
      var depth = +(li.getAttribute('data-depth') || 0) + 1;
      childrenOf(num).forEach(function (kid) {
        var node = treeItem(kid, depth);
        if (node) { node.setAttribute('data-depth', depth); group.appendChild(node); }
      });
      group.dataset.built = '1';
    }
    group.hidden = !open;
    twisty.setAttribute('aria-expanded', open ? 'true' : 'false');
    li.classList.toggle('is-open', !!open);
  }

  function buildTree() {
    var root = RL.el('ul', { class: 'rtree__group rtree__root' });
    buildIndex().roots.forEach(function (n) {
      var node = treeItem(n, 0);
      if (node) { node.setAttribute('data-depth', '0'); root.appendChild(node); }
    });
    return root;
  }

  /* Expand every ancestor of `num` and scroll it into view. */
  function revealInTree(num) {
    if (!dom || !num) return;
    var chain = ancestorsOf(num).map(function (r) { return r.number; }).concat([num]);
    var scope = dom.tree;
    for (var i = 0; i < chain.length; i++) {
      var li = scope.querySelector('[data-num="' + cssq(chain[i]) + '"]');
      if (!li) break;
      if (i < chain.length - 1) toggle(li, true);
      scope = li;
    }
    var target = dom.tree.querySelector('[data-num="' + cssq(num) + '"]');
    dom.tree.querySelectorAll('.rtree__link[aria-current]').forEach(function (a) {
      a.removeAttribute('aria-current');
    });
    if (!target) return;
    var link = target.querySelector(':scope > .rtree__row > .rtree__link');
    if (link) link.setAttribute('aria-current', 'true');
    if (dom.treeWrap && !dom.treeWrap.hidden) {
      var tr = target.getBoundingClientRect();
      var wr = dom.treeWrap.getBoundingClientRect();
      if (tr.top < wr.top || tr.bottom > wr.bottom) {
        dom.treeWrap.scrollTop += (tr.top - wr.top) - wr.height / 3;
      }
    }
  }

  /* attribute-selector-safe: rule numbers are [0-9.a-z] only, but be careful */
  function cssq(s) { return String(s).replace(/["\\]/g, '\\$&'); }

  /* ---- detail ----------------------------------------------------------- */
  function copyBtn(rule) {
    var btn = RL.el('button', {
      class: 'btn btn--ghost btn--sm', type: 'button',
      on: {
        click: function () {
          RL.copy(citationFor(rule)).then(function (ok) {
            RL.clear(btn);
            btn.appendChild(RL.svgIcon(ok ? 'check' : 'alert-triangle', 16));
            btn.appendChild(RL.el('span', { text: ok ? 'Copied' : 'Copy failed' }));
            RL.toast(ok ? 'Rule ' + rule.number + ' copied with its full text'
                        : 'Could not reach the clipboard \u2014 select the text instead',
                     { tone: ok ? 'good' : 'bad' });
            window.setTimeout(function () {
              RL.clear(btn);
              btn.appendChild(RL.svgIcon('copy', 16));
              btn.appendChild(RL.el('span', { text: 'Copy citation' }));
            }, 2000);
          });
        }
      }
    }, RL.svgIcon('copy', 16), RL.el('span', { text: 'Copy citation' }));
    return btn;
  }

  function renderDetail(num) {
    var host = dom.detail;
    RL.clear(host);

    if (!num) { host.appendChild(startHerePanel()); return; }

    var rule = getRule(num);
    if (!rule) {
      host.appendChild(RL.el('div', { class: 'panel state' },
        RL.el('div', { class: 'state__icon' }, RL.svgIcon('alert-triangle', 28)),
        RL.el('h2', { class: 'state__title', text: 'not in my data: rule \u2018' + num + '\u2019' }),
        RL.el('p', { class: 'state__body' },
          'There is no rule with that number in the ',
          RL.el('strong', { text: RL.fmt.int(buildIndex().all.length) }),
          ' Comprehensive Rules on this machine. Rule numbers look like ',
          RL.el('code', { class: 'md-code', text: '117' }), ', ',
          RL.el('code', { class: 'md-code', text: '601.2' }), ' or ',
          RL.el('code', { class: 'md-code', text: '601.2a' }), '.'),
        RL.el('p', { class: 'state__body' },
          RL.el('a', { href: RL.href('rules'), class: 'btn btn--ghost' },
            RL.svgIcon('compass', 16), RL.el('span', { text: 'Back to Start here' })))
      ));
      return;
    }

    var art = RL.el('article', { class: 'panel rdetail', 'aria-labelledby': 'rdetail-h' });

    // breadcrumb
    var chain = ancestorsOf(rule.number);
    if (chain.length) {
      var crumbs = RL.el('nav', { class: 'rdetail__crumbs', aria: { label: 'Rule location' } });
      chain.forEach(function (a, i) {
        if (i) crumbs.appendChild(RL.svgIcon('chevron-right', 12));
        crumbs.appendChild(RL.el('a', { class: 'rdetail__crumb', href: ruleHref(a.number) },
          RL.el('span', { class: 'mono', text: a.number }),
          RL.el('span', { text: ' ' + shortText(a, 46) })
        ));
      });
      art.appendChild(crumbs);
    }

    var head = RL.el('header', { class: 'rdetail__head' },
      RL.el('h2', { class: 'rdetail__num', id: 'rdetail-h' },
        RL.el('span', { class: 'sr-only', text: 'Rule ' }),
        rule.number),
      RL.el('div', { class: 'rdetail__actions' }, copyBtn(rule))
    );
    art.appendChild(head);

    var body = RL.el('div', {
      class: ['rdetail__text', isHeading(rule) ? 'rdetail__text--head' : '']
    });
    body.appendChild(linkifyText(rule.text));
    if (lastSearch.terms.length) highlight(body, lastSearch.terms);
    art.appendChild(body);

    // subrules
    var kids = childrenOf(rule.number);
    if (kids.length) {
      var list = RL.el('ul', { class: 'rdetail__kids' });
      kids.forEach(function (kn) {
        var k = getRule(kn);
        if (!k) return;
        list.appendChild(RL.el('li', null,
          RL.el('a', { class: 'rdetail__kid', href: ruleHref(kn) },
            RL.el('span', { class: 'rdetail__kidnum mono', text: kn }),
            RL.el('span', { class: 'rdetail__kidtxt', text: shortText(k, 150) })
          )
        ));
      });
      art.appendChild(RL.el('section', { class: 'rdetail__block' },
        RL.el('h3', { class: 'rdetail__blocktitle' },
          RL.svgIcon('layers', 16),
          RL.el('span', { text: kids.length + ' subrule' + (kids.length === 1 ? '' : 's') })),
        list
      ));
    }

    // footer: parent + CLI equivalent
    var foot = RL.el('footer', { class: 'rdetail__foot' });
    if (rule.parent && getRule(rule.parent)) {
      foot.appendChild(RL.el('a', { class: 'btn btn--ghost btn--sm', href: ruleHref(rule.parent) },
        RL.svgIcon('arrow-left', 16),
        RL.el('span', { text: 'Parent \u2014 rule ' + rule.parent })));
    }
    foot.appendChild(RL.el('span', { class: 'rdetail__cli mono' },
      RL.svgIcon('terminal', 14),
      RL.el('span', { text: './bin/mtg rule ' + rule.number })));
    art.appendChild(foot);

    host.appendChild(art);
  }

  /* ---- start here -------------------------------------------------------- */
  function startHerePanel() {
    var wrap = RL.el('div', { class: 'stack' });
    var missing = [];

    var panel = RL.el('section', { class: 'panel rstart' },
      RL.el('div', { class: 'panel__head' },
        RL.el('h2', { class: 'panel__title' },
          RL.svgIcon('compass', 20), RL.el('span', { text: 'Start here' }))),
      RL.el('p', { class: 'panel__sub' },
        'Nine sections, ' + RL.fmt.int(buildIndex().all.length) + ' rules. These are the ones ' +
        'that decide a Commander game. Each opens the rule verbatim.')
    );

    START_HERE.forEach(function (grp) {
      var items = grp.items.filter(function (it) {
        var ok = !!getRule(it.n);
        if (!ok) missing.push(it.n);
        return ok;
      });
      if (!items.length) return;

      var ul = RL.el('ul', { class: 'rstart__list' });
      items.forEach(function (it) {
        var r = getRule(it.n);
        ul.appendChild(RL.el('li', null,
          RL.el('a', { class: 'rstart__item', href: ruleHref(r.number) },
            RL.el('span', { class: 'rstart__num mono', text: r.number }),
            RL.el('span', { class: 'rstart__body' },
              RL.el('span', { class: 'rstart__title', text: shortText(r, 64) }),
              RL.el('span', { class: 'rstart__why', text: it.why })
            )
          )
        ));
      });

      panel.appendChild(RL.el('div', { class: 'rstart__group' },
        RL.el('h3', { class: 'rstart__grouptitle', text: grp.group }),
        ul
      ));
    });

    if (missing.length) {
      panel.appendChild(RL.el('p', { class: 'rstart__missing' },
        RL.svgIcon('alert-triangle', 16),
        RL.el('span', { text: 'Dropped from this list because they are not in the data on ' +
                              'this machine: ' + missing.join(', ') + '.' })));
    }
    wrap.appendChild(panel);

    wrap.appendChild(RL.el('section', { class: 'panel panel--quiet rhow' },
      RL.el('h3', { class: 'rhow__title' },
        RL.svgIcon('link', 16), RL.el('span', { text: 'Everything here is linked' })),
      RL.el('p', { class: 'rhow__body' },
        'The rules constantly point at each other \u2014 \u201csee rule 601.2b\u201d. Every one of ' +
        'those references is a link, and every link was checked against the index before it was ' +
        'drawn. A reference that does not resolve is left as plain text rather than sent nowhere.'),
      RL.el('p', { class: 'rhow__body' },
        'Search matches rule text and rule numbers. Type a number like ',
        RL.el('code', { class: 'md-code', text: '601.2a' }),
        ' and press Enter to jump straight to it. Press ',
        RL.el('kbd', { class: 'kbd', text: '/' }), ' to focus search.')
    ));

    return wrap;
  }

  /* ---- search results ---------------------------------------------------- */
  function renderResults(res) {
    var host = dom.results;
    RL.clear(host);
    dom.treeWrap.hidden = !!res.query;
    host.hidden = !res.query;
    if (!res.query) { dom.count.textContent = ''; return; }

    if (res.jump) {
      host.appendChild(RL.el('a', { class: 'rjump', href: ruleHref(res.jump.number) },
        RL.svgIcon('hash', 18),
        RL.el('span', { class: 'rjump__body' },
          RL.el('span', { class: 'rjump__num mono', text: res.jump.number }),
          RL.el('span', { class: 'rjump__txt', text: shortText(res.jump, 90) })),
        RL.svgIcon('chevron-right', 18)
      ));
    }

    if (!res.hits.length) {
      dom.count.textContent = res.jump ? 'exact number match' : 'no matches';
      if (!res.jump) {
        host.appendChild(RL.el('p', { class: 'rres__empty' },
          'Nothing in the Comprehensive Rules contains ',
          RL.el('strong', { text: res.query }),
          '. Every word has to appear in the same rule \u2014 try fewer of them.'));
      }
      return;
    }

    dom.count.textContent = res.total > res.hits.length
      ? 'showing ' + res.hits.length + ' of ' + RL.fmt.int(res.total) + ' matches'
      : RL.fmt.plural(res.total, 'match', 'matches');

    var ul = RL.el('ul', { class: 'rres' });
    res.hits.forEach(function (r) {
      var text = RL.el('span', { class: 'rres__txt', text: snippet(r, res.terms) });
      highlight(text, res.terms);
      ul.appendChild(RL.el('li', null,
        RL.el('a', { class: 'rres__item', href: ruleHref(r.number) },
          RL.el('span', { class: 'rres__num mono', text: r.number }),
          text)
      ));
    });
    host.appendChild(ul);
  }

  /* ---- mount ------------------------------------------------------------- */
  function mount(el) {
    var i = buildIndex();
    if (!i) {
      el.appendChild(RL.el('div', { class: 'panel state' },
        RL.el('div', { class: 'state__icon' }, RL.svgIcon('book', 28)),
        RL.el('h2', { class: 'state__title', text: 'The rules have not been built' }),
        RL.el('p', { class: 'state__body' },
          RL.el('code', { class: 'md-code', text: 'dashboard/data/rules.js' }),
          ' did not register. Run ',
          RL.el('code', { class: 'md-code', text: './bin/mtg dashboard --build' }),
          ' and reload.')));
      return;
    }

    el.appendChild(RL.el('div', { class: 'row' },
      RL.el('h1', { class: 'section-title', text: 'Comprehensive Rules' })));
    el.appendChild(RL.el('p', { class: 'section-sub' },
      RL.fmt.int(i.all.length) + ' rules across nine sections, verbatim, with every ' +
      'cross-reference turned into a link. Nothing here is paraphrased.'));

    var input = RL.el('input', {
      class: 'input rsearch__input', type: 'search', id: 'rules-search',
      placeholder: 'Search rule text, or type 601.2a',
      autocomplete: 'off', spellcheck: 'false',
      on: {
        input: function () { schedule(); },
        keydown: function (e) {
          if (e.key === 'Enter') {
            e.preventDefault();
            var res = search(input.value);
            if (res.jump) RL.navigate('rules', res.jump.number);
            else if (res.hits.length) RL.navigate('rules', res.hits[0].number);
          } else if (e.key === 'Escape' && input.value) {
            e.preventDefault();
            input.value = '';
            runSearch();
          }
        }
      }
    });

    var clear = RL.el('button', {
      class: 'icon-btn rsearch__clear', type: 'button',
      aria: { label: 'Clear the search' },
      on: { click: function () { input.value = ''; runSearch(); input.focus(); } }
    }, RL.svgIcon('x', 18));

    var count = RL.el('p', { class: 'rsearch__count', role: 'status', 'aria-live': 'polite' });

    var nav = RL.el('aside', { class: 'rules__nav' },
      RL.el('div', { class: 'rsearch' },
        RL.el('label', { class: 'sr-only', for: 'rules-search', text: 'Search the Comprehensive Rules' }),
        RL.el('div', { class: 'rsearch__field' }, RL.svgIcon('search', 18), input, clear),
        count
      )
    );

    var tree = buildTree();
    var treeWrap = RL.el('nav', { class: 'rules__tree', aria: { label: 'Rules by section' } }, tree);
    var results = RL.el('div', { class: 'rules__results', hidden: true });
    nav.appendChild(treeWrap);
    nav.appendChild(results);

    var back = RL.el('a', {
      class: 'btn btn--ghost rules__back', href: RL.href('rules')
    }, RL.svgIcon('arrow-left', 16), RL.el('span', { text: 'All rules' }));

    var detail = RL.el('div', { class: 'rules__detail' });

    var pane = RL.el('div', { class: 'rules', 'data-mode': 'list' }, nav,
      RL.el('div', { class: 'rules__right' }, back, detail));
    el.appendChild(pane);

    dom = { pane: pane, input: input, count: count, tree: tree, treeWrap: treeWrap,
            results: results, detail: detail };

    var timer = null;
    function schedule() {
      window.clearTimeout(timer);
      timer = window.setTimeout(runSearch, 130);
    }
    function runSearch() {
      var res = search(dom.input.value);
      lastSearch = res;
      renderResults(res);
      dom.pane.classList.toggle('is-searching', !!res.query);
    }
    dom.runSearch = runSearch;
  }

  function select(num) {
    if (!dom) return;
    currentNum = num || '';
    dom.pane.setAttribute('data-mode', currentNum ? 'detail' : 'list');
    renderDetail(currentNum);
    if (currentNum) revealInTree(currentNum);
  }

  RL.registerView({
    id: 'rules',
    label: 'Rules',
    icon: 'book',
    mount: mount,
    onEnter: function (params) {
      if (!dom) return;
      select(params[0] ? normNum(params[0]) : '');
      if (!keyHandler) {
        keyHandler = function (e) {
          if (e.key !== '/' || e.metaKey || e.ctrlKey || e.altKey) return;
          var t = e.target;
          if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' ||
                    t.tagName === 'SELECT' || t.isContentEditable)) return;
          e.preventDefault();
          dom.input.focus();
          dom.input.select();
        };
        document.addEventListener('keydown', keyHandler);
      }
    },
    onLeave: function () {
      if (keyHandler) { document.removeEventListener('keydown', keyHandler); keyHandler = null; }
    }
  });

  /* ==========================================================================
     7. Export for the Glossary view (and anything else that cites a rule).
     Kept off window.RL so this file never collides with core.js.
     ====================================================================== */
  window.RLRules = {
    index: buildIndex,
    get: getRule,
    href: ruleHref,
    normalize: normNum,
    linkify: linkifyText,
    linkifyElement: linkifyElement,
    highlight: highlight,
    search: search
  };

})(window, document);

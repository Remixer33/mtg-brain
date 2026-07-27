/* ============================================================================
   REMY'S LAIR — app/boot.js
   Startup: nav order, drawer behaviour, empty/error states, router start.

   Runs LAST (after core.js, the data/*.js files, and every app/view-*.js).
   Everything it touches is defensive: a view file that does not exist yet, a
   data file that has never been built, a view whose mount() throws — none of
   those may produce a blank page or a console-only error.
   ========================================================================== */
(function (window, document) {
  'use strict';

  var RL = window.RL;
  if (!RL) {
    // core.js itself failed to load. Nothing else here can work; say so in the DOM.
    var hostEl = document.getElementById('viewHost');
    if (hostEl) {
      hostEl.innerHTML =
        '<div class="panel state state--bad">' +
        '<h2 class="state__title">The app failed to load</h2>' +
        '<p class="state__body">app/core.js did not run. Check that the file exists at ' +
        'dashboard/app/core.js and reload.</p></div>';
    }
    return;
  }

  var BUILD_CMD = './bin/mtg dashboard --build';

  /* ==========================================================================
     Canonical nav order. Views register themselves; this list decides the
     order they appear in and supplies the label + icon if a view omits them.
     A view in this list that never registered gets a stub (see below), so the
     nav is always complete and every item goes somewhere honest.
     ====================================================================== */
  var NAV = [
    { id: 'lair',     label: 'Lair',     icon: 'home',      blurb: 'The overview: decks, totals, what changed.' },
    { id: 'decks',    label: 'Decks',    icon: 'layers',    blurb: 'Tidus, Bumbleflower, Dogmeat — lists, curves, primers.' },
    { id: 'cards',    label: 'Cards',    icon: 'search',    blurb: 'Search all 38,351 cards. Loaded on demand.' },
    { id: 'rules',    label: 'Rules',    icon: 'book',      blurb: 'The 3,309 Comprehensive Rules.' },
    { id: 'glossary', label: 'Glossary', icon: 'bookmark',  blurb: '735 official glossary terms.' },
    { id: 'merge',    label: 'Merge',    icon: 'git-merge', blurb: 'The Bant merge — one deck out of two boxes.' },
    { id: 'learning', label: 'Learning', icon: 'activity',  blurb: 'Game log and the rules that keep catching you out.' }
  ];

  function navMeta(id) {
    for (var i = 0; i < NAV.length; i++) if (NAV[i].id === id) return NAV[i];
    return null;
  }

  /* ==========================================================================
     Stubs for views that have not been built yet.
     Honest placeholder > missing nav item > blank page.
     ====================================================================== */
  NAV.forEach(function (item) {
    if (RL.view(item.id)) return;
    RL.registerView({
      id: item.id,
      label: item.label,
      icon: item.icon,
      mount: function (el) {
        el.appendChild(RL.el('div', { class: 'panel state' },
          RL.el('div', { class: 'state__icon' }, RL.svgIcon('sparkles', 28)),
          RL.el('h2', { class: 'state__title', text: item.label + ' is not built yet' }),
          RL.el('p', { class: 'state__body' },
            item.blurb + ' This section renders from ',
            RL.el('code', { class: 'md-code', text: 'dashboard/app/view-' + item.id + '.js' }),
            ', which is not on disk yet. The rest of the dashboard is unaffected.')
        ));
      }
    });
  });

  /* ==========================================================================
     The empty state — no data has been built.
     ====================================================================== */
  var emptyStateEl = null;

  function copyButton(text) {
    var btn = RL.el('button', {
      class: 'btn btn--primary', type: 'button',
      on: {
        click: function () {
          RL.copy(text).then(function (ok) {
            RL.clear(btn);
            btn.appendChild(RL.svgIcon(ok ? 'check' : 'alert-triangle', 18));
            btn.appendChild(RL.el('span', { text: ok ? 'Copied' : 'Copy failed' }));
            RL.toast(ok ? 'Command copied to the clipboard' : 'Could not reach the clipboard — select the text instead',
                     { tone: ok ? 'good' : 'bad' });
            window.setTimeout(function () {
              RL.clear(btn);
              btn.appendChild(RL.svgIcon('copy', 18));
              btn.appendChild(RL.el('span', { text: 'Copy command' }));
            }, 2200);
          });
        }
      }
    }, RL.svgIcon('copy', 18), RL.el('span', { text: 'Copy command' }));
    return btn;
  }

  function buildEmptyState() {
    return RL.el('div', { class: 'panel state', id: 'emptyState' },
      RL.el('div', { class: 'state__icon' }, RL.svgIcon('database', 28)),
      RL.el('h2', { class: 'state__title', text: 'No data has been built yet' }),
      RL.el('p', { class: 'state__body' },
        'Remy’s Lair renders whatever is sitting in ',
        RL.el('code', { class: 'md-code', text: 'dashboard/data/' }),
        '. That folder has no ', RL.el('code', { class: 'md-code', text: 'core.js' }),
        ' in it, so there is nothing to draw — the page is fine, the data is simply absent.'),
      RL.el('p', { class: 'state__body' },
        'Run this from the project root, then reload this page:'),
      RL.el('div', { class: 'cmdbar' },
        RL.el('div', { class: 'cmdbar__code' }, RL.svgIcon('terminal', 16),
          RL.el('span', { text: BUILD_CMD })),
        copyButton(BUILD_CMD)
      ),
      RL.el('p', { class: 'state__body muted' },
        'It reads ', RL.el('code', { class: 'md-code', text: 'data/mtg.sqlite' }),
        ' and writes plain .js files next to this page. Nothing is downloaded, nothing is billed — ' +
        'the dashboard never touches the network.'),
      RL.el('hr', { class: 'divider' }),
      RL.el('p', { class: 'state__body muted' },
        'Already ran it? Then the files exist but did not register. Open the browser console: a ' +
        'failed ', RL.el('code', { class: 'md-code', text: '<script src="data/core.js">' }),
        ' shows up there. Serving the folder with ',
        RL.el('code', { class: 'md-code', text: './bin/mtg dashboard --serve' }),
        ' also rules out a file:// path problem.')
    );
  }

  function showEmptyState(show) {
    var host = document.getElementById('viewHost');
    if (!host) return;
    if (show) {
      if (!emptyStateEl) { emptyStateEl = buildEmptyState(); host.appendChild(emptyStateEl); }
      emptyStateEl.hidden = false;
      // hide any view container that may be showing
      var vs = host.querySelectorAll('.view');
      for (var i = 0; i < vs.length; i++) vs[i].hidden = true;
    } else if (emptyStateEl) {
      emptyStateEl.hidden = true;
    }
  }

  function hasData() { return RL.data('core') !== null; }

  /* The router asks this before mounting anything. Returning false means
     "do not render the view" — the empty state stands in for every route. */
  RL.setRouteGuard(function () {
    if (hasData()) { showEmptyState(false); return true; }
    showEmptyState(true);
    return false;
  });

  /* ==========================================================================
     Navigation
     ====================================================================== */
  var navList = document.getElementById('navList');

  function buildNav() {
    if (!navList) return;
    RL.clear(navList);

    var ordered = [];
    NAV.forEach(function (item) { if (RL.view(item.id)) ordered.push(RL.view(item.id)); });
    RL.views().forEach(function (v) {
      if (ordered.indexOf(v) === -1) ordered.push(v); // anything registered outside the canonical list
    });

    ordered.forEach(function (view) {
      var meta = navMeta(view.id) || {};
      var label = view.label || meta.label || view.id;
      var icon = view.icon || meta.icon || 'chevron-right';

      var link = RL.el('a', {
        class: 'nav__link',
        href: RL.href(view.id),
        'data-nav': view.id,
        on: { click: closeDrawerSoon }
      },
        RL.svgIcon(icon, 18),
        RL.el('span', { class: 'nav__label', text: label })
      );
      navList.appendChild(RL.el('li', { class: 'nav__item' }, link));
    });

    markActive(RL.route());
  }

  function markActive(route) {
    if (!navList) return;
    var links = navList.querySelectorAll('.nav__link');
    for (var i = 0; i < links.length; i++) {
      var on = links[i].getAttribute('data-nav') === route.id;
      if (on) links[i].setAttribute('aria-current', 'page');
      else links[i].removeAttribute('aria-current');
    }
  }

  RL.setNavBuilder(buildNav);
  RL.on('route', markActive);
  RL.on('view', function () { if (navList && navList.childNodes.length) buildNav(); });

  /* ==========================================================================
     Sidebar footer — a quiet, honest status line
     ====================================================================== */
  function buildFooter() {
    var foot = document.getElementById('sidebarFoot');
    if (!foot) return;
    RL.clear(foot);
    var core = RL.data('core');

    if (!core) {
      foot.appendChild(RL.el('div', { class: 'sidebar__footrow' },
        RL.svgIcon('alert-triangle', 14),
        RL.el('span', { text: 'No data built' })));
      foot.appendChild(RL.el('code', { class: 'mono', text: BUILD_CMD }));
      return;
    }

    var tables = (core.db && core.db.tables) || {};
    var decks = core.decks || [];

    foot.appendChild(RL.el('div', { class: 'sidebar__footrow' },
      RL.svgIcon('database', 14),
      RL.el('span', null, RL.el('strong', { text: RL.fmt.int(tables.cards) }), ' cards')));
    foot.appendChild(RL.el('div', { class: 'sidebar__footrow' },
      RL.svgIcon('book', 14),
      RL.el('span', null, RL.el('strong', { text: RL.fmt.int(tables.rules) }), ' rules · ',
        RL.el('strong', { text: RL.fmt.int(tables.rulings) }), ' rulings')));
    foot.appendChild(RL.el('div', { class: 'sidebar__footrow' },
      RL.svgIcon('layers', 14),
      RL.el('span', null, RL.el('strong', { text: RL.fmt.int(decks.length) }), ' decks loaded')));
    if (core.generated_at) {
      foot.appendChild(RL.el('div', { class: 'sidebar__footrow' },
        RL.svgIcon('check', 14),
        RL.el('span', { text: 'Built ' + RL.fmt.date(core.generated_at) })));
    }
  }

  /* ==========================================================================
     Mobile drawer: toggle, scrim, Escape, focus trap, focus restore
     ====================================================================== */
  var sidebar = document.getElementById('sidebar');
  var scrim = document.getElementById('drawerScrim');
  var toggleBtn = document.getElementById('navToggle');
  var closeBtn = document.getElementById('navClose');
  var lastFocused = null;

  function isDrawerMode() { return window.matchMedia('(max-width: 1023.98px)').matches; }
  function drawerOpen() { return !!sidebar && sidebar.classList.contains('is-open'); }

  function openDrawer() {
    if (!sidebar || !isDrawerMode()) return;
    lastFocused = document.activeElement;
    sidebar.classList.add('is-open');
    if (scrim) scrim.hidden = false;
    if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    var first = sidebar.querySelector('.nav__link');
    if (first) first.focus();
    document.addEventListener('keydown', onDrawerKey, true);
  }

  function closeDrawer() {
    if (!sidebar) return;
    sidebar.classList.remove('is-open');
    if (scrim) scrim.hidden = true;
    if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    document.removeEventListener('keydown', onDrawerKey, true);
    if (lastFocused && lastFocused.focus && document.contains(lastFocused)) lastFocused.focus();
    lastFocused = null;
  }

  function closeDrawerSoon() { if (drawerOpen()) window.setTimeout(closeDrawer, 0); }

  function onDrawerKey(e) {
    if (!drawerOpen()) return;
    if (e.key === 'Escape') { e.preventDefault(); closeDrawer(); return; }
    if (e.key !== 'Tab') return;
    var focusables = sidebar.querySelectorAll(
      'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])');
    var list = Array.prototype.filter.call(focusables, function (n) {
      return n.offsetParent !== null || n === document.activeElement;
    });
    if (!list.length) return;
    var first = list[0], last = list[list.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  if (toggleBtn) {
    toggleBtn.appendChild(RL.svgIcon('menu', 22));
    toggleBtn.addEventListener('click', function () {
      if (drawerOpen()) closeDrawer(); else openDrawer();
    });
  }
  if (closeBtn) {
    closeBtn.appendChild(RL.svgIcon('x', 20));
    closeBtn.addEventListener('click', closeDrawer);
  }
  if (scrim) scrim.addEventListener('click', closeDrawer);

  window.addEventListener('resize', function () {
    if (!isDrawerMode() && drawerOpen()) closeDrawer();
  });

  /* ==========================================================================
     Late-arriving data (RL.loadLazy, or a data file that parsed slowly):
     refresh the footer and re-render if we were sitting on the empty state.
     ====================================================================== */
  RL.on('data', function (evt) {
    if (evt.key === 'core') {
      buildFooter();
      if (emptyStateEl && !emptyStateEl.hidden) RL.render();
    }
  });

  /* Any uncaught error still gets a visible home rather than only the console. */
  window.addEventListener('error', function (e) {
    if (e && e.message && /Script error/i.test(e.message)) return;
    console.error('[boot] uncaught error', e && (e.error || e.message));
  });

  /* ==========================================================================
     Go
     ====================================================================== */
  function start() {
    var preboot = document.getElementById('preboot');
    if (preboot && preboot.parentNode) preboot.parentNode.removeChild(preboot);

    buildFooter();
    RL.start(document.getElementById('viewHost'));

    if (!hasData()) {
      showEmptyState(true);
      console.info('[Remy’s Lair] no data/core.js — run `' + BUILD_CMD + '` and reload.');
    }
    document.documentElement.setAttribute('data-booted', 'true');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();

})(window, document);

/* ============================================================================
   REMY'S LAIR — app/core.js
   window.RL: the shared toolkit every view is built on.

   Hard constraints this file obeys:
     C1  zero LLM spend        — no inference, no API, no keys. Pure rendering.
     C5  offline-first         — NO fetch(), NO XHR, NO CDN, NO remote anything.
                                 Local data arrives via <script src="data/*.js">
                                 files that call RL.register(). RL.loadLazy()
                                 injects one more <script> on demand; that is the
                                 only "loading" mechanism that exists here.
     C6  no build step         — plain ES2019-ish JS, no modules, no bundler.
     C3  Commander only        — no format words leak into any string below.

   PUBLIC API (the app contract — other views depend on this exactly):
     RL.register(key, payload)
     RL.data(key)                       -> payload | null
     RL.loadLazy(key, file, cb)         cb(payload, errOrNull)
     RL.registerView({id,label,icon,mount,onEnter,onLeave})
     RL.navigate(id, ...params)         (also accepts an array of params)
     RL.route()                         -> {id, params}
     RL.el(tag, attrs, ...children)     -> Element
     RL.svgIcon(name, size)             -> <svg>   (inline paths; NEVER emoji)
     RL.chart.bar/hbar/donut(spec)      -> <figure> (hand-rolled SVG + table view)
     RL.manaCost("{2}{G}{U}")           -> <span> of letter-labeled pips
     RL.md(markdown)                    -> HTML string   (escapes first)
     RL.mdEl(markdown)                  -> <div class="md">
     RL.toast(msg, opts)
     RL.fmt.price/int/pct/date/num
     RL.copy(text)                      -> Promise<boolean>
     RL.on(event, fn) / RL.emit(...)    tiny bus ('data', 'route')

   VIEW LIFECYCLE (what a view can rely on):
     mount(el, params)    ONCE, the first time the view is activated.
     onEnter(params, el)  EVERY activation, including the first (after mount).
     onLeave(el)          when navigating away.
     The element `el` stays in the DOM (hidden) between visits, so a view may
     cache DOM and only re-render on param change.
   ========================================================================== */
(function (window, document) {
  'use strict';

  var SVG_NS = 'http://www.w3.org/2000/svg';
  var RL = {};
  RL.version = '1.0.0';

  /* ==========================================================================
     0. tiny event bus
     ====================================================================== */
  var listeners = {};
  RL.on = function (name, fn) {
    (listeners[name] || (listeners[name] = [])).push(fn);
    return function off() {
      listeners[name] = (listeners[name] || []).filter(function (f) { return f !== fn; });
    };
  };
  RL.emit = function (name, detail) {
    (listeners[name] || []).forEach(function (fn) {
      try { fn(detail); } catch (e) { console.error('[RL] listener for "' + name + '" threw', e); }
    });
  };

  /* ==========================================================================
     1. data registry
     Data files are plain scripts ending in RL.register('key', {...}).
     ====================================================================== */
  var store = Object.create(null);

  RL.register = function (key, payload) {
    if (typeof key !== 'string' || !key) {
      console.error('[RL] register() needs a string key, got', key);
      return;
    }
    store[key] = payload;
    RL.emit('data', { key: key, payload: payload });
  };

  RL.data = function (key) {
    return Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null;
  };

  RL.has = function (key) { return Object.prototype.hasOwnProperty.call(store, key); };

  RL.keys = function () { return Object.keys(store); };

  /* Lazy data: inject <script src="data/<file>">. Used for cards.js (~9.6MB),
     which must NOT be paid for on first paint. Never fetch() — file:// CORS. */
  var lazyPending = Object.create(null);

  RL.loadLazy = function (key, file, cb) {
    cb = typeof cb === 'function' ? cb : function () {};
    if (RL.has(key)) { cb(store[key], null); return; }

    if (lazyPending[key]) { lazyPending[key].push(cb); return; }
    lazyPending[key] = [cb];

    var src = String(file).indexOf('/') >= 0 ? String(file) : 'data/' + file;
    var s = document.createElement('script');
    s.src = src;
    s.async = true;

    function settle(err) {
      var queue = lazyPending[key] || [];
      delete lazyPending[key];
      var payload = RL.has(key) ? store[key] : null;
      var realErr = err || (payload === null
        ? new Error('"' + src + '" loaded but did not register "' + key + '"')
        : null);
      queue.forEach(function (fn) {
        try { fn(payload, realErr); } catch (e) { console.error('[RL] loadLazy callback threw', e); }
      });
    }

    s.onload = function () { settle(null); };
    s.onerror = function () {
      settle(new Error('could not load "' + src + '" — run `./bin/mtg dashboard --build`'));
    };
    document.head.appendChild(s);
  };

  /* ==========================================================================
     2. RL.el — tiny hyperscript. No framework, no vdom.
        RL.el('div', {class:['a','b'], on:{click:fn}, dataset:{x:1}, aria:{label:'y'},
                      style:{color:'red'}, text:'hi' | html:'<b>hi</b>'}, child, [child])
     ====================================================================== */
  function isPlainObject(v) {
    return v !== null && typeof v === 'object' && !Array.isArray(v) &&
           !(v instanceof Node) && Object.getPrototypeOf(v) !== Date.prototype;
  }

  function appendChild(parent, child) {
    if (child === null || child === undefined || child === false || child === true) return;
    if (Array.isArray(child)) { child.forEach(function (c) { appendChild(parent, c); }); return; }
    if (child instanceof Node) { parent.appendChild(child); return; }
    parent.appendChild(document.createTextNode(String(child)));
  }

  RL.el = function (tag, attrs) {
    var node = document.createElement(tag);
    var childStart = 1;

    if (isPlainObject(attrs)) {
      childStart = 2;
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v === null || v === undefined || v === false) return;

        if (k === 'class' || k === 'className') {
          var cls = Array.isArray(v) ? v.filter(Boolean).join(' ') : String(v);
          if (cls) node.setAttribute('class', cls);
        } else if (k === 'text') {
          node.textContent = String(v);
        } else if (k === 'html') {
          node.innerHTML = String(v);
        } else if (k === 'on' && isPlainObject(v)) {
          Object.keys(v).forEach(function (evt) {
            if (typeof v[evt] === 'function') node.addEventListener(evt, v[evt]);
          });
        } else if (k === 'dataset' && isPlainObject(v)) {
          Object.keys(v).forEach(function (d) {
            if (v[d] !== null && v[d] !== undefined) node.dataset[d] = String(v[d]);
          });
        } else if (k === 'aria' && isPlainObject(v)) {
          Object.keys(v).forEach(function (a) {
            if (v[a] !== null && v[a] !== undefined) node.setAttribute('aria-' + a, String(v[a]));
          });
        } else if (k === 'style' && isPlainObject(v)) {
          Object.keys(v).forEach(function (p) {
            if (p.indexOf('--') === 0) node.style.setProperty(p, String(v[p]));
            else node.style[p] = v[p];
          });
        } else if (v === true) {
          node.setAttribute(k, '');
        } else {
          node.setAttribute(k, String(v));
        }
      });
    }

    for (var i = childStart; i < arguments.length; i++) appendChild(node, arguments[i]);
    return node;
  };

  /* SVG-namespaced sibling of RL.el — charts and icons need it. */
  RL.svgEl = function (tag, attrs) {
    var node = document.createElementNS(SVG_NS, tag);
    var childStart = 1;
    if (isPlainObject(attrs)) {
      childStart = 2;
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v === null || v === undefined || v === false) return;
        if (k === 'on' && isPlainObject(v)) {
          Object.keys(v).forEach(function (evt) {
            if (typeof v[evt] === 'function') node.addEventListener(evt, v[evt]);
          });
        } else if (k === 'text') {
          node.textContent = String(v);
        } else if (k === 'aria' && isPlainObject(v)) {
          Object.keys(v).forEach(function (a) { node.setAttribute('aria-' + a, String(v[a])); });
        } else if (k === 'dataset' && isPlainObject(v)) {
          Object.keys(v).forEach(function (d) { node.setAttribute('data-' + d, String(v[d])); });
        } else if (v === true) {
          node.setAttribute(k, '');
        } else {
          node.setAttribute(k, String(v));
        }
      });
    }
    for (var i = childStart; i < arguments.length; i++) appendChild(node, arguments[i]);
    return node;
  };

  RL.clear = function (node) {
    while (node && node.firstChild) node.removeChild(node.firstChild);
    return node;
  };

  RL.frag = function () {
    var f = document.createDocumentFragment();
    for (var i = 0; i < arguments.length; i++) appendChild(f, arguments[i]);
    return f;
  };

  /* ==========================================================================
     3. RL.svgIcon — inline stroke icons, 24x24, currentColor, stroke 1.75.
        NO EMOJI, EVER. Extend ICONS; never reach for a font or an image.
     ====================================================================== */
  var ICONS = {
    home:          '<path d="m3 10.2 9-7.2 9 7.2"/><path d="M5.5 8.8V20a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1V8.8"/><path d="M9.5 21v-7h5v7"/>',
    layers:        '<path d="m12 2.6 8.6 4.7-8.6 4.7-8.6-4.7z"/><path d="m20.6 12-8.6 4.7L3.4 12"/><path d="m20.6 16.7-8.6 4.7-8.6-4.7"/>',
    search:        '<circle cx="10.8" cy="10.8" r="7.2"/><path d="m21 21-5.1-5.1"/>',
    book:          '<path d="M4 19.2A2.8 2.8 0 0 1 6.8 16.4H20"/><path d="M6.8 2.4H20v19.2H6.8A2.8 2.8 0 0 1 4 18.8V5.2a2.8 2.8 0 0 1 2.8-2.8z"/>',
    bookmark:      '<path d="m19 21-7-4.8L5 21V4.8A1.8 1.8 0 0 1 6.8 3h10.4A1.8 1.8 0 0 1 19 4.8z"/>',
    'git-merge':   '<circle cx="6.5" cy="6" r="2.8"/><circle cx="17.5" cy="18" r="2.8"/><path d="M6.5 8.8V21"/><path d="M6.5 11.5a6.5 6.5 0 0 0 6.5 6.5h1.7"/>',
    activity:      '<path d="M22 12h-4.2l-3 8.4L9.2 3.6l-3 8.4H2"/>',
    'chevron-right':'<path d="m9 18 6-6-6-6"/>',
    'chevron-down':'<path d="m6 9 6 6 6-6"/>',
    'chevron-left':'<path d="m15 18-6-6 6-6"/>',
    'chevron-up':  '<path d="m6 15 6-6 6 6"/>',
    x:             '<path d="M18.5 5.5 5.5 18.5"/><path d="m5.5 5.5 13 13"/>',
    menu:          '<path d="M3.5 6.5h17"/><path d="M3.5 12h17"/><path d="M3.5 17.5h17"/>',
    'external-link':'<path d="M14.5 3.5H20.5v6"/><path d="m20.5 3.5-8 8"/><path d="M18 13.5V19a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 19V7.5A1.5 1.5 0 0 1 5 6h5.5"/>',
    table:         '<rect x="3" y="3.5" width="18" height="17" rx="1.8"/><path d="M3 9.5h18"/><path d="M3 15h18"/><path d="M11 9.5v11"/>',
    'chart-bar':   '<path d="M3.5 3.5v17h17"/><path d="M8 17V11.5"/><path d="M13 17V6.5"/><path d="M18 17v-8"/>',
    copy:          '<rect x="8.5" y="8.5" width="12" height="12" rx="1.8"/><path d="M5.5 15.5H5a1.5 1.5 0 0 1-1.5-1.5V5A1.5 1.5 0 0 1 5 3.5h9A1.5 1.5 0 0 1 15.5 5v.5"/>',
    check:         '<path d="m20 6.5-9.5 11L4 12"/>',
    filter:        '<path d="M21 4H3l7.2 8.5V19l3.6 1.8v-8.3z"/>',
    sparkles:      '<path d="m12 3 1.85 4.65L18.5 9.5l-4.65 1.85L12 16l-1.85-4.65L5.5 9.5l4.65-1.85z"/><path d="m18.8 15 .85 2.15 2.15.85-2.15.85-.85 2.15-.85-2.15-2.15-.85 2.15-.85z"/><path d="m5.4 3 .6 1.5 1.5.6-1.5.6-.6 1.5-.6-1.5L3.3 5.1l1.5-.6z"/>',
    shield:        '<path d="M12 21.4s7.6-3.6 7.6-9.4V5.4L12 2.6 4.4 5.4V12c0 5.8 7.6 9.4 7.6 9.4z"/>',
    coins:         '<circle cx="9" cy="9" r="5.6"/><path d="M17.9 10.6a5.6 5.6 0 1 1-7.4 7.5"/><path d="M8.2 6.8h1.4v4.4"/>',
    'alert-triangle':'<path d="m21.4 18.1-8-14a1.6 1.6 0 0 0-2.8 0l-8 14A1.6 1.6 0 0 0 4 20.5h16a1.6 1.6 0 0 0 1.4-2.4z"/><path d="M12 9v4"/><path d="M12 16.6h.01"/>',
    info:          '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 8h.01"/>',
    terminal:      '<path d="m4.5 17 5.5-5-5.5-5"/><path d="M12.5 19h7"/>',
    database:      '<ellipse cx="12" cy="5.4" rx="8" ry="2.9"/><path d="M4 5.4v13.2c0 1.6 3.6 2.9 8 2.9s8-1.3 8-2.9V5.4"/><path d="M4 12c0 1.6 3.6 2.9 8 2.9s8-1.3 8-2.9"/>',
    star:          '<path d="m12 3.4 2.65 5.5 6 .85-4.35 4.2 1.05 5.95L12 17.1l-5.35 2.8 1.05-5.95L3.35 9.75l6-.85z"/>',
    'arrow-left':  '<path d="M20 12H4"/><path d="m10 6-6 6 6 6"/>',
    play:          '<path d="M7 4.5 19.5 12 7 19.5z"/>',
    scroll:        '<path d="M6 4.5h12.5A1.5 1.5 0 0 1 20 6v11a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3V6a1.5 1.5 0 0 1 1.5-1.5z"/><path d="M8 9h8"/><path d="M8 13h6"/>'
  };

  RL.icons = ICONS; // extend, don't replace

  RL.svgIcon = function (name, size) {
    var px = size || 20;
    var svg = document.createElementNS(SVG_NS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('width', px);
    svg.setAttribute('height', px);
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.setAttribute('stroke-width', '1.75');
    svg.setAttribute('stroke-linecap', 'round');
    svg.setAttribute('stroke-linejoin', 'round');
    svg.setAttribute('class', 'icon icon--' + name);
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    var body = ICONS[name];
    if (!body) {
      console.warn('[RL] unknown icon "' + name + '" — falling back to a dot. Add it to RL.icons.');
      body = '<circle cx="12" cy="12" r="4"/>';
    }
    svg.innerHTML = body;
    return svg;
  };

  /* ==========================================================================
     4. formatting helpers
     ====================================================================== */
  var DASH = '—'; // em dash — the "no value" mark used everywhere

  function toNum(v) {
    if (v === null || v === undefined || v === '') return null;
    var n = typeof v === 'number' ? v : parseFloat(String(v).replace(/[^0-9.\-]/g, ''));
    return isFinite(n) ? n : null;
  }

  RL.fmt = {
    dash: DASH,
    num: function (v, digits) {
      var n = toNum(v);
      if (n === null) return DASH;
      return n.toLocaleString('en-US', {
        minimumFractionDigits: digits === undefined ? 0 : digits,
        maximumFractionDigits: digits === undefined ? 2 : digits
      });
    },
    int: function (v) {
      var n = toNum(v);
      return n === null ? DASH : Math.round(n).toLocaleString('en-US');
    },
    price: function (v) {
      var n = toNum(v);
      if (n === null) return DASH;
      return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    pct: function (v, digits) {
      var n = toNum(v);
      if (n === null) return DASH;
      return n.toFixed(digits === undefined ? 1 : digits) + '%';
    },
    bytes: function (v) {
      var n = toNum(v);
      if (n === null) return DASH;
      var units = ['B', 'KB', 'MB', 'GB'], i = 0;
      while (n >= 1024 && i < units.length - 1) { n /= 1024; i++; }
      return (i === 0 ? Math.round(n) : n.toFixed(1)) + ' ' + units[i];
    },
    date: function (v) {
      if (!v) return DASH;
      var d = new Date(v);
      if (isNaN(d.getTime())) return String(v);
      return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    },
    dateTime: function (v) {
      if (!v) return DASH;
      var d = new Date(v);
      if (isNaN(d.getTime())) return String(v);
      return d.toLocaleString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit'
      });
    },
    plural: function (n, one, many) {
      return RL.fmt.int(n) + ' ' + (Math.abs(toNum(n) || 0) === 1 ? one : (many || one + 's'));
    }
  };

  RL.escape = function (s) {
    return String(s === null || s === undefined ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  };

  RL.slug = function (s) {
    return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  };

  RL.reducedMotion = function () {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  };

  /* ==========================================================================
     5. RL.copy + RL.toast
     ====================================================================== */
  /* Always settles. Two traps here, both hit in practice:
       1. file:// is not a secure context in every browser, so navigator.clipboard
          may be missing entirely.
       2. Chrome leaves writeText() PENDING FOREVER when the document does not
          have focus — a plain .then() chain would hang and the button would
          give the user no feedback at all.
     So: race the async API against a short timer and fall back to execCommand. */
  RL.copy = function (text) {
    var str = String(text === null || text === undefined ? '' : text);
    var canAsync = !!(navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext);
    if (!canAsync) return Promise.resolve(legacyCopy(str));

    return new Promise(function (resolve) {
      var settled = false;
      function finish(v) { if (!settled) { settled = true; window.clearTimeout(timer); resolve(v); } }
      var timer = window.setTimeout(function () { finish(legacyCopy(str)); }, 500);
      try {
        navigator.clipboard.writeText(str).then(
          function () { finish(true); },
          function () { finish(legacyCopy(str)); }
        );
      } catch (e) {
        finish(legacyCopy(str));
      }
    });
  };

  function legacyCopy(str) {
    try {
      var ta = document.createElement('textarea');
      ta.value = str;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.top = '-1000px';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      var ok = document.execCommand('copy');
      document.body.removeChild(ta);
      return ok;
    } catch (e) {
      console.warn('[RL] copy failed', e);
      return false;
    }
  }

  RL.toast = function (msg, opts) {
    opts = opts || {};
    var host = document.getElementById('toaster');
    if (!host) return null;
    var t = RL.el('div', { class: ['toast', opts.tone ? 'toast--' + opts.tone : ''] },
      RL.svgIcon(opts.icon || (opts.tone === 'bad' ? 'alert-triangle' : 'check'), 18),
      RL.el('span', { class: 'toast__msg', text: String(msg) })
    );
    host.appendChild(t);
    var ttl = opts.duration || 3200;
    window.setTimeout(function () {
      t.classList.add('is-leaving');
      window.setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 280);
    }, ttl);
    return t;
  };

  /* ==========================================================================
     6. RL.manaCost — "{2}{G}{U}" -> letter-labeled pips.

     The letter is MANDATORY. tokens.css documents why: the five mana colors
     fail deuteranopia separation on red<->green (dE 3.9) and that is unfixable
     while they still read as Magic's colors. Colour is therefore never the only
     encoding — the glyph carries the meaning, the colour is decoration.
     ====================================================================== */
  var MANA_NAME = {
    W: 'white', U: 'blue', B: 'black', R: 'red', G: 'green', C: 'colorless',
    X: 'variable', Y: 'variable', Z: 'variable', S: 'snow', T: 'tap', Q: 'untap',
    E: 'energy', P: 'Phyrexian'
  };
  var COLOR_KEYS = { W: 1, U: 1, B: 1, R: 1, G: 1, C: 1 };

  function pipClass(sym) {
    var up = sym.toUpperCase();
    if (COLOR_KEYS[up]) return 'pip--' + up.toLowerCase();
    if (/^\d+$/.test(up)) return 'pip--generic';
    return 'pip--other';
  }

  function describeSymbol(sym) {
    var up = String(sym).toUpperCase();
    if (/^\d+$/.test(up)) return up + ' generic';
    if (up.indexOf('/') > 0) {
      return up.split('/').map(function (p) { return MANA_NAME[p] || p; }).join(' or ');
    }
    return MANA_NAME[up] || up;
  }

  /* Renders one symbol. `sym` is the inside of a {}, e.g. "2", "G", "W/U", "2/W". */
  RL.manaPip = function (sym) {
    var up = String(sym).toUpperCase();
    var parts = up.split('/');
    var cls = ['pip'];
    var label = describeSymbol(up);

    if (parts.length > 1) {
      cls.push('pip--hybrid');
      cls.push('pip--h-' + (COLOR_KEYS[parts[0]] ? parts[0].toLowerCase() : 'generic'));
      cls.push('pip--h2-' + (COLOR_KEYS[parts[1]] ? parts[1].toLowerCase() : 'generic'));
    } else {
      cls.push(pipClass(up));
    }

    return RL.el('span', {
      class: cls,
      title: label,
      aria: { label: label },
      role: 'img'
    }, RL.el('span', { class: 'pip__glyph', text: up }));
  };

  RL.manaCost = function (str, opts) {
    opts = opts || {};
    var wrap = RL.el('span', { class: 'mana' });
    var raw = String(str || '').trim();
    if (!raw) {
      wrap.setAttribute('aria-label', 'no mana cost');
      wrap.appendChild(RL.el('span', { class: 'mana__none', text: DASH }));
      return wrap;
    }
    var re = /\{([^}]+)\}/g, m, syms = [], found = false;
    while ((m = re.exec(raw)) !== null) { found = true; syms.push(m[1]); }
    if (!found) syms = raw.split('').filter(function (c) { return c.trim(); }); // tolerate "2GU"

    syms.forEach(function (s) { wrap.appendChild(RL.manaPip(s)); });
    wrap.setAttribute('aria-label',
      (opts.prefix ? opts.prefix + ': ' : '') +
      syms.map(describeSymbol).join(', '));
    wrap.setAttribute('role', 'img');
    return wrap;
  };

  /* A single color letter chip (W/U/B/R/G) for color-identity rows. */
  RL.colorChip = function (letter) {
    var up = String(letter || 'C').toUpperCase();
    return RL.el('span', {
      class: ['pip', 'pip--' + (COLOR_KEYS[up] ? up.toLowerCase() : 'generic')],
      title: MANA_NAME[up] || up,
      aria: { label: MANA_NAME[up] || up },
      role: 'img'
    }, RL.el('span', { class: 'pip__glyph', text: up }));
  };

  RL.manaVar = function (letter) {
    var up = String(letter || 'C').toUpperCase();
    return COLOR_KEYS[up] ? 'var(--mana-' + up.toLowerCase() + ')' : 'var(--mana-c)';
  };

  /* ==========================================================================
     7. RL.md — minimal markdown. ESCAPES FIRST, then builds tags.
        Supports: h1-h4, p, ul/ol (nested), tables, blockquote, hr,
                  fenced + inline code, **bold**, *italic*, ~~strike~~, links.
     ====================================================================== */
  var NUL = '\u0000'; // sentinel for protected spans; never occurs in real text

  function inlineMd(text) {
    var codes = [];
    // 1. protect inline code (content is already HTML-escaped)
    text = text.replace(/`([^`]+)`/g, function (_, c) {
      codes.push(c);
      return NUL + 'C' + (codes.length - 1) + NUL;
    });
    // 2. links [text](url)
    text = text.replace(/\[([^\]]*)\]\(([^)\s]+)(?:\s+&quot;([^&]*)&quot;)?\)/g,
      function (whole, label, url, title) {
        var lower = url.toLowerCase();
        if (lower.indexOf('javascript:') === 0 || lower.indexOf('data:') === 0) return label;
        var ext = /^https?:/i.test(url);
        return '<a href="' + url + '"' +
               (title ? ' title="' + title + '"' : '') +
               (ext ? ' target="_blank" rel="noopener noreferrer"' : '') + '>' +
               (label || url) + '</a>';
      });
    // 3. emphasis
    text = text.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>');
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/(^|[\s(])__([^_]+)__/g, '$1<strong>$2</strong>');
    text = text.replace(/\*([^*\n]+)\*/g, '<em>$1</em>');
    text = text.replace(/(^|[\s(])_([^_\n]+)_/g, '$1<em>$2</em>');
    text = text.replace(/~~([^~]+)~~/g, '<del>$1</del>');
    // 4. restore code
    text = text.replace(new RegExp(NUL + 'C(\\d+)' + NUL, 'g'), function (_, i) {
      return '<code class="md-code">' + codes[+i] + '</code>';
    });
    return text;
  }

  var BQ = /^\s*(?:&gt;|>)\s?/;

  function tableRowCells(line) {
    var s = line.trim().replace(/^\|/, '').replace(/\|$/, '');
    return s.split('|').map(function (c) { return c.trim(); });
  }

  function isTableDivider(line) {
    return /^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$/.test(line) && line.indexOf('-') >= 0 &&
           (line.indexOf('|') >= 0);
  }

  RL.md = function (src) {
    if (src === null || src === undefined) return '';
    var text = RL.escape(String(src)).replace(/\r\n?/g, '\n');

    // fenced code blocks -> placeholders
    var fences = [];
    text = text.replace(/```([^\n]*)\n([\s\S]*?)```/g, function (_, lang, body) {
      fences.push({ lang: String(lang || '').trim(), body: body.replace(/\n$/, '') });
      return NUL + 'F' + (fences.length - 1) + NUL;
    });

    var lines = text.split('\n');
    var out = [];
    var i = 0;

    function flushParagraph(buf) {
      if (!buf.length) return;
      out.push('<p>' + inlineMd(buf.join(' ')) + '</p>');
    }

    while (i < lines.length) {
      var line = lines[i];

      // fenced-code placeholder on its own line
      var fm = line.match(new RegExp('^' + NUL + 'F(\\d+)' + NUL + '$'));
      if (fm) {
        var f = fences[+fm[1]];
        out.push('<pre class="md-pre"' + (f.lang ? ' data-lang="' + f.lang + '"' : '') +
                 '><code>' + f.body + '</code></pre>');
        i++; continue;
      }

      if (!line.trim()) { i++; continue; }

      // heading
      var h = line.match(/^(#{1,6})\s+(.*?)\s*#*\s*$/);
      if (h) {
        var lvl = Math.min(h[1].length, 4);
        out.push('<h' + lvl + ' class="md-h md-h' + lvl + '">' + inlineMd(h[2]) + '</h' + lvl + '>');
        i++; continue;
      }

      // hr
      if (/^\s*([-*_])\s*\1\s*\1[\s\-*_]*$/.test(line)) { out.push('<hr class="md-hr">'); i++; continue; }

      // table
      if (line.indexOf('|') >= 0 && i + 1 < lines.length && isTableDivider(lines[i + 1])) {
        var head = tableRowCells(line);
        var aligns = tableRowCells(lines[i + 1]).map(function (c) {
          var l = c.charAt(0) === ':', r = c.charAt(c.length - 1) === ':';
          return l && r ? 'center' : (r ? 'right' : (l ? 'left' : ''));
        });
        i += 2;
        var rows = [];
        while (i < lines.length && lines[i].indexOf('|') >= 0 && lines[i].trim()) {
          rows.push(tableRowCells(lines[i])); i++;
        }
        var t = ['<div class="md-tablewrap"><table class="md-table"><thead><tr>'];
        head.forEach(function (c, ci) {
          t.push('<th scope="col"' + (aligns[ci] ? ' style="text-align:' + aligns[ci] + '"' : '') +
                 '>' + inlineMd(c) + '</th>');
        });
        t.push('</tr></thead><tbody>');
        rows.forEach(function (r) {
          t.push('<tr>');
          for (var c = 0; c < head.length; c++) {
            t.push('<td' + (aligns[c] ? ' style="text-align:' + aligns[c] + '"' : '') + '>' +
                   inlineMd(r[c] === undefined ? '' : r[c]) + '</td>');
          }
          t.push('</tr>');
        });
        t.push('</tbody></table></div>');
        out.push(t.join(''));
        continue;
      }

      // blockquote — note the &gt;: RL.escape() ran before this parser, so a
      // quote marker reaches us as "&gt;", not ">". Accept both.
      if (BQ.test(line)) {
        var qbuf = [];
        while (i < lines.length && (BQ.test(lines[i]) || (qbuf.length && lines[i].trim()))) {
          qbuf.push(lines[i].replace(BQ, ''));
          i++;
        }
        out.push('<blockquote class="md-quote">' + RL.md(unescapeForRecurse(qbuf.join('\n'))) + '</blockquote>');
        continue;
      }

      // lists (nested by indentation, 2 spaces per level)
      var lm = line.match(/^(\s*)([-*+]|\d+[.)])\s+(.*)$/);
      if (lm) {
        var stack = [];
        var html = [];
        while (i < lines.length) {
          var cur = lines[i];
          var cm = cur.match(/^(\s*)([-*+]|\d+[.)])\s+(.*)$/);
          if (!cm) {
            // lazy continuation of the previous item
            if (cur.trim() && stack.length) {
              html.push(' ' + inlineMd(cur.trim()));
              i++; continue;
            }
            break;
          }
          var depth = Math.floor(cm[1].replace(/\t/g, '  ').length / 2);
          var ordered = /\d/.test(cm[2]);
          var content = cm[3];

          while (stack.length > depth + 1) { html.push('</li></' + stack.pop() + '>'); }
          if (stack.length === depth + 1) {
            html.push('</li><li>');
          } else {
            while (stack.length < depth + 1) {
              var tag = ordered ? 'ol' : 'ul';
              stack.push(tag);
              html.push('<' + tag + ' class="md-list">' + '<li>');
            }
          }
          html.push(inlineMd(content));
          i++;
        }
        while (stack.length) { html.push('</li></' + stack.pop() + '>'); }
        out.push(html.join(''));
        continue;
      }

      // paragraph
      var pbuf = [];
      while (i < lines.length && lines[i].trim() &&
             !/^(#{1,6})\s/.test(lines[i]) &&
             !BQ.test(lines[i]) &&
             !/^(\s*)([-*+]|\d+[.)])\s+/.test(lines[i]) &&
             !new RegExp('^' + NUL + 'F\\d+' + NUL + '$').test(lines[i]) &&
             !(lines[i].indexOf('|') >= 0 && i + 1 < lines.length && isTableDivider(lines[i + 1]))) {
        pbuf.push(lines[i].replace(/\s+$/, '')); i++;
      }
      if (pbuf.length) flushParagraph(pbuf);
      else i++;
    }

    return out.join('\n');
  };

  /* Blockquotes recurse through RL.md, which escapes again — undo one layer. */
  function unescapeForRecurse(s) {
    return s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
            .replace(/&#39;/g, "'").replace(/&amp;/g, '&');
  }

  RL.mdEl = function (src, extraClass) {
    return RL.el('div', { class: ['md', extraClass || ''], html: RL.md(src) });
  };

  /* ==========================================================================
     8. Charts — hand-rolled inline SVG. No library, no rainbow, no dual axis.

     Rules baked in (a validator already settled these; do not re-litigate):
       - ONE hue for magnitude (--chart-single). A curve is not five things.
       - Per-datum colour is allowed ONLY for genuinely-colour data (mana), and
         a coloured datum MUST carry a text label — enforced with a throw below.
       - Every chart: accessible name, per-mark aria-label + tabindex, hover
         tooltip with the exact value, and a real <table> alternative.
       - Grow-in animation lives in CSS behind prefers-reduced-motion.
     ====================================================================== */
  var chartSeq = 0;

  function assertLabels(data, title) {
    data.forEach(function (d, i) {
      var hasColor = !!d.color;
      var hasLabel = d.label !== undefined && d.label !== null && String(d.label).trim() !== '';
      if (hasColor && !hasLabel) {
        throw new Error(
          '[RL.chart] datum ' + i + ' in "' + (title || 'untitled chart') + '" has a custom ' +
          'colour but no label. Colour is never the only encoding in this dashboard — ' +
          'give every coloured datum a visible label (W/U/B/R/G).');
      }
    });
  }

  function niceTicks(max, count) {
    if (!(max > 0)) return [0, 1];
    var raw = max / (count || 4);
    var mag = Math.pow(10, Math.floor(Math.log10(raw)));
    var norm = raw / mag;
    var step = (norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10) * mag;
    var ticks = [];
    for (var v = 0; v <= max + step * 0.001; v += step) ticks.push(+v.toFixed(6));
    if (ticks[ticks.length - 1] < max) ticks.push(ticks[ticks.length - 1] + step);
    return ticks;
  }

  function vBarPath(x, y, w, h, r) {
    r = Math.max(0, Math.min(r, w / 2, h));
    if (h <= 0.5) return '';
    return 'M' + x + ',' + (y + h) +
           'L' + x + ',' + (y + r) +
           'Q' + x + ',' + y + ' ' + (x + r) + ',' + y +
           'L' + (x + w - r) + ',' + y +
           'Q' + (x + w) + ',' + y + ' ' + (x + w) + ',' + (y + r) +
           'L' + (x + w) + ',' + (y + h) + 'Z';
  }

  function hBarPath(x, y, w, h, r) {
    r = Math.max(0, Math.min(r, h / 2, w));
    if (w <= 0.5) return '';
    return 'M' + x + ',' + y +
           'L' + (x + w - r) + ',' + y +
           'Q' + (x + w) + ',' + y + ' ' + (x + w) + ',' + (y + r) +
           'L' + (x + w) + ',' + (y + h - r) +
           'Q' + (x + w) + ',' + (y + h) + ' ' + (x + w - r) + ',' + (y + h) +
           'L' + x + ',' + (y + h) + 'Z';
  }

  /* figure + toolbar + tooltip + table alternative */
  function chartShell(spec, svg, tableNode) {
    var id = 'chart-' + (++chartSeq);
    var fig = RL.el('figure', { class: ['chart', spec.className || ''], id: id });

    var head = RL.el('div', { class: 'chart__head' });
    if (spec.title) {
      head.appendChild(RL.el('figcaption', { class: 'chart__title', text: spec.title }));
    }

    var tableWrap = RL.el('div', { class: 'chart__tablewrap', hidden: true, id: id + '-table' },
      tableNode);
    var canvas = RL.el('div', { class: 'chart__canvas' }, svg);

    var toggle = RL.el('button', {
      class: 'btn btn--ghost btn--sm chart__toggle',
      type: 'button',
      'aria-expanded': 'false',
      'aria-controls': id + '-table',
      on: {
        click: function () {
          var showing = tableWrap.hidden;
          tableWrap.hidden = !showing;
          canvas.hidden = showing;
          toggle.setAttribute('aria-expanded', showing ? 'true' : 'false');
          RL.clear(toggle);
          toggle.appendChild(RL.svgIcon(showing ? 'chart-bar' : 'table', 16));
          toggle.appendChild(RL.el('span', { text: showing ? 'Show chart' : 'Show table' }));
        }
      }
    }, RL.svgIcon('table', 16), RL.el('span', { text: 'Show table' }));

    head.appendChild(toggle);
    fig.appendChild(head);
    if (spec.description) {
      fig.appendChild(RL.el('p', { class: 'chart__desc', text: spec.description }));
    }
    fig.appendChild(canvas);
    fig.appendChild(tableWrap);

    // one tooltip per chart
    var tip = RL.el('div', { class: 'chart__tip', role: 'tooltip', hidden: true });
    fig.appendChild(tip);
    fig._tip = tip;
    wireTooltips(fig);

    if (spec.mount && spec.mount.appendChild) spec.mount.appendChild(fig);
    return fig;
  }

  /* Marks only carry their readout; the figure handles the events. Direct
     'focus' listeners on an SVG <g> are unreliable in Chrome (the element does
     take focus, but the handler is not guaranteed to run), so tooltips are
     delegated from the figure via focusin/mouseover, which always bubble. */
  function wireMark(fig, mark, text) {
    mark.setAttribute('data-readout', text);
  }

  function closestMark(node, root) {
    while (node && node !== root) {
      if (node.getAttribute && node.hasAttribute && node.hasAttribute('data-readout')) return node;
      node = node.parentNode;
    }
    return null;
  }

  function showTip(fig, mark) {
    var tip = fig._tip;
    if (!tip) return;
    tip.textContent = mark.getAttribute('data-readout') || '';
    tip.hidden = false;
    var fr = fig.getBoundingClientRect();
    var mr = mark.getBoundingClientRect();
    var left = mr.left - fr.left + mr.width / 2;
    var top = mr.top - fr.top;
    tip.style.left = Math.max(4, Math.min(left, fr.width - 4)) + 'px';
    tip.style.top = Math.max(0, top) + 'px';
  }

  function hideTip(fig) { if (fig._tip) fig._tip.hidden = true; }

  function wireTooltips(fig) {
    fig.addEventListener('mouseover', function (e) {
      var m = closestMark(e.target, fig);
      if (m) showTip(fig, m); else hideTip(fig);
    });
    fig.addEventListener('mouseleave', function () { hideTip(fig); });
    fig.addEventListener('focusin', function (e) {
      var m = closestMark(e.target, fig);
      if (m) showTip(fig, m); else hideTip(fig);
    });
    fig.addEventListener('focusout', function () { hideTip(fig); });
    fig.addEventListener('keydown', function (e) { if (e.key === 'Escape') hideTip(fig); });
    /* Belt and braces for the keyboard path: Chrome does not always emit focus
       events for an SVG <g>, but the keyup DOES bubble from whatever Tab just
       landed on. Read activeElement instead of trusting the focus event. */
    fig.addEventListener('keyup', function (e) {
      if (e.key !== 'Tab') return;
      var m = closestMark(document.activeElement, fig);
      if (m) showTip(fig, m); else hideTip(fig);
    });
  }

  function dataTable(spec, data, fmt) {
    var catHead = spec.categoryLabel || 'Category';
    var valHead = spec.valueLabel || 'Value';
    var total = data.reduce(function (a, d) { return a + (+d.value || 0); }, 0);
    var tbody = RL.el('tbody');
    data.forEach(function (d) {
      tbody.appendChild(RL.el('tr', null,
        RL.el('th', { scope: 'row', text: String(d.label) }),
        RL.el('td', { class: 'num', text: fmt(d.value) }),
        RL.el('td', { class: 'num', text: total > 0 ? RL.fmt.pct((d.value / total) * 100) : RL.fmt.dash })
      ));
    });
    return RL.el('table', { class: 'data-table data-table--chart' },
      RL.el('caption', { class: 'sr-only', text: (spec.title || 'Chart') + ' — data table' }),
      RL.el('thead', null, RL.el('tr', null,
        RL.el('th', { scope: 'col', text: catHead }),
        RL.el('th', { scope: 'col', class: 'num', text: valHead }),
        RL.el('th', { scope: 'col', class: 'num', text: 'Share' })
      )),
      tbody,
      RL.el('tfoot', null, RL.el('tr', null,
        RL.el('th', { scope: 'row', text: 'Total' }),
        RL.el('td', { class: 'num', text: fmt(total) }),
        RL.el('td', { class: 'num', text: total > 0 ? '100.0%' : RL.fmt.dash })
      ))
    );
  }

  function normalize(data) {
    return (data || []).map(function (d) {
      if (Array.isArray(d)) return { label: String(d[0]), value: +d[1] || 0 };
      // keep a missing label MISSING — assertLabels() below relies on it, and
      // String(undefined) === "undefined" would silently satisfy the check.
      var hasLabel = d.label !== undefined && d.label !== null;
      return { label: hasLabel ? String(d.label) : d.label, value: +d.value || 0,
               color: d.color, note: d.note };
    });
  }

  RL.chart = {};

  /* Charts draw in REAL pixels. A viewBox stretched to fit would shrink 12px
     labels to ~6px inside a narrow column, so instead we observe the canvas
     width and re-lay-out at 1 unit = 1 CSS px. Legibility does not depend on
     where a view decides to put the chart. */
  function autosize(fig, draw, fallbackW) {
    var canvas = fig.querySelector('.chart__canvas');
    var last = fallbackW;
    draw(fallbackW);
    function apply() {
      var w = Math.round((canvas && canvas.clientWidth) || 0) || fallbackW;
      w = Math.max(300, w);
      if (Math.abs(w - last) < 2) return;
      last = w;
      draw(w);
    }
    if (window.ResizeObserver) {
      try { new window.ResizeObserver(apply).observe(canvas); }
      catch (e) { window.addEventListener('resize', apply); }
    } else {
      window.addEventListener('resize', apply);
    }
    window.requestAnimationFrame(apply);
  }

  /* ---- vertical bars: mana curve, price tiers, anything magnitude ------- */
  RL.chart.bar = function (spec) {
    spec = spec || {};
    var data = normalize(spec.data);
    assertLabels(data, spec.title);
    var fmt = spec.format || RL.fmt.int;
    var H = spec.height || 240;

    var svg = RL.svgEl('svg', {
      class: 'chart__svg', role: 'group', preserveAspectRatio: 'xMidYMid meet',
      aria: { label: spec.title || 'Bar chart' }
    });
    var fig = chartShell(spec, svg, dataTable(spec, data, fmt));

    function draw(W) {
      RL.clear(svg);
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
      svg.appendChild(RL.svgEl('title', { text: spec.title || 'Bar chart' }));

      var padL = 38, padR = 10, padT = 18, padB = 34;
      var plotW = W - padL - padR, plotH = H - padT - padB;
      var n = Math.max(data.length, 1);
      var gap = Math.max(2, Math.min(12, plotW / n * 0.2));
      var barW = Math.max(3, (plotW - gap * (n - 1)) / n);
      var max = data.reduce(function (a, d) { return Math.max(a, d.value); }, 0);
      var ticks = niceTicks(max, 4);
      var top = ticks[ticks.length - 1] || 1;

      var grid = RL.svgEl('g', { class: 'chart__grid' });
      ticks.forEach(function (t) {
        var y = padT + plotH - (t / top) * plotH;
        grid.appendChild(RL.svgEl('line', { x1: padL, x2: W - padR, y1: y, y2: y }));
        grid.appendChild(RL.svgEl('text', {
          x: padL - 8, y: y + 4, class: 'chart__ticklabel', 'text-anchor': 'end', text: fmt(t)
        }));
      });
      svg.appendChild(grid);

      var marks = RL.svgEl('g', { class: 'chart__marks' });
      data.forEach(function (d, idx) {
        var x = padL + idx * (barW + gap);
        var h = top > 0 ? (d.value / top) * plotH : 0;
        var y = padT + plotH - h;
        var readout = d.label + ': ' + fmt(d.value) +
                      (spec.valueLabel ? ' ' + spec.valueLabel.toLowerCase() : '');

        var g = RL.svgEl('g', {
          class: 'mark mark--bar', tabindex: '0', role: 'img',
          aria: { label: readout }, style: '--d:' + (idx * 28) + 'ms'
        });
        g.appendChild(RL.svgEl('rect', {
          class: 'mark__hit', x: x, y: padT, width: barW, height: plotH, rx: 2
        }));
        var path = vBarPath(x, y, barW, h, 4);
        g.appendChild(RL.svgEl('path', path
          ? { class: 'bar-v', d: path, fill: d.color || 'var(--chart-single)' }
          : { class: 'bar-v bar-v--zero', d: vBarPath(x, padT + plotH - 2, barW, 2, 1),
              fill: 'var(--chart-grid)' }));
        if (spec.showValues !== false && barW >= 16) {
          g.appendChild(RL.svgEl('text', {
            class: 'chart__value', x: x + barW / 2, y: Math.max(padT + 9, y - 6),
            'text-anchor': 'middle', text: fmt(d.value)
          }));
        }
        g.appendChild(RL.svgEl('text', {
          class: 'chart__catlabel', x: x + barW / 2, y: H - padB + 18,
          'text-anchor': 'middle', text: d.label
        }));
        marks.appendChild(g);
        wireMark(fig, g, readout);
      });
      svg.appendChild(marks);
      svg.appendChild(RL.svgEl('line', {
        class: 'chart__axis', x1: padL, x2: W - padR, y1: padT + plotH, y2: padT + plotH
      }));
    }

    autosize(fig, draw, 640);
    return fig;
  };

  /* ---- horizontal bars: role counts, colour sources --------------------- */
  RL.chart.hbar = function (spec) {
    spec = spec || {};
    var data = normalize(spec.data);
    assertLabels(data, spec.title);
    var fmt = spec.format || RL.fmt.int;

    var rowH = spec.rowHeight || 26;
    var gap = 8, padT = 6, padB = 22;
    var n = Math.max(data.length, 1);
    var H = padT + padB + n * rowH + (n - 1) * gap;

    var svg = RL.svgEl('svg', {
      class: 'chart__svg', role: 'group', preserveAspectRatio: 'xMidYMid meet',
      aria: { label: spec.title || 'Horizontal bar chart' }
    });
    var fig = chartShell(spec, svg, dataTable(spec, data, fmt));

    function draw(W) {
      RL.clear(svg);
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
      svg.appendChild(RL.svgEl('title', { text: spec.title || 'Horizontal bar chart' }));

      // the label gutter adapts to the width so long role names still fit
      var padL = Math.max(64, Math.min(spec.labelWidth || 116, Math.round(W * 0.34)));
      var padR = 46;
      var plotW = Math.max(40, W - padL - padR);
      var max = data.reduce(function (a, d) { return Math.max(a, d.value); }, 0);
      var ticks = niceTicks(max, W < 420 ? 2 : 4);
      var top = ticks[ticks.length - 1] || 1;

      var grid = RL.svgEl('g', { class: 'chart__grid' });
      ticks.forEach(function (t) {
        var x = padL + (t / top) * plotW;
        grid.appendChild(RL.svgEl('line', { x1: x, x2: x, y1: padT, y2: H - padB }));
        grid.appendChild(RL.svgEl('text', {
          x: x, y: H - padB + 15, class: 'chart__ticklabel', 'text-anchor': 'middle', text: fmt(t)
        }));
      });
      svg.appendChild(grid);

      var marks = RL.svgEl('g', { class: 'chart__marks' });
      data.forEach(function (d, idx) {
        var y = padT + idx * (rowH + gap);
        var w = top > 0 ? (d.value / top) * plotW : 0;
        var readout = d.label + ': ' + fmt(d.value) +
                      (spec.valueLabel ? ' ' + spec.valueLabel.toLowerCase() : '');

        var g = RL.svgEl('g', {
          class: 'mark mark--hbar', tabindex: '0', role: 'img',
          aria: { label: readout }, style: '--d:' + (idx * 28) + 'ms'
        });
        g.appendChild(RL.svgEl('rect', {
          class: 'mark__hit', x: 0, y: y, width: W, height: rowH, rx: 2
        }));
        g.appendChild(RL.svgEl('text', {
          class: 'chart__rowlabel', x: padL - 10, y: y + rowH / 2 + 4,
          'text-anchor': 'end', text: d.label
        }));
        var path = hBarPath(padL, y + 3, w, rowH - 6, 4);
        g.appendChild(RL.svgEl('path', path
          ? { class: 'bar-h', d: path, fill: d.color || 'var(--chart-single)' }
          : { class: 'bar-h bar-h--zero', d: hBarPath(padL, y + 3, 2, rowH - 6, 1),
              fill: 'var(--chart-grid)' }));
        g.appendChild(RL.svgEl('text', {
          class: 'chart__value', x: padL + w + 8, y: y + rowH / 2 + 4,
          'text-anchor': 'start', text: fmt(d.value)
        }));
        marks.appendChild(g);
        wireMark(fig, g, readout);
      });
      svg.appendChild(marks);
      svg.appendChild(RL.svgEl('line', {
        class: 'chart__axis', x1: padL, x2: padL, y1: padT, y2: H - padB
      }));
    }

    autosize(fig, draw, 640);
    return fig;
  };

  /* ---- donut: proportion only, <= 5 categories -------------------------- */
  RL.chart.donut = function (spec) {
    spec = spec || {};
    var data = normalize(spec.data).filter(function (d) { return d.value > 0; });
    assertLabels(data, spec.title);
    if (data.length > 5) {
      console.warn('[RL.chart.donut] ' + data.length + ' categories — a donut reads badly past 5. ' +
                   'Use RL.chart.hbar for anything longer.');
    }
    var fmt = spec.format || RL.fmt.int;
    var pendingMarks = [];
    var total = data.reduce(function (a, d) { return a + d.value; }, 0);

    var S = 260, cx = S / 2, cy = S / 2, rOut = 108, rIn = 66;
    var svg = RL.svgEl('svg', {
      viewBox: '0 0 ' + S + ' ' + S, class: 'chart__svg chart__svg--donut',
      role: 'group', preserveAspectRatio: 'xMidYMid meet',
      aria: { label: spec.title || 'Proportion chart' }
    });
    svg.appendChild(RL.svgEl('title', { text: spec.title || 'Proportion chart' }));

    function polar(r, a) {
      return [cx + r * Math.cos(a - Math.PI / 2), cy + r * Math.sin(a - Math.PI / 2)];
    }

    var acc = 0;
    var marks = RL.svgEl('g', { class: 'chart__marks' });
    var GAP = data.length > 1 ? 0.022 : 0; // radians of separation between slices

    data.forEach(function (d, idx) {
      var frac = total > 0 ? d.value / total : 0;
      var a0 = acc * Math.PI * 2 + GAP / 2;
      var a1 = (acc + frac) * Math.PI * 2 - GAP / 2;
      acc += frac;
      if (a1 <= a0) a1 = a0 + 0.001;
      var large = (a1 - a0) > Math.PI ? 1 : 0;
      var p0 = polar(rOut, a0), p1 = polar(rOut, a1);
      var q1 = polar(rIn, a1), q0 = polar(rIn, a0);
      var dPath = 'M' + p0[0] + ',' + p0[1] +
                  'A' + rOut + ',' + rOut + ' 0 ' + large + ' 1 ' + p1[0] + ',' + p1[1] +
                  'L' + q1[0] + ',' + q1[1] +
                  'A' + rIn + ',' + rIn + ' 0 ' + large + ' 0 ' + q0[0] + ',' + q0[1] + 'Z';
      var readout = d.label + ': ' + fmt(d.value) + ' (' + RL.fmt.pct(frac * 100) + ')';

      var g = RL.svgEl('g', {
        class: 'mark mark--slice', tabindex: '0', role: 'img',
        aria: { label: readout }, style: '--d:' + (idx * 40) + 'ms'
      });
      g.appendChild(RL.svgEl('path', {
        class: 'slice', d: dPath, fill: d.color || 'var(--chart-single)'
      }));
      // direct label ON the slice — colour is never the only encoding
      if (frac > 0.06) {
        var mid = polar((rOut + rIn) / 2, (a0 + a1) / 2);
        g.appendChild(RL.svgEl('text', {
          class: 'chart__slicelabel', x: mid[0], y: mid[1] + 4, 'text-anchor': 'middle',
          text: String(d.label)
        }));
      }
      marks.appendChild(g);
      pendingMarks.push([g, readout]);
    });
    svg.appendChild(marks);

    svg.appendChild(RL.svgEl('text', {
      class: 'chart__centerval', x: cx, y: cy - 2, 'text-anchor': 'middle', text: fmt(total)
    }));
    svg.appendChild(RL.svgEl('text', {
      class: 'chart__centerlab', x: cx, y: cy + 18, 'text-anchor': 'middle',
      text: spec.centerLabel || 'total'
    }));

    var fig = chartShell(spec, svg, dataTable(spec, data, fmt));
    pendingMarks.forEach(function (m) { wireMark(fig, m[0], m[1]); });

    // legend: swatch + label + value, always visible (the second encoding)
    var legend = RL.el('ul', { class: 'chart__legend' });
    data.forEach(function (d) {
      legend.appendChild(RL.el('li', { class: 'chart__legenditem' },
        RL.el('span', {
          class: 'chart__swatch', 'aria-hidden': 'true',
          style: { '--swatch': d.color || 'var(--chart-single)' }
        }),
        RL.el('span', { class: 'chart__legendlabel', text: String(d.label) }),
        RL.el('span', { class: 'chart__legendval', text: fmt(d.value) })
      ));
    });
    fig.insertBefore(legend, fig.querySelector('.chart__tablewrap'));
    return fig;
  };

  /* Convenience: a compact key/value stat tile used across views. */
  RL.stat = function (label, value, opts) {
    opts = opts || {};
    return RL.el('div', { class: ['stat', opts.tone ? 'stat--' + opts.tone : ''] },
      RL.el('div', { class: 'stat__label', text: label }),
      RL.el('div', { class: 'stat__value' }, value instanceof Node ? value : String(value)),
      opts.note ? RL.el('div', { class: 'stat__note', text: opts.note }) : null
    );
  };

  /* ==========================================================================
     9. Router — hash based: #/<viewId>/<param>/<param>
        Deep-linkable, back/forward works, scroll restored per route,
        focus moves to <main> on every route change.
     ====================================================================== */
  var views = Object.create(null);
  var viewOrder = [];
  var current = null;          // {id, params, el}
  var scrollMemory = Object.create(null);
  var started = false;
  var host = null;

  RL.registerView = function (view) {
    if (!view || !view.id) { console.error('[RL] registerView needs {id,...}', view); return; }
    if (views[view.id]) { console.warn('[RL] view "' + view.id + '" re-registered'); }
    else viewOrder.push(view.id);
    views[view.id] = view;
    RL.emit('view', view);
    if (started) buildNav();
  };

  RL.views = function () { return viewOrder.map(function (id) { return views[id]; }); };
  RL.view = function (id) { return views[id] || null; };

  RL.parseHash = function (hash) {
    var h = String(hash === undefined ? window.location.hash : hash).replace(/^#\/?/, '');
    var parts = h.split('/').filter(function (p) { return p !== ''; })
                 .map(function (p) { try { return decodeURIComponent(p); } catch (e) { return p; } });
    return { id: parts[0] || '', params: parts.slice(1) };
  };

  RL.route = function () { return current ? { id: current.id, params: current.params.slice() } : RL.parseHash(); };

  RL.href = function (id) {
    var params = Array.prototype.slice.call(arguments, 1);
    if (params.length === 1 && Array.isArray(params[0])) params = params[0];
    return '#/' + [id].concat(params.map(function (p) { return encodeURIComponent(String(p)); })).join('/');
  };

  RL.navigate = function (id) {
    var params = Array.prototype.slice.call(arguments, 1);
    if (params.length === 1 && Array.isArray(params[0])) params = params[0];
    var next = RL.href(id, params);
    if (window.location.hash === next) render();
    else window.location.hash = next;
  };

  RL.replace = function (id) {
    var params = Array.prototype.slice.call(arguments, 1);
    if (params.length === 1 && Array.isArray(params[0])) params = params[0];
    var next = RL.href(id, params);
    if (window.history && window.history.replaceState) {
      window.history.replaceState(null, '', next);
      render();
    } else {
      window.location.hash = next;
    }
  };

  function routeKey(r) { return r.id + '/' + r.params.join('/'); }

  /* Views render into their own persistent container so they can cache DOM. */
  function containerFor(id) {
    var view = views[id];
    if (view._el) return view._el;
    var el = RL.el('section', {
      class: 'view view--' + id,
      id: 'view-' + id,
      'data-view': id,
      hidden: true
    });
    view._el = el;
    host.appendChild(el);
    return el;
  }

  function renderFailure(el, id, err) {
    console.error('[RL] view "' + id + '" failed', err);
    RL.clear(el);
    el.appendChild(RL.el('div', { class: 'panel state state--bad' },
      RL.el('div', { class: 'state__icon' }, RL.svgIcon('alert-triangle', 28)),
      RL.el('h2', { class: 'state__title', text: 'This view hit an error' }),
      RL.el('p', { class: 'state__body' },
        'The ', RL.el('strong', { text: id }), ' view threw while rendering. ' +
        'Everything else still works — pick another section in the sidebar.'),
      RL.el('pre', { class: 'state__pre', text: String((err && err.stack) || err) })
    ));
  }

  var beforeRenderHook = null;
  RL.setRouteGuard = function (fn) { beforeRenderHook = fn; }; // boot.js uses this for the empty state

  function render() {
    if (!host) return;
    var r = RL.parseHash();
    var id = r.id;

    if (!id || !views[id]) {
      var fallback = viewOrder[0];
      if (!fallback) return; // nothing registered at all — boot.js handles it
      if (id && id !== fallback) console.warn('[RL] no view "' + id + '" — falling back to "' + fallback + '"');
      RL.replace(fallback);
      return;
    }

    // remember where we were
    if (current) {
      scrollMemory[routeKey(current)] = window.scrollY || window.pageYOffset || 0;
      if (current.id !== id) {
        var prev = views[current.id];
        try { if (prev.onLeave) prev.onLeave(prev._el); } catch (e) { console.error('[RL] onLeave threw', e); }
        if (prev._el) prev._el.hidden = true;
      }
    }

    if (beforeRenderHook && beforeRenderHook(r) === false) {
      current = { id: id, params: r.params };
      RL.emit('route', RL.route());
      return;
    }

    var view = views[id];
    var el = containerFor(id);
    el.hidden = false;

    // Publish the new route BEFORE the view runs, so RL.route() is accurate
    // inside mount()/onEnter() rather than reporting the page we just left.
    var wasSameView = current && current.id === id;
    current = { id: id, params: r.params };

    if (!view._mounted) {
      view._mounted = true;
      try { if (view.mount) view.mount(el, r.params.slice()); }
      catch (e) { renderFailure(el, id, e); }
    }
    try { if (view.onEnter) view.onEnter(r.params.slice(), el); }
    catch (e) { renderFailure(el, id, e); }

    // a11y: move focus to <main> on route change (not on a param-only refresh
    // of the same view, which would yank focus away mid-interaction)
    var main = document.getElementById('main');
    if (main && !wasSameView) {
      try { main.focus({ preventScroll: true }); } catch (e) { main.focus(); }
    }

    // restore the scroll position we last had on THIS exact route; new routes start at the top
    var remembered = scrollMemory[routeKey(current)] || 0;
    window.requestAnimationFrame(function () { window.scrollTo(0, remembered); });

    RL.emit('route', RL.route());
  }

  RL.render = render;

  var navBuilder = null;
  RL.setNavBuilder = function (fn) { navBuilder = fn; };
  function buildNav() { if (navBuilder) navBuilder(); }

  RL.start = function (hostEl) {
    host = hostEl || document.getElementById('viewHost');
    if (!host) { console.error('[RL] no #viewHost to render into'); return; }
    started = true;
    window.addEventListener('hashchange', render);
    buildNav();
    render();
  };

  window.RL = RL;
})(window, document);

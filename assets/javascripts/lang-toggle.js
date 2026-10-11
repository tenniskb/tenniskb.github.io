/* =========================================================================
   Tennis Unified & TennisKB — Dynamic Language Toggle Script (v2)
   Switches dynamically between corresponding English and Vietnamese pages.

   Language detection is SEGMENT-AWARE: a page is Vietnamese iff one of its
   path segments is exactly "vi" (at any position), not only at the start.
   This fixes subtrees such as /tenniskb/vi/  <->  /tenniskb/en/  and
   /tnkb/vi/  <->  /tnkb/en/, where the language directory is nested.

   Priority when computing the counterpart URL:
     1. An explicit data-lang-href written on the element at build time
        (authoritative — overrides everything below).
     2. A <link rel="alternate" hreflang="..."> in <head> (if present).
     3. Article / pillar heuristics.
     4. General SEGMENT-AWARE swap:
          - /vi/x           <-> /x            (root-level prefix)
          - /en/x           <-> /vi/x
          - /tenniskb/vi/x  <-> /tenniskb/en/x (nested directory swap)
   ========================================================================= */

(function () {
  'use strict';

  if (typeof window === 'undefined' || typeof document === 'undefined') return;

  var LANG_SEG = /^(vi|en)$/i;
  var pillarEnToVi = {
    'biomechanics': 'co-sinh-hoc',
    'neuro-athletics': 'than-kinh',
    'stroke-mechanics': 'cu-danh',
    'tactics': 'chien-thuat',
    'conditioning': 'the-luc'
  };
  var pillarViToEn = {};
  for (var pk in pillarEnToVi) {
    if (Object.prototype.hasOwnProperty.call(pillarEnToVi, pk)) {
      pillarViToEn[pillarEnToVi[pk]] = pk;
    }
  }

  function getLangToggles() {
    return document.querySelectorAll('[data-lang-toggle], a.tu-nav-lang');
  }

  // Index of a path segment that is exactly 'vi' or 'en' (any position), else -1.
  function langSegmentIndex(path) {
    var parts = path.split('/');
    for (var i = 0; i < parts.length; i++) {
      if (LANG_SEG.test(parts[i])) return i;
    }
    return -1;
  }

  function isVietnamesePath(path) {
    var i = langSegmentIndex(path);
    if (i !== -1) return /^vi$/i.test(path.split('/')[i]);
    return false;
  }

  // Authoritative, build-time target written on the element itself.
  function getExplicitTarget(el) {
    var h = el.getAttribute('data-lang-href');
    if (h && (h.charAt(0) === '/' || /^https?:\/\//i.test(h))) {
      return h.replace(/^https?:\/\/[^\/]+/i, '');
    }
    return null;
  }

  function resolveAlt(selector) {
    var alt = document.querySelector(selector);
    if (!alt) return null;
    var href = alt.getAttribute('href');
    if (!href) return null;
    if (/^https?:\/\//i.test(href)) return href.replace(/^https?:\/\/[^\/]+/i, '');
    if (href.charAt(0) === '/') return href;
    try { return new URL(href, window.location.href).pathname; } catch (e) { return null; }
  }

  function buildTargetUrl(currentPath, currentSearch) {
    currentPath = currentPath || window.location.pathname;
    currentSearch = (currentSearch !== undefined) ? currentSearch : window.location.search;
    var isVi = isVietnamesePath(currentPath);

    // 1. Authoritative <link rel="alternate" hreflang> if present.
    var alt = resolveAlt(isVi ? 'link[rel="alternate"][hreflang="en"]' : 'link[rel="alternate"][hreflang="vi"]');
    if (alt) return alt;

    // 2. Individual Article Pages (200 Articles): EN-xxx <-> VI-xxx
    var mEn = currentPath.match(/^(?:\/en)?\/articles\/EN-(.*)$/i);
    if (mEn) return '/vi/articles/VI-' + mEn[1];
    var mVi = currentPath.match(/^\/vi\/articles\/VI-(.*)$/i);
    if (mVi) return '/en/articles/EN-' + mVi[1];

    // 3. Pillar Taxonomy Categories in Articles
    for (var pen in pillarEnToVi) {
      if (Object.prototype.hasOwnProperty.call(pillarEnToVi, pen) &&
          currentPath.indexOf('/articles/' + pen) !== -1) {
        return '/vi/articles/' + pillarEnToVi[pen] + '/';
      }
    }
    for (var pvi in pillarViToEn) {
      if (Object.prototype.hasOwnProperty.call(pillarViToEn, pvi) &&
          currentPath.indexOf('/vi/articles/' + pvi) !== -1) {
        return '/en/articles/' + pillarViToEn[pvi] + '/';
      }
    }

    // 4. Articles Catalog Main Index
    if (/^\/(?:en\/)?articles\/?$/i.test(currentPath)) return '/vi/articles/';
    if (/^\/vi\/articles\/?$/i.test(currentPath)) return '/en/articles/';

    // 5. 5 Pillars & 10 Pillars Knowledge Bases
    var pillars = ['Tenniskb-5 Pillars', 'Tenniskb-10 Pillars'];
    for (var p = 0; p < pillars.length; p++) {
      var pName = pillars[p];
      if (currentPath.indexOf('/vi/' + pName) !== -1) {
        var enPath = currentPath.replace('/vi/' + pName, '/' + pName);
        var enSearch = currentSearch.replace(/_VN\.md/gi, '_EN.md').replace(/lang=vi/gi, 'lang=en');
        return enPath + enSearch;
      }
      if (currentPath.indexOf('/' + pName) !== -1) {
        var viPath = currentPath.replace('/' + pName, '/vi/' + pName);
        var viSearch = currentSearch.replace(/_EN\.md/gi, '_VN.md').replace(/lang=en/gi, 'lang=vi');
        return viPath + viSearch;
      }
    }

    // 6. General fallback — SEGMENT-AWARE swap (fixes /tenniskb/vi/ etc.)
    var parts = currentPath.split('/');
    var idx = langSegmentIndex(currentPath);
    if (idx !== -1) {
      var cur = parts[idx].toLowerCase();
      // A language segment at index 1 means a ROOT-LEVEL prefix (/vi/x, /en/x).
      // split('/') yields ['', 'vi', ...] so the real first segment is index 1.
      if (idx === 1) {
        if (cur === 'vi') {
          return '/' + parts.slice(2).join('/');        // /vi/x -> /x
        }
        parts[1] = 'vi';                                 // /en/x -> /vi/x
        return parts.join('/');
      }
      parts[idx] = (cur === 'vi') ? 'en' : 'vi';         // /tenniskb/vi/x <-> /tenniskb/en/x
      return parts.join('/');
    }

    // 7. No language segment -> treat as EN. VI counterpart is a nested or
    //    prefixed sibling. Subtrees (/tenniskb/, /tnkb/) use the nested form
    //    (/tenniskb/vi/x); the main site uses the prefixed form (/vi/x).
    //    Pages that need an exact target should carry data-lang-href.
    if (currentPath === '/' || currentPath === '') return '/vi/';
    var nested = parts.slice();
    nested.splice(2, 0, 'vi');
    return nested.join('/');
  }

  function updateToggleElements() {
    var toggles = getLangToggles();
    if (!toggles || toggles.length === 0) return;

    var currentPath = window.location.pathname;
    var target = buildTargetUrl(currentPath, window.location.search);
    var isVi = isVietnamesePath(currentPath);

    toggles.forEach(function (toggle) {
      // 1. Explicit, build-time target wins.
      var explicit = getExplicitTarget(toggle);
      if (explicit) target = explicit;
      toggle.setAttribute('href', target);
      var textEl = toggle.querySelector('.tu-nav-text');
      if (textEl) {
        textEl.textContent = isVi ? 'EN' : 'VI';
      }
      toggle.setAttribute('title', isVi ? 'Switch to English' : 'Chuyển sang Tiếng Việt');
    });

    // Also update any MkDocs header dropdown language links if present.
    var targetLang = isVi ? 'en' : 'vi';
    var selectLinks = document.querySelectorAll('.md-select__link[hreflang="' + targetLang + '"]');
    selectLinks.forEach(function (link) {
      link.setAttribute('href', target);
    });
  }

  function init() {
    updateToggleElements();

    // Capture-phase click listener to guarantee latest dynamic target on click.
    document.addEventListener('click', function (e) {
      var toggle = e.target && e.target.closest && e.target.closest('[data-lang-toggle], a.tu-nav-lang, .md-select__link');
      if (toggle) {
        var explicit = getExplicitTarget(toggle);
        var target = explicit || buildTargetUrl(window.location.pathname, window.location.search);
        if (target) toggle.setAttribute('href', target);
      }
    }, true);

    // Watch for dynamic head updates (e.g. single-page doc navigation).
    if (window.MutationObserver && document.head) {
      var observer = new MutationObserver(function () {
        updateToggleElements();
      });
      observer.observe(document.head, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

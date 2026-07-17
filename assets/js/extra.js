// Cross-language tab URL fix.
// The mkdocs-static-i18n plugin uses a single shared nav: across all language
// builds, so the cross-language tab's href is the same in both EN and VI.
// At runtime we detect the current language and rewrite the cross-link tab
// to point at the *other* language's site root.
(function () {
  function fixCrossLangTab() {
    var path = window.location.pathname;  // e.g. "/tenniskb/vi/..."
    var isVi = path.indexOf("/vi/") !== -1 || /\/vi(\/|$|\.)/.test(path);
    var crossLinks = document.querySelectorAll(".md-tabs__link[href*='tenniskb/'], .md-nav__link[href*='tenniskb/']");
    crossLinks.forEach(function (a) {
      var href = a.getAttribute("href") || "";
      if (isVi) {
        // Currently on VI site -> point cross-link to EN site
        if (href.indexOf("/vi/index.html") !== -1 || href.indexOf("/vi/") !== -1) {
          a.setAttribute("href", "https://henryphamduc.github.io/tenniskb/en/index.html");
        }
      } else {
        // Currently on EN site (or root) -> point cross-link to VI site
        if (href.indexOf("/en/index.html") !== -1 || href.indexOf("/en/") !== -1) {
          a.setAttribute("href", "https://henryphamduc.github.io/tenniskb/vi/index.html");
        }
      }
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fixCrossLangTab);
  } else {
    fixCrossLangTab();
  }
})();

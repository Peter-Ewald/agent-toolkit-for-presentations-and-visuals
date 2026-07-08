// Reads the version already present in each card's Artifactory link and
// renders it as a badge, so the badge can never drift from the link — there
// is only ever one place (the href) where the version is typed.
document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll(".md-typeset .grid.cards > ul > li, .md-typeset .grid.cards > ol > li")
    .forEach(function (card) {
      var link = card.querySelector('a[href*="artifactory.ramboll.com"]');
      if (!link) return;
      var match = link.href.match(/\/([0-9]+\.[0-9]+\.[0-9]+)(?:[/?]|$)/);
      if (!match) return;
      var badge = document.createElement("span");
      badge.className = "ramboll-version-badge";
      badge.textContent = "v" + match[1];
      card.appendChild(badge);
    });
});

// Inserts a header strip above mkdocs-material's own header, replicating
// the Astro portal's own header (brand link, nav, static Ramboll mark) — a
// DOM-insertion approach rather than a Jinja2 template override, since
// there's no way to visually verify a template partial's correctness ahead
// of time. Every mkdocs site loads this same script, so it looks and
// behaves identically everywhere, including the portal itself.
document.addEventListener("DOMContentLoaded", function () {
  // This script's own <script src="…/_theme/ramboll.js"> tells us the
  // correct relative path to the rest of _theme/ regardless of how deeply
  // nested the current page is (e.g. /docs/workshop/01-setup/ needs
  // "../_theme/", while /docs/workshop/ needs "_theme/") — mkdocs already
  // resolved that once for this very script, so re-deriving it from
  // window.location would duplicate logic mkdocs already got right.
  var scriptEl = document.currentScript || document.querySelector('script[src*="ramboll.js"]');
  var themeBase = scriptEl ? scriptEl.src.replace(/ramboll\.js.*$/, "") : "";

  // "Get Started" is deliberately not in this list — the brand link below
  // already goes to Home, which is where the get-started role cards live.
  var navLinks = [
    { href: "/overview/", label: "Overview" },
    { href: "/packages/", label: "Packages" },
    { href: "/services/", label: "Services" },
    { href: "/docs/workshop/", label: "Workshop" },
  ];

  var header = document.createElement("div");
  header.className = "ramboll-portal-header";

  // Inner row is constrained/centered the same way the portal's own header
  // is (max-width + margin auto) — the outer .ramboll-portal-header stays
  // full-bleed only for its white background, matching how the portal's
  // <header> (full-bleed) and inner <nav> (constrained) are split.
  var inner = document.createElement("div");
  inner.className = "ramboll-portal-header__inner";
  header.appendChild(inner);

  var brand = document.createElement("a");
  brand.className = "ramboll-portal-header__brand";
  brand.href = "/";
  brand.textContent = "LOGO SEMANTIC EVALUATION";
  inner.appendChild(brand);

  var nav = document.createElement("div");
  nav.className = "ramboll-portal-header__nav";
  navLinks.forEach(function (item) {
    var a = document.createElement("a");
    a.href = item.href;
    a.textContent = item.label;
    nav.appendChild(a);
  });
  inner.appendChild(nav);

  var logo = document.createElement("img");
  logo.className = "ramboll-portal-header__logo";
  logo.src = themeBase + "logo.svg";
  logo.alt = "Ramboll";
  inner.appendChild(logo);

  document.body.insertBefore(header, document.body.firstChild);
});

// Bolds "Getting started" and "Changelog" in the left sidebar nav — mkdocs
// generates that nav straight from mkdocs.yml with no way to mark individual
// entries in the YAML itself, so this matches on the rendered label text
// instead. Runs against every ".md-nav__link" (mkdocs renders the nav twice,
// once for the desktop sidebar and once for the mobile drawer) so both stay
// in sync.
document.addEventListener("DOMContentLoaded", function () {
  var emphasizedLabels = ["Getting started", "Changelog"];
  document.querySelectorAll(".md-nav__link").forEach(function (link) {
    var label = (link.textContent || "").trim();
    if (emphasizedLabels.indexOf(label) !== -1) {
      link.classList.add("ramboll-nav-emphasis");
    }
  });
});

// Shows "<kind> · latest vX.Y.Z" next to the site name in the native
// mkdocs-material header, for the two published SDK sites only.
// window.RAMBOLL_PACKAGE_INFO is set by a small per-site generated script
// (_theme/ramboll-package-info.js, written by build_local_site.sh straight
// from each SDK's pyproject.toml) — this shared ramboll.js file stays
// identical across every site, the version data lives in the one
// site-specific file instead. Sites without that global (scoring-service,
// review-sync-service, workshop) simply skip this, unchanged.
document.addEventListener("DOMContentLoaded", function () {
  var info = window.RAMBOLL_PACKAGE_INFO;
  if (!info) return;
  var topic = document.querySelector(".md-header__topic");
  if (!topic) return;
  var badge = document.createElement("span");
  badge.className = "ramboll-package-badge";
  badge.textContent = info.kind + " · latest v" + info.version;
  topic.appendChild(badge);
});

// Drops the "Made with Material for MkDocs" attribution mkdocs-material adds
// after our own copyright line — there's no documented mkdocs.yml setting to
// suppress it short of overriding the footer template, so this removes the
// trailing text/link nodes that follow .md-copyright__highlight instead.
document.addEventListener("DOMContentLoaded", function () {
  var highlight = document.querySelector(".md-copyright__highlight");
  if (!highlight) return;
  while (highlight.nextSibling) {
    highlight.parentNode.removeChild(highlight.nextSibling);
  }
});

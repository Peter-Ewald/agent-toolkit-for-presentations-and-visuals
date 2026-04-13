---
marp: true
theme: default
size: 16:9
paginate: true
style: |
  :root {
    --ramboll-cyan: #0094e3;
    --ramboll-title-blue: #0094e3;
    --ramboll-cyan-20: #cceafb;
    --ramboll-cyan-10: #e5f4fd;
    --ramboll-ocean: #05326e;
    --ramboll-ocean-80: #375b8b;
    --ramboll-forest: #125a40;
    --ramboll-heath: #62294b;
    --ramboll-mountain: #273943;
    --ramboll-grass: #add095;
    --ramboll-pebble: #e3e1d8;
    --ramboll-pebble-20: #f9f9f7;
    --ramboll-pebble-10: #fcfcfb;
    --ramboll-field: #ff8855;
    --ramboll-sand: #ffe682;
    --ramboll-text: #000000;
    --ramboll-muted: #7d888e;
    --ramboll-page-number: #6984a8;
    --ramboll-divider: #b1b2b3;
  }

  section {
    display: flex;
    flex-direction: column;
    justify-content: flex-start !important;
    align-items: flex-start !important;
    align-content: flex-start !important;
    place-content: flex-start !important;
    font-family: "NunitoCustom", Nunito, Verdana, "Segoe UI", sans-serif;
    color: var(--ramboll-text);
    background: #ffffff;
    padding: 34px 38px 28px 38px;
    font-size: 23px;
    position: relative;
  }

  section::before {
    content: "Ramboll";
    position: absolute;
    left: 38px;
    bottom: 16px;
    color: var(--ramboll-title-blue);
    font-family: "NunitoCustom", Nunito, Verdana, "Segoe UI", sans-serif;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0;
  }

  section::after {
    color: var(--ramboll-page-number);
    font-size: 13px;
    font-weight: 600;
    right: 34px;
    bottom: 16px;
  }

  h1,
  h2,
  h3,
  h4,
  p,
  li {
    font-family: "NunitoCustom", Nunito, Verdana, "Segoe UI", sans-serif;
  }

  h1 {
    color: var(--ramboll-title-blue);
    font-weight: 500;
    font-size: 2rem;
    line-height: 1.08;
    margin: 0 0 0.9rem 0;
    max-width: 11.5em;
  }

  h2 {
    color: var(--ramboll-text);
    font-weight: 700;
    font-size: 0.98rem;
    letter-spacing: 0.02em;
    margin: 0 0 0.45rem 0;
    text-transform: uppercase;
  }

  ul {
    margin-top: 0.35rem;
    max-width: 34em;
    padding-left: 1.15em;
  }

  li {
    line-height: 1.42;
    margin-bottom: 0.32rem;
  }

  p {
    line-height: 1.38;
    margin: 0 0 0.55rem 0;
    max-width: 42em;
  }

  strong {
    color: var(--ramboll-text);
  }

  section.lead {
    background: #ffffff;
    padding-top: 46px;
  }

  section.lead::before {
    content: "";
    position: absolute;
    left: 38px;
    bottom: 18px;
    width: 224px;
    height: 31px;
    background: url("assets/ramboll-logo.png") no-repeat left center / contain;
  }

  section.lead h1 {
    color: var(--ramboll-title-blue);
    font-size: 3.55rem;
    font-weight: 500;
    max-width: 10.5em;
    margin-top: 0;
    margin-bottom: 1.3rem;
  }

  section.lead p,
  section.lead li {
    color: var(--ramboll-text);
    font-size: 1.08rem;
    max-width: 48em;
  }

  section.lead ul {
    padding-left: 1.15em;
    list-style: disc;
    margin-top: 0.75rem;
  }

  section > *:first-child {
    margin-top: 0;
  }

  section.diagram h1 {
    font-size: 2rem;
    max-width: none;
    margin-bottom: 0.6rem;
  }

  section.diagram p {
    margin: 0.1rem 0 0.4rem;
  }

  section.diagram img {
    display: block;
    margin: 0.15rem auto 0;
    filter: none;
  }

  section.bullets h1,
  section.image-right h1,
  section.full-image h1 {
    max-width: none;
  }

  section.image-right .columns {
    display: grid;
    grid-template-columns: 1.03fr 0.97fr;
    gap: 36px;
    width: 100%;
    align-items: center;
    margin-top: 0.2rem;
  }

  section.image-right .copy-panel {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  section.image-right .media-panel {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  section.image-right .media-panel img {
    display: block;
    width: auto;
    max-width: 100%;
    max-height: 405px;
    border: none;
  }

  section.image-right .copy-panel ul {
    max-width: none;
  }

  section.full-image {
    min-height: 100%;
  }

  section.full-image .hero-image {
    width: 100%;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 0.3rem;
  }

  section.full-image img {
    display: block;
    width: auto;
    max-width: 100%;
    max-height: 420px;
    margin: 0 auto;
    border: none;
  }

  section.statement {
    background: var(--ramboll-ocean);
    color: white;
  }

  section.statement h1,
  section.statement h2,
  section.statement strong {
    color: white;
  }

  section.statement h2 {
    color: rgba(255, 255, 255, 0.85);
  }

  section.split {
    background:
      linear-gradient(90deg, transparent 0, transparent 49.6%, var(--ramboll-divider) 49.6%, var(--ramboll-divider) 49.85%, transparent 49.85%),
      #ffffff;
  }
---

<!-- _class: lead -->

# Example Deck With Split And Full Visuals

- This deck demonstrates the two main visual patterns in the Ramboll default
  deck
- Both graphics are produced from source in `visualisations/excalidraw/`

---
<!-- _class: image-right -->

# Split Layout With Diagram

<div class="columns">
<div class="copy-panel">

- Use the left column for the narrative or takeaway
- Use the right column for the rendered supporting diagram
- Keep the graphic sourced from `visualisations/`, not hand-drawn in the deck

</div>
<div class="media-panel">

![w:100%](../../visualisations/excalidraw/examples/rendered/standard_deck_split.png)

</div>
</div>

---
<!-- _class: full-image -->

# Full-Image Visual

<div class="hero-image">

![w:100%](../../visualisations/excalidraw/examples/rendered/standard_deck_full.png)

</div>
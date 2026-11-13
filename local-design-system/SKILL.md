# Design discipline for pages, artifacts and HTML/CSS output

Use this skill whenever the deliverable is visual: an HTML/CSS file, a web artifact, a landing page, a poster, a report or memo page, a dashboard mockup, or any page a person will look at. It governs taste and structure only — how the thing is delivered (artifact tool, file, export) is decided by the task itself.

Attribution: the rules below are adapted from BaoCut's built-in `design` and `design-system` skills, which were themselves ported from Anthropic's anthropic-design skill (see the source note in `references/brand-colors.md`). BaoCut-canvas mechanics (`.dc.html`, DCLogic, `canvas.json`, `design_check`, asset import tools) are deliberately dropped; everything here assumes you write plain HTML/CSS directly. In the copied references, read "board/artboard" as the page or file you are producing and `<helmet>` as `<head>`.

## Decide the direction before any layout

- Gather design context before inventing anything: the user's brand, an existing design system, the codebase or page this will live beside, screenshots or files they gave you. A high-fidelity design grows out of that context; mocking a whole product from zero is the last resort and produces poor work.

- When a brand or design system is specified, match it exactly — colors, type, spacing, radius, fonts — and let it override every default in this skill. When the user names a brand or product, ask for or fetch its real assets rather than designing blind.

- When nobody can answer and no system constrains you, pick one named, deliberate aesthetic direction (brutally minimal, maximalist, retro-future, editorial, brutalist, art deco, soft pastel, industrial, luxury, playful…) and state your assumptions in one line, then build. Never end with a question nobody can answer; never silently converge on the same look every time.

- If two or more decisions would change the outcome and someone can answer, ask once before building — at most 4 questions, each offering 2–4 concrete, genuinely different options (your recommendation first), never boilerplate requirements-gathering. Otherwise decide, say what you chose, and proceed.

## Define the token set before building

- Before writing layout, write down a small token set and use only those values. Put it in a `:root` CSS custom-properties block at the top of the file (or a tokens file the page loads) — every color, size and font the page uses traces back to it, one source per value:

```css
:root{
  --surface: #faf7f2;              /* the one tonal base */
  --ink: #211d19;
  --accent: oklch(0.62 0.14 45);   /* 0–2 accents, oklch */
  --font-display: "Space Grotesk", "Avenir Next", sans-serif;
  --font-body: "Source Sans 3", system-ui, sans-serif;
  --space-1: 4px; --space-2: 8px; --space-3: 16px; --space-4: 24px; --space-5: 40px;
  --radius-sm: 6px; --radius-md: 10px;
}
```

- Color: one tonal base (warm, cool or neutral). Whites and blacks carry a slight tint — a pure white's saturation stays under 0.02; never use pure `#FFF` as a full-page background. Accents: 0–2, expressed in `oklch` with the same chroma and lightness, differing only in hue. Prefer brand/system colors; if too constrained, derive harmonious oklch colors from them instead of inventing new hues.

- Type: 1–3 families — a distinctive display face paired with a refined body face. Every webfont gets a metric-matched system fallback, because the fallback is what renders while the font loads and wherever it cannot be embedded. Avoid generic defaults as first choice: no Inter, Roboto, Arial or Fraunces. Letter-spacing stays 0 unless a deliberate effect needs otherwise.

- Also fix a small type scale (display / title / heading / body / small / caption with size, weight, line-height), a spacing scale and a radius scale in the same token pass. Exact values from a real source are copied exactly — never rounded or snapped to a 4/8px grid.

## Anti-slop rules (hard)

- No big gradient washes or gradient backgrounds as decoration, no blue-purple gradients, no rounded cards with a colored left-border accent, no emoji as icons or UI glyphs (icons are inline stroke SVG or a real icon set; emoji appears only when it is genuinely part of the brand).

- No filler content: no lorem ipsum, no invented statistics, testimonials or "data slop" added to fill space. Every element earns its place; an empty-feeling section is a layout problem, not a content-invention prompt. Missing facts become visibly marked placeholders like `[YOUR PRICE]`.

- No fake chrome: never draw a fake phone status bar or keyboard inside a device mockup.

- Match the ambition of the execution to the direction: maximalist designs get rich effects; minimal designs get restraint and precision in spacing and detail. Dominant color with sharp accents beats timid, evenly spread color; asymmetry, overlap, generous whitespace or controlled density beat a default centered grid.

## Layout mechanics

- Lay out groups of siblings (buttons, chips, cards, nav items, toolbars) with flex or grid plus `gap` — never with whitespace text nodes or per-element margins between siblings. Inline flow is for prose with the occasional `<a>`/`<strong>` inside it, not for arranging UI elements.

- Pages are fluid: no px width on the root, a `max-width` container with side padding, `%`/`rem`/`fr` sizing, grids written as `repeat(auto-fit, minmax(min(<min>px, 100%), 1fr))` so they collapse to one column on a phone instead of overflowing. `vh` only for roots that truly fill the screen; sections followed by more content use px/rem `min-height`. Prefer slightly too tall over clipped.

- Fixed-size roots are only for fixed formats: device mockups, posters, social images, print pieces. Mobile app screens are 390×844; pages are designed to work at phone width — titles must not break awkwardly, grids must not crush, text must not shrink below readability.

- Diagrams in a deliverable page are ordinary inline SVG (in a `<figure>` is fine); keep labels and callouts as real text where someone may need to edit them.

## Accessibility is drawn in, not checked later

- Use real elements even in a static mockup: `<button>`, `<a href>`, `<input>` with a `<label>`. Never put `role` or `onClick` on a `div`/`span` as a substitute — keyboards skip it and screen readers get nothing. Icon-only buttons get `aria-label`; decorative SVG gets `aria-hidden="true"`, meaningful SVG gets `role="img"` and a label.

- Text contrast is at least 4.5:1 against what's behind it (3:1 for text 24px and up). The usual failures are gray caption text and colored fills under white text — darken both until they pass.

- Colors that must be distinguished must also differ in lightness, not only in hue; prefer blue/orange over red/green.

- Hit targets are at least 44px. Print body text is at least 12pt.

## Content and editing discipline

- Ask before adding material: if extra sections, pages or copy would improve the piece, ask first instead of adding them unasked.

- A small, targeted change changes only that spot: every other layout value, spacing, font, size, position, color and content stays exactly as it was. Do the requested change, then suggest anything bigger instead of doing it unasked. A request to redesign or start over is different — then do the big change.

- When extending an existing page or document, first read its visual vocabulary — copy style, palette, tone, hover states, shadow and card patterns, density — and write in it.

- When asked to reproduce an interface you can get source for, work from the real source: read the components and styles, copy the actual assets, copy exact values. Never reproduce from memory or from a screenshot when source exists. Do not reproduce another company's distinctive proprietary design for someone who doesn't work there; offer an original design aimed at their actual goal instead.

## Landing pages and print

- Landing pages: one hero that says in one sentence what is offered, with one clear call to action; proof a visitor can trust (testimonials, logos, numbers — theirs, or visibly marked placeholders); benefit sections that answer real objections rather than listing features. One primary action per page, repeated as the page descends. The copy is the product: specific, rooted in what the user actually sells, never interchangeable marketing boilerplate.

- Print pieces (posters, flyers, brochures, memos, reports, anything exported to PDF): read `references/print.md` before starting — decide fixed-page vs flowing document first, use real paper sizes (Letter 816×1056, A4 794×1123 CSS px), ≥40px safe margins, ≥1px rules, gray text no lighter than `#767676`, and flyer hierarchy readable across a room in three seconds.

## Anthropic-branded work

- For work carrying the Anthropic/Claude brand: base Ivory `#FAF9F5`, text Slate `#141413`, accent Clay `#D97757`, serif display type with sans body. The full warm-gray ramp, auxiliary palette and logo rules are in `references/brand-colors.md`; the font stacks and type scale are in `references/brand-typography.md`. The cream-base + serif-headline + terracotta habit is for Anthropic-branded work or when a brief calls for it — not a default for everything.

## References

- `references/craft.md` — the full reasoning behind these rules: choosing direction with the user, variations and wireframe rounds, landing-page structure, reproducing interfaces from source, and the shared content rules. Read it when a design decision is contested or a piece needs depth.

- `references/brand-colors.md` — Anthropic brand color system (warm grays, Claude palette, data-viz scales) and its source note.

- `references/brand-typography.md` — Anthropic brand font stacks with metric-matched fallbacks and the brand type scale.

- `references/print.md` — print craft: fixed vs flowing pages, paper sizes and units, margins, tables, flyer rules.

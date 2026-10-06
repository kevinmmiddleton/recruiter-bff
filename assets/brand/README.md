# Recruiter BFF brand files

A comically giant iced tea in chunky glasses, with no eyes. It's the friend who knows how
hiring works, reads the posting first, and gives you a straight answer. Sibling of Unpaid
Intern.

Version 3 (2026-10-06). Earlier versions are kept in `../_snapshots/` (v1, v2).

## Files

| File | Use |
|---|---|
| `svg/recruiter-bff-horizontal.svg` | The default logo: cup left, wordmark right. Transparent background |
| `svg/recruiter-bff-stacked.svg` | Cup above the wordmark, for square and tall spaces |
| `svg/recruiter-bff-mark.svg` | The cup alone |
| `svg/recruiter-bff-wordmark.svg` | "recruiter" on the Highlighter swipe above a big "bff" |
| `svg/recruiter-bff-wordmark-line.svg` | The name on one line, for small spaces like a site header |
| `svg/recruiter-bff-app-icon.svg` | 512 × 512 rounded square on Highlighter yellow. The cup is 90% of the tile's height and the straw runs off the top edge |
| `svg/recruiter-bff-mark-sticker-on-dark.svg` | The color cup with a paper edge, for dark backgrounds |
| `svg/recruiter-bff-favicon-mono-fallback.svg` | Fallback only: the one-color cup-top crop, for places that can't take color. Its solid lens cut-outs can read as eyes, so prefer the shipped favicon |
| `svg/*-black.svg`, `svg/*-white.svg` | One-color versions: the line drawing of the cup, with "recruiter" cut out of the swipe. Use white on dark backgrounds. Never on the yellow tile |
| `png/` | PNG exports of each logo (color and white), the app icon at 1024, the sticker, and the one-line wordmark |
| `favicon/` | `favicon.svg` (the color crop on the yellow tile, see below), `favicon.ico` (16, 32, 48), `apple-touch-icon.png`, 192 and 512 icons (the app icon, full bleed), a maskable 512 (the cup inside the safe circle), `site.webmanifest`, `head-snippet.html` |
| `brand-sheet.html`, `brand-sheet.png` | Every variant, clear space, small sizes, colors, favicon tabs, and app icons on one page |
| `banners/` | The logo and "A recruiter that works for you." in every size, each as SVG, PNG, and @2x PNG: `link-preview-1200x630` (LinkedIn link posts, Open Graph), `github-social-1280x640` (GitHub repo social preview), `wide-1600x900` (blog cover, X; everything sits inside a centered square, so square crops are safe), `square-1080x1080` (LinkedIn and Instagram feed), `portrait-1080x1350` (tall feed posts). Rebuild with `python3 tools/brand/build_banners.py` from the repo root |

Every file is filled paths only: no fonts, no strokes, no CSS. They open the same way everywhere.

## Favicon

The favicon is its own crop: the top of the cup only (lid, heart, glasses), upright, no
straw, in color on the yellow rounded tile, like Unpaid Intern's. The tile works on light
and dark tabs, so there's no dark-mode switch. Use the files in `favicon/` together, copied next to the page, with
`head-snippet.html` pasted into `<head>`. The paths are relative, so this works in a
subfolder too.

## Colors

| Name | Hex | Use |
|---|---|---|
| Ink | #16131F | Outlines, text, glasses (shared with the family) |
| Paper | #FFF8EF | Cup, straw, lenses, ice (shared) |
| Highlighter | #FFE14D | Wordmark swipe, app icon background (shared) |
| Mint | #5FD6A4 | The signature color: the lid and lens glints. Mint only, never a darker green |
| Iced Tea | #D98A2B | The tea, inside the mascot only |

## Minimum sizes

These are set so "recruiter" keeps an x-height of at least 6 pixels.

| Logo | Smallest height | Below that |
|---|---|---|
| Stacked lockup | 120 px | Use the horizontal lockup or the one-line wordmark |
| Horizontal lockup | 72 px | Use the one-line wordmark (18 px minimum), with the cup beside it if there's room |
| Cup alone | 48 px | Use the favicon crop |

## Rules

- **Clear space:** keep at least a quarter of the cup's height empty around the logo.
- **One-color versions drop the yellow tile.** A yellow square in one color is a solid block.
- **Never** add eyes, a mouth, arms, or a face. No dots or stubs next to the lenses (they read as pupils). No green straw (the straw is Paper), no darker green, no logo on the cup, no coffee-chain references. No Brain Pink, no Claude orange.
- **The ice:** two cubes and one heart, always (the favicon crop shows the heart alone).
- **Type:** the wordmark is Poppins Bold (SIL Open Font License), outlined, emboldened by 1% of its size, and rounded at the corners. For body text next to the logo, use Poppins or any clean geometric sans.

## Rebuilding

One command rebuilds the whole kit exactly:

```bash
cd ../build && ~/.cache/svg-logo-venv/bin/python kit.py
```

What it does:
1. `final.py` builds the art in `../final/`.
2. The `svg-logo` skill's `export.py` builds the kit. All of its settings are in `kit.py`.
3. `kit.py` adds the app icon, sticker, one-line wordmark, and the one-color favicon fallback.

Pass an output folder to build somewhere else, e.g. `kit.py /tmp/kit-test`. Every variant
explored on the way here is in `../VARIANTS.md`.

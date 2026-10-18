"""Build the Recruiter BFF banner set in assets/brand/banners/.

Matches Unpaid Intern's set: link-preview-1200x630, github-social-1280x640, wide-1600x900
(everything inside a centered square, so square crops are safe), square-1080x1080, and
portrait-1080x1350. Each is an SVG plus PNG and @2x PNG.

github-social-1280x640 (the README banner) uses the share arrangement Kevin picked on Oct 17,
the same one as the landing page's share image: the cup big on the left, the wordmark big on
the right, the tagline below. It sits closer to the edges than the kit's clear-space rule, on
purpose, so it skips that check. The other four keep the lockups and the clear space.

The logo art is used exactly as shipped in assets/brand/svg/ (never edited here). The tagline
is Poppins Bold, outlined to filled paths, so every SVG is paths only: no fonts, no CSS.

Run from the repo root:
    python3 tools/brand/build_banners.py            # SVG + PNG (PNG needs Playwright)
    python3 tools/brand/build_banners.py --svg-only
    python3 tools/brand/build_banners.py --tagline "Every recruiter says you'd be a great fit. This one checks."

Needs: fontTools, uharfbuzz; Playwright with Chromium for the PNGs.
"""
import argparse, glob, os, re, sys

import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SVG_DIR = os.path.join(ROOT, "assets", "brand", "svg")
OUT_DIR = os.path.join(ROOT, "assets", "brand", "banners")

INK, PAPER = "#16131F", "#FFF8EF"
TAGLINE = "A recruiter that works for you."
FONT_CANDIDATES = [
    os.path.expanduser("~/Library/Fonts/Poppins-Bold.ttf"),
    "/Library/Fonts/Poppins-Bold.ttf",
    "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
    *glob.glob("/usr/share/fonts/**/Poppins-Bold.ttf", recursive=True),
]

# Proportions follow Unpaid Intern's set. The block (logo, clear space, tagline) is centered
# in the frame. Clear space follows the kit rule: a quarter of the cup's height, both between
# the logo and the tagline and between the block and every edge. For wide-1600x900 the
# "edge" is the centered 900 x 900 square, so a square crop never cuts anything.
# In both lockups the cup is 100 units tall (the lockup viewBox height is 100 or 169.8).
CUP_UNITS = 100
# name, width, height, lockup, tagline lines, logo height, tagline size, frame (x0, y0, x1, y1)
BANNERS = [
    ("link-preview-1200x630",  1200,  630, "horizontal", 1, 320, 46, (0, 0, 1200, 630)),
    ("github-social-1280x640", 1280,  640, "share",      1, 0,   0,  (0, 0, 1280, 640)),
    ("wide-1600x900",          1600,  900, "horizontal", 2, 420, 60, (350, 0, 1250, 900)),
    ("square-1080x1080",       1080, 1080, "stacked",    2, 600, 64, (0, 0, 1080, 1080)),
    ("portrait-1080x1350",     1080, 1350, "stacked",    2, 760, 68, (0, 0, 1080, 1350)),
]


def find_font(path=None):
    for p in ([path] if path else []) + FONT_CANDIDATES:
        if p and os.path.exists(p):
            return p
    sys.exit("Poppins-Bold.ttf not found. Pass --font /path/to/Poppins-Bold.ttf")


def load_logo(kind):
    s = open(os.path.join(SVG_DIR, f"recruiter-bff-{kind}.svg")).read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    body = "\n".join(re.findall(r"<path[^>]*/>", s))
    return vb, body


class Tagline:
    def __init__(self, font_path):
        data = open(font_path, "rb").read()
        self.hb_font = hb.Font(hb.Face(data))
        self.tt = TTFont(font_path)
        self.upm = self.tt["head"].unitsPerEm
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()

    def line(self, text, size, x, baseline):
        """Return (svg path d, ink bounds) for one line, left edge at x."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb_font, buf, {"kern": True, "liga": True})
        k = size / self.upm
        pen = SVGPathPen(self.glyphs)
        bounds = BoundsPen(self.glyphs)
        cx = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            name = self.order[info.codepoint]
            t = (k, 0, 0, -k, x + (cx + pos.x_offset) * k, baseline - pos.y_offset * k)
            self.glyphs[name].draw(TransformPen(pen, t))
            self.glyphs[name].draw(TransformPen(bounds, t))
            cx += pos.x_advance
        return pen.getCommands(), bounds.bounds

    def measure(self, text, size):
        _, b = self.line(text, size, 0, 0)
        return b  # (xmin, ymin, xmax, ymax) relative to x=0, baseline=0


def split_two(text):
    words = text.split()
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = abs(len(a) - len(b))
        if best is None or score < best[0]:
            best = (score, a, b)
    return [best[1], best[2]]


def build(name, W, H, kind, n_lines, logo_h, size, frame, tag, text):
    (vx, vy, vw, vh), logo = load_logo(kind)
    clear = logo_h * CUP_UNITS / vh / 4          # kit rule: a quarter of the cup's height
    gap = clear
    x0, y0, x1, y1 = frame[0] + clear, frame[1] + clear, frame[2] - clear, frame[3] - clear
    sw = x1 - x0
    lines = [text] if n_lines == 1 else split_two(text)

    # Shrink the tagline if a long alternate line would overflow the safe width.
    while True:
        ink = [tag.measure(l, size) for l in lines]  # SVG coords: ymin is above the baseline
        if max(b[2] - b[0] for b in ink) <= sw or size <= 20:
            break
        size -= 1
    lead = size * 1.2
    top_ink = -ink[0][1]           # first line: tallest ink above its baseline
    bot_ink = ink[-1][3]           # last line: deepest descender below its baseline
    tag_h = top_ink + lead * (len(lines) - 1) + bot_ink

    logo_w = logo_h * vw / vh
    block_h = logo_h + gap + tag_h
    top = (H - block_h) / 2
    lx = (W - logo_w) / 2
    scale = logo_h / vh

    # Everything must keep its clear space from the frame edges.
    widest = max(b[2] - b[0] for b in ink)
    assert top >= y0 and top + block_h <= y1, f"{name}: block {block_h:.0f}px tall breaks clear space"
    assert lx >= x0 and lx + logo_w <= x1 and (W - widest) / 2 >= x0, f"{name}: too wide for clear space"

    parts = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>',
             f'<g transform="translate({lx:.2f} {top:.2f}) scale({scale:.4f}) translate({-vx:.2f} {-vy:.2f})">',
             logo, "</g>"]
    baseline = top + logo_h + gap + top_ink
    for l in lines:
        b = tag.measure(l, size)
        x = (W - (b[2] - b[0])) / 2 - b[0]
        d, _ = tag.line(l, size, x, baseline)
        parts.append(f'<path fill="{INK}" d="{d}"/>')
        baseline += lead

    label = f"Recruiter BFF: {text[0].lower() + text[1:]}" if text.startswith("A ") else f"Recruiter BFF. {text}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">\n'
           f"<title>{label}</title>\n" + "\n".join(parts) + "\n</svg>\n")
    path = os.path.join(OUT_DIR, f"{name}.svg")
    open(path, "w").write(svg)
    return path, logo_h


def build_share(name, W, H, tag, text):
    """The Oct 17 share arrangement, laid out in 1200 x 630 units (the landing page's share
    image) and scaled to the frame height: cup 430 tall at y 40, wordmark 330 tall at y 92,
    64 apart and centered together, tagline 44 px on a baseline at 548."""
    k = H / 630
    (mvx, mvy, mvw, mvh), mark = load_logo("mark")
    (wvx, wvy, wvw, wvh), word = load_logo("wordmark")
    ch, wh, gap = 430 * k, 330 * k, 64 * k
    cw, ww = ch * mvw / mvh, wh * wvw / wvh
    x0 = (W - (cw + gap + ww)) / 2
    parts = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>',
             f'<g transform="translate({x0:.2f} {40 * k:.2f}) scale({ch / mvh:.4f}) translate({-mvx:.2f} {-mvy:.2f})">', mark, "</g>",
             f'<g transform="translate({x0 + cw + gap:.2f} {92 * k:.2f}) scale({wh / wvh:.4f}) translate({-wvx:.2f} {-wvy:.2f})">', word, "</g>"]
    size = 44 * k
    b = tag.measure(text, size)
    d, _ = tag.line(text, size, (W - (b[2] - b[0])) / 2 - b[0], 548 * k)
    parts.append(f'<path fill="{INK}" d="{d}"/>')
    label = f"Recruiter BFF: {text[0].lower() + text[1:]}" if text.startswith("A ") else f"Recruiter BFF. {text}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">\n'
           f"<title>{label}</title>\n" + "\n".join(parts) + "\n</svg>\n")
    path = os.path.join(OUT_DIR, f"{name}.svg")
    open(path, "w").write(svg)
    return path, round(ch)


def rasterize(items):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        # PW_CHANNEL=chrome uses an installed Chrome when Playwright's own Chromium isn't there
        browser = p.chromium.launch(channel=os.environ.get("PW_CHANNEL") or None)
        for svg_path, W, H in items:
            sized = open(svg_path).read().replace("<svg ", '<svg width="%d" height="%d" ' % (W, H), 1)
            html = '<html><body style="margin:0">' + sized + "</body></html>"
            for scale, suffix in ((1, ""), (2, "@2x")):
                page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=scale)
                page.set_content(html)
                page.screenshot(path=svg_path[:-4] + suffix + ".png", clip={"x": 0, "y": 0, "width": W, "height": H})
                page.close()
        browser.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font")
    ap.add_argument("--tagline", default=TAGLINE)
    ap.add_argument("--svg-only", action="store_true")
    a = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)
    tag = Tagline(find_font(a.font))
    built = []
    for name, W, H, kind, n, logo_h, size, frame in BANNERS:
        if kind == "share":
            path, logo_h = build_share(name, W, H, tag, a.tagline)
        else:
            path, _ = build(name, W, H, kind, n, logo_h, size, frame, tag, a.tagline)
        print(f"{name}: {kind} {'arrangement, cup' if kind == 'share' else 'lockup'} {logo_h}px tall")
        built.append((path, W, H))
    if not a.svg_only:
        rasterize(built)


if __name__ == "__main__":
    main()

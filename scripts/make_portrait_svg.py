"""Generate portrait.svg: a colored ASCII portrait inside a terminal window.

Usage (from the repo root):
    python scripts/make_portrait_svg.py [--src photo.png] [--cols 92] [--out portrait.svg]

Only needs Pillow + numpy. Works on a photo with a plain light background
(the background is removed by flood-filling from the image borders).
"""
import argparse
import html

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

# Characters ordered from lightest to densest. On a dark terminal background,
# dense characters look bright, so bright pixels get dense characters.
RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

SVG_W, SVG_H = 370, 520
PAD_X = 15
ART_TOP = 36
ART_W = SVG_W - 2 * PAD_X
FOOTER_H = 58  # three prompt lines under the art
ART_H_MAX = SVG_H - ART_TOP - FOOTER_H - 6
CHAR_ASPECT = 0.6  # monospace glyph width / font-size
N_COLORS = 28


def foreground_mask(img: Image.Image) -> np.ndarray:
    """True where the subject is. Background = near-white region touching the top/sides."""
    a = np.asarray(img, dtype=np.int16)
    lo, hi = a.min(axis=2), a.max(axis=2)
    candidate = (lo > 222) & (hi - lo < 24)
    m = Image.new("L", img.size)
    m.putdata(np.where(candidate, 255, 0).astype(np.uint8).ravel().tolist())
    w, h = m.size
    seeds = [(x, 0) for x in range(0, w, 4)]
    seeds += [(0, y) for y in range(0, h, 4)] + [(w - 1, y) for y in range(0, h, 4)]
    for s in seeds:
        if m.getpixel(s) == 255:
            ImageDraw.floodfill(m, s, 128)
    bg = np.asarray(m) == 128
    # Smooth the edge a little so the outline is not jagged.
    fg = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7))
    return np.asarray(fg) > 127


def crop_to_subject(img, fg, keep_w=0.64, margin=0.02):
    """Crop from the top of the head and keep the central `keep_w` of the width, so the
    face fills more of the frame. The height is cut to fit the art area of the window."""
    ys, xs = np.nonzero(fg)
    h, w = fg.shape
    top = max(ys.min() - int(h * margin), 0)
    cx = (xs.min() + xs.max()) // 2
    half = int(w * keep_w) // 2
    left, right = max(cx - half, 0), min(cx + half, w)
    height = min(int((right - left) * ART_H_MAX / ART_W), h - top)
    box = (left, top, right, top + height)
    return img.crop(box), fg[box[1]:box[3], box[0]:box[2]]


def build_cells(src, cols):
    img = Image.open(src).convert("RGB")
    fg = foreground_mask(img)
    img, fg = crop_to_subject(img, fg)

    cell_w = ART_W / cols
    font_size = cell_w / CHAR_ASPECT
    line_h = font_size * 1.08
    rows = round(cols * (img.height / img.width) * (cell_w / line_h))

    # Tone: local-contrast boost + sharpening so glasses, eyes and beard read clearly.
    fg_img = Image.fromarray(fg.astype(np.uint8) * 255)
    gray = ImageOps.grayscale(img)
    gray = ImageOps.equalize(gray, mask=fg_img)  # spread the subject's tones
    gray = Image.blend(ImageOps.grayscale(img), gray, 0.55)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=8, percent=220, threshold=1))
    tone = np.asarray(gray.resize((cols, rows), Image.Resampling.LANCZOS), dtype=np.float32) / 255.0
    color = np.asarray(img.resize((cols, rows), Image.Resampling.BOX), dtype=np.float32) / 255.0
    cover = np.asarray(
        Image.fromarray(fg.astype(np.uint8) * 255).resize((cols, rows), Image.Resampling.BOX),
        dtype=np.float32) / 255.0
    inside = cover > 0.45

    # Stretch tones of the subject only, then a gentle gamma.
    lo, hi = np.percentile(tone[inside], [2, 99])
    t = np.clip((tone - lo) / (hi - lo), 0, 1) ** 0.85
    # Keep a faint texture in very dark areas (hair, suit) so the silhouette stays visible.
    t = 0.12 + 0.88 * t
    idx = np.clip((t * (len(RAMP) - 1)).round().astype(int), 1, len(RAMP) - 1)

    # Colors: lift dark ones so they stay readable on #0d1117, then quantize to a small palette.
    v = color.max(axis=2, keepdims=True)
    lifted = np.clip(color + (0.42 - v).clip(0) * 0.9 + 0.04, 0, 1)
    # Background cells are blank anyway: give them a subject color so they don't eat palette slots.
    lifted[~inside] = np.median(lifted[inside], axis=0)
    lifted_img = ImageEnhance.Color(Image.fromarray((lifted * 255).astype(np.uint8))).enhance(1.5)
    q = lifted_img.quantize(N_COLORS, method=Image.Quantize.MEDIANCUT)
    palette = np.array(q.getpalette()[: N_COLORS * 3]).reshape(-1, 3)
    labels = np.asarray(q)

    grid = []
    for y in range(rows):
        row = []
        for x in range(cols):
            if inside[y, x]:
                row.append((RAMP[idx[y, x]], int(labels[y, x])))
            else:
                row.append((" ", None))
        grid.append(row)
    return grid, palette, font_size, line_h, rows


def row_to_svg(row):
    """Merge consecutive characters of the same color into one <tspan>; spaces join any run."""
    out, cur_cls, buf = [], None, []

    def flush():
        if buf:
            # Non-breaking spaces: renderers never collapse them, so columns stay aligned.
            text = html.escape("".join(buf), quote=False).replace(" ", " ")
            out.append(f'<tspan class="c{cur_cls}">{text}</tspan>' if cur_cls is not None else text)

    for ch, cls in row:
        if ch == " " or cls == cur_cls:
            buf.append(ch)
            continue
        flush()
        buf, cur_cls = [ch], cls
    flush()
    return "".join(out)


def make_svg(grid, palette, font_size, line_h, rows):
    art_h = rows * line_h
    color_css = "\n".join(
        f"    .c{i}{{fill:#{r:02x}{g:02x}{b:02x}}}" for i, (r, g, b) in enumerate(palette))
    mono = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
    footer_y = SVG_H - FOOTER_H + 13

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}" width="{SVG_W}" height="{SVG_H}">',
        "  <style>",
        f"    .t{{font-family:{mono};}}",
        f"    .art{{font-family:{mono};font-size:{font_size:.2f}px;white-space:pre;}}",
        "    .muted{fill:#8b949e;font-size:11px}",
        "    .user{fill:#58a6ff;font-weight:bold;font-size:11px}",
        "    .cmd{fill:#c9d1d9;font-size:11px}",
        "    .out{fill:#7ee787;font-size:11px}",
        "    .cursor{fill:#c9d1d9;animation:blink 1s steps(1) infinite}",
        "    @keyframes blink{50%{opacity:0}}",
        color_css,
        "  </style>",
        "  <defs>",
        '    <clipPath id="reveal">',
        f'      <rect x="0" y="{ART_TOP}" width="{SVG_W}" height="0">',
        f'        <animate attributeName="height" from="0" to="{art_h + 4:.1f}" begin="0.3s" dur="2.4s" fill="freeze"/>',
        "      </rect>",
        "    </clipPath>",
        "  </defs>",
        f'  <rect x="0.5" y="0.5" width="{SVG_W - 1}" height="{SVG_H - 1}" rx="10" fill="#0d1117" stroke="#30363d"/>',
        '  <circle cx="15" cy="14" r="4.5" fill="#ff5f56"/>',
        '  <circle cx="28" cy="14" r="4.5" fill="#ffbd2e"/>',
        '  <circle cx="41" cy="14" r="4.5" fill="#27c93f"/>',
        f'  <text x="{SVG_W // 2}" y="18" text-anchor="middle" class="t muted">echlouchi@github:~$ ./portrait.sh</text>',
        f'  <g class="art" clip-path="url(#reveal)" xml:space="preserve">',
    ]
    for i, row in enumerate(grid):
        y = ART_TOP + (i + 1) * line_h - line_h * 0.22
        parts.append(
            f'    <text x="{PAD_X}" y="{y:.2f}" textLength="{ART_W}" lengthAdjust="spacing">{row_to_svg(row)}</text>')
    parts += [
        "  </g>",
        f'  <text x="{PAD_X}" y="{footer_y}" class="t"><tspan class="user">echlouchi@github:~$</tspan><tspan class="cmd"> whoami</tspan></text>',
        f'  <text x="{PAD_X}" y="{footer_y + 17}" class="t out">Ali Echlouchi · AI &amp; Full-Stack Engineer</text>',
        f'  <text x="{PAD_X}" y="{footer_y + 34}" class="t"><tspan class="user">echlouchi@github:~$</tspan><tspan class="cursor"> █</tspan></text>',
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="photo/portrait-professionnel (1).png")
    ap.add_argument("--cols", type=int, default=92)
    ap.add_argument("--out", default="portrait.svg")
    ap.add_argument("--txt", help="also write the plain ASCII art to this file")
    a = ap.parse_args()

    grid, palette, font_size, line_h, rows = build_cells(a.src, a.cols)
    art_bottom = ART_TOP + rows * line_h
    if art_bottom > SVG_H - FOOTER_H:
        raise SystemExit(f"art too tall ({art_bottom:.0f}px); lower --cols")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(make_svg(grid, palette, font_size, line_h, rows))
    if a.txt:
        with open(a.txt, "w", encoding="utf-8") as f:
            f.write("\n".join("".join(c for c, _ in r).rstrip() for r in grid) + "\n")
    print(f"{a.out}: {a.cols}x{rows} chars, font {font_size:.2f}px")


if __name__ == "__main__":
    main()

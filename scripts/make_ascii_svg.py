import os
import cv2
import numpy as np

# Character density ramp (light/bright to dark/dense)
RAMP = " .`:-=+*cs#%@"

def image_to_ascii(img_path, width=95):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not read image from {img_path}")
        
    h, w = img.shape
    aspect_ratio = h / w
    # Monospace characters are roughly 2x taller than wide (aspect ~ 0.55)
    height = int(width * aspect_ratio * 0.52)
    
    resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    
    # Map pixel values (0-255) to RAMP indices (0 to len(RAMP)-1)
    # Note: 255 is bright (space), 0 is dark (@)
    ramp_len = len(RAMP)
    lines = []
    for y in range(height):
        row_str = ""
        for x in range(width):
            val = resized[y, x]
            idx = int((255 - val) / 255 * (ramp_len - 1))
            row_str += RAMP[idx]
        lines.append(row_str)
        
    return lines, width, height

def generate_ascii_svg(lines, width, height, output_path="avi-ascii.svg"):
    char_w = 7.2
    char_h = 13.0
    padding_x = 20
    padding_y = 25
    
    svg_w = int(width * char_w + padding_x * 2)
    svg_h = int(height * char_h + padding_y * 2)
    
    total_rows = len(lines)
    row_delay = 0.04  # seconds per row
    anim_duration = 0.12 # seconds wipe per row
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg.append('    .ascii-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 11px; fill: #58a6ff; white-space: pre; }')
    svg.append('    .border { stroke: #30363d; stroke-width: 1; fill: none; rx: 10px; ry: 10px; }')
    svg.append('    .header-dot { rx: 50%; ry: 50%; }')
    svg.append('  </style>')
    
    # Container background
    svg.append(f'  <rect width="{svg_w}" height="{svg_h}" class="bg" />')
    svg.append(f'  <rect width="{svg_w}" height="{svg_h}" class="border" />')
    
    # Header dots (Mac/Terminal style)
    svg.append('  <circle cx="15" cy="12" r="4.5" fill="#ff5f56" />')
    svg.append('  <circle cx="28" cy="12" r="4.5" fill="#ffbd2e" />')
    svg.append('  <circle cx="41" cy="12" r="4.5" fill="#27c93f" />')
    svg.append(f'  <text x="{svg_w // 2}" y="15" fill="#8b949e" font-size="10" font-family="monospace" text-anchor="middle">echlouchi@portrait ~ ascii</text>')
    
    # Clip paths and rows
    svg.append('  <defs>')
    for i in range(total_rows):
        start_t = i * row_delay
        clip_y = padding_y + i * char_h - 2
        svg.append(f'    <clipPath id="cp_{i}">')
        svg.append(f'      <rect x="{padding_x}" y="{clip_y}" width="0" height="{char_h + 4}">')
        svg.append(f'        <animate attributeName="width" from="0" to="{svg_w - padding_x * 2}" begin="{start_t:.2f}s" dur="{anim_duration:.2f}s" fill="freeze" />')
        svg.append('      </rect>')
        svg.append('    </clipPath>')
    svg.append('  </defs>')
    
    svg.append(f'  <g class="ascii-text">')
    for i, line in enumerate(lines):
        y_pos = padding_y + (i + 1) * char_h - 3
        # Escape HTML entities
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        svg.append(f'    <text x="{padding_x}" y="{y_pos:.1f}" clip-path="url(#cp_{i})">{escaped_line}</text>')
    svg.append('  </g>')
    
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"ASCII SVG saved to {output_path}")

if __name__ == "__main__":
    prepped_img = os.path.join("data", "source-prepped.png")
    lines, w, h = image_to_ascii(prepped_img, width=88)
    generate_ascii_svg(lines, w, h, "avi-ascii.svg")

import os
import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@"

def process_portrait_to_ascii(prepped_path, char_width=68):
    img = cv2.imread(prepped_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load {prepped_path}")
        
    h, w = img.shape
    aspect_ratio = h / w
    # Monospace aspect ~ 0.52
    char_height = int(char_width * aspect_ratio * 0.52)
    
    resized = cv2.resize(img, (char_width, char_height), interpolation=cv2.INTER_AREA)
    
    lines = []
    ramp_len = len(RAMP)
    
    for y in range(char_height):
        row_str = ""
        for x in range(char_width):
            val = resized[y, x]
            if val >= 245:
                row_str += " "
            else:
                norm = (244 - val) / 244.0
                idx = int(norm * (ramp_len - 1))
                idx = max(0, min(ramp_len - 1, idx))
                row_str += RAMP[idx]
        lines.append(row_str)
        
    return lines, char_width, char_height

def generate_exact_ascii_svg(lines, width, height, output_path="avi-ascii-v2.svg"):
    char_w = 5.0
    char_h = 8.5
    padding_x = 15
    padding_y = 35
    
    svg_w = 370
    svg_h = 520
    
    total_rows = len(lines)
    row_delay = 0.025
    anim_duration = 0.10
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg.append('    .border { stroke: #30363d; stroke-width: 1; fill: none; rx: 10px; ry: 10px; }')
    svg.append('    .title-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('    .ascii-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 8.5px; fill: #c9d1d9; white-space: pre; }')
    svg.append('    .prompt-user { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; font-weight: bold; fill: #58a6ff; }')
    svg.append('    .prompt-path { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #79c0ff; }')
    svg.append('    .prompt-cmd { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #c9d1d9; }')
    svg.append('  </style>')
    
    # Container background & border
    svg.append(f'  <rect width="{svg_w}" height="{svg_h}" class="bg" />')
    svg.append(f'  <rect width="{svg_w}" height="{svg_h}" class="border" />')
    
    # Header buttons (Mac style)
    svg.append('  <circle cx="15" cy="14" r="4.5" fill="#ff5f56" />')
    svg.append('  <circle cx="28" cy="14" r="4.5" fill="#ffbd2e" />')
    svg.append('  <circle cx="41" cy="14" r="4.5" fill="#27c93f" />')
    svg.append(f'  <text x="{svg_w // 2}" y="17" class="title-text" text-anchor="middle">echlouchi@github:~$ ./portrait.sh</text>')
    
    # Clip paths for animated wipe
    svg.append('  <defs>')
    for i in range(total_rows):
        start_t = i * row_delay
        clip_y = padding_y + i * char_h - 1
        svg.append(f'    <clipPath id="cp_{i}">')
        svg.append(f'      <rect x="{padding_x}" y="{clip_y}" width="0" height="{char_h + 2}">')
        svg.append(f'        <animate attributeName="width" from="0" to="{svg_w - padding_x * 2}" begin="{start_t:.2f}s" dur="{anim_duration:.2f}s" fill="freeze" />')
        svg.append('      </rect>')
        svg.append('    </clipPath>')
    svg.append('  </defs>')
    
    # ASCII text content
    svg.append(f'  <g class="ascii-text">')
    for i, line in enumerate(lines):
        y_pos = padding_y + (i + 1) * char_h - 2
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        svg.append(f'    <text x="{padding_x}" y="{y_pos:.1f}" clip-path="url(#cp_{i})">{escaped_line}</text>')
    svg.append('  </g>')
    
    # Footer prompt line inside window: "echlouchi@github:~$ whoami Ali Echlouchi"
    footer_y = svg_h - 18
    svg.append(f'  <text x="{padding_x}" y="{footer_y}">')
    svg.append(f'    <tspan class="prompt-user">echlouchi@github:~$ </tspan>')
    svg.append(f'    <tspan class="prompt-cmd">whoami </tspan>')
    svg.append(f'    <tspan class="prompt-path">Ali Echlouchi</tspan>')
    svg.append(f'  </text>')
    
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    # Also write to avi-ascii.svg
    with open("avi-ascii.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Blog-Style ASCII Portrait SVG saved to {output_path} and avi-ascii.svg")

if __name__ == "__main__":
    prepped = os.path.join("data", "source-prepped.png")
    lines, w, h = process_portrait_to_ascii(prepped, char_width=68)
    generate_exact_ascii_svg(lines, w, h, "avi-ascii-v2.svg")

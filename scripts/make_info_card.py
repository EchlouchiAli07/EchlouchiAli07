import os

def generate_info_card(output_path="info-card.svg"):
    width = 540
    height = 370
    padding_x = 24
    padding_y = 20
    
    # Custom color palette for terminal card
    bg_color = "#0d1117"
    border_color = "#30363d"
    key_color = "#79c0ff"      # Soft blue
    val_color = "#c9d1d9"      # Bright text
    highlight_color = "#7ee787"# Soft green
    accent_color = "#d2a8ff"   # Soft purple
    sub_color = "#8b949e"      # Muted gray
    
    rows = [
        ("OS", "Master IS2IA @ ESISA Fès (2025 - 2027)", key_color),
        ("Role", "AI & Full-Stack Engineer Student", highlight_color),
        ("Status", "Looking for PFE Internship (Feb 2027)", accent_color),
        ("AI / ML", "ML (scikit-learn), NLP (CamemBERT), LLM (Gemini, OpenRouter)", val_color),
        ("Full-Stack", "Next.js 15/16, NestJS 11, FastAPI, React 19, TypeScript", val_color),
        ("Databases", "PostgreSQL, Supabase, TypeORM, MongoDB", val_color),
        ("Experience", "CHU Hassan II (Triage IA), Business Partners (ERP COD)", sub_color),
        ("Projects", "EnergyAI SaaS, Interactive Chatbot PFA, Transport Analytics", sub_color),
        ("Certs", "Cisco Ethical Hacker, IBM Data Analysis, Intro to IoT", sub_color),
        ("Languages", "French (TCF B2), English (Inter.), Arabic (Native)", sub_color),
    ]
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .card-bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg.append('    .card-border { stroke: #30363d; stroke-width: 1; fill: none; rx: 10px; ry: 10px; }')
    svg.append('    .term-title { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('    .user-header { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 14px; font-weight: bold; fill: #58a6ff; }')
    svg.append('    .separator { stroke: #30363d; stroke-width: 1; }')
    svg.append('    .row-key { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11.5px; font-weight: bold; }')
    svg.append('    .row-val { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11.5px; fill: #c9d1d9; }')
    svg.append('    .color-block { rx: 3px; ry: 3px; }')
    
    # CSS animations for staggered line entry
    svg.append('    @keyframes fadeIn {')
    svg.append('      from { opacity: 0; transform: translateY(6px); }')
    svg.append('      to { opacity: 1; transform: translateY(0); }')
    svg.append('    }')
    svg.append('    .anim-row { opacity: 0; animation: fadeIn 0.4s ease-out forwards; }')
    svg.append('  </style>')
    
    # Background & border
    svg.append(f'  <rect width="{width}" height="{height}" class="card-bg" />')
    svg.append(f'  <rect width="{width}" height="{height}" class="card-border" />')
    
    # Header buttons
    svg.append('  <circle cx="15" cy="14" r="4.5" fill="#ff5f56" />')
    svg.append('  <circle cx="28" cy="14" r="4.5" fill="#ffbd2e" />')
    svg.append('  <circle cx="41" cy="14" r="4.5" fill="#27c93f" />')
    svg.append(f'  <text x="{width // 2}" y="17" class="term-title" text-anchor="middle">echlouchi@portfolio ~ neofetch</text>')
    
    # User header line
    svg.append('  <g class="anim-row" style="animation-delay: 0.1s;">')
    svg.append(f'    <text x="{padding_x}" y="48" class="user-header">Ali Echlouchi</text>')
    svg.append(f'    <text x="{padding_x + 105}" y="48" font-family="monospace" font-size="14" fill="#8b949e">@</text>')
    svg.append(f'    <text x="{padding_x + 120}" y="48" font-family="monospace" font-size="14" fill="#79c0ff">EchlouchiAli07</text>')
    svg.append(f'    <line x1="{padding_x}" y1="58" x2="{width - padding_x}" y2="58" class="separator" />')
    svg.append('  </g>')
    
    # Staggered rows
    start_y = 80
    row_height = 24
    
    for i, (key, val, k_color) in enumerate(rows):
        y = start_y + i * row_height
        delay = 0.2 + i * 0.08
        svg.append(f'  <g class="anim-row" style="animation-delay: {delay:.2f}s;">')
        svg.append(f'    <text x="{padding_x}" y="{y}" class="row-key" fill="{k_color}">{key}:</text>')
        # Calculate padding for aligned values
        val_x = padding_x + 95
        escaped_val = val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg.append(f'    <text x="{val_x}" y="{y}" class="row-val">{escaped_val}</text>')
        svg.append('  </g>')
        
    # Neofetch color palette blocks at bottom
    palette_y = start_y + len(rows) * row_height + 10
    colors_dark = ["#484f58", "#ff7b72", "#7ee787", "#ffa657", "#79c0ff", "#d2a8ff", "#a5d6ff"]
    colors_bright = ["#6e7681", "#ffa198", "#56d364", "#e3b341", "#58a6ff", "#bc8cff", "#39c5cf"]
    
    delay_blocks = 0.2 + len(rows) * 0.08 + 0.1
    svg.append(f'  <g class="anim-row" style="animation-delay: {delay_blocks:.2f}s;">')
    svg.append(f'    <line x1="{padding_x}" y1="{palette_y - 10}" x2="{width - padding_x}" y2="{palette_y - 10}" class="separator" />')
    
    block_w = 26
    block_h = 10
    for idx, c in enumerate(colors_dark):
        bx = padding_x + idx * (block_w + 4)
        svg.append(f'    <rect x="{bx}" y="{palette_y}" width="{block_w}" height="{block_h}" fill="{c}" class="color-block" />')
    for idx, c in enumerate(colors_bright):
        bx = padding_x + idx * (block_w + 4)
        svg.append(f'    <rect x="{bx}" y="{palette_y + 14}" width="{block_w}" height="{block_h}" fill="{c}" class="color-block" />')
        
    svg.append('  </g>')
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Info Card SVG saved to {output_path}")

if __name__ == "__main__":
    generate_info_card("info-card.svg")

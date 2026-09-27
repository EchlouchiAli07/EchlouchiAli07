import os
import base64

def generate_avatar_svg(photo_path, output_path="avi-ascii.svg"):
    if not os.path.exists(photo_path):
        raise FileNotFoundError(f"Photo not found at {photo_path}")
        
    with open(photo_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")
        
    width = 370
    height = 370
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg.append('    .border { stroke: #30363d; stroke-width: 1; fill: none; rx: 10px; ry: 10px; }')
    svg.append('    .title-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('    .avatar-ring { stroke: #58a6ff; stroke-width: 2.5; fill: none; }')
    svg.append('    .avatar-glow { stroke: #58a6ff; stroke-width: 6; opacity: 0.3; fill: none; filter: blur(4px); }')
    svg.append('    .status-badge { fill: #238636; rx: 12px; ry: 12px; }')
    svg.append('    .status-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #ffffff; font-weight: bold; }')
    svg.append('    .role-title { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; fill: #58a6ff; font-weight: bold; }')
    svg.append('    .role-sub { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('    @keyframes pulse { 0% { opacity: 0.3; } 50% { opacity: 0.7; } 100% { opacity: 0.3; } }')
    svg.append('    .pulse-ring { animation: pulse 2.5s infinite ease-in-out; }')
    svg.append('  </style>')
    
    svg.append('  <defs>')
    svg.append('    <clipPath id="avatar-clip">')
    svg.append('      <circle cx="185" cy="165" r="95" />')
    svg.append('    </clipPath>')
    svg.append('  </defs>')
    
    # Background & border
    svg.append(f'  <rect width="{width}" height="{height}" class="bg" />')
    svg.append(f'  <rect width="{width}" height="{height}" class="border" />')
    
    # Terminal header
    svg.append('  <circle cx="15" cy="14" r="4.5" fill="#ff5f56" />')
    svg.append('  <circle cx="28" cy="14" r="4.5" fill="#ffbd2e" />')
    svg.append('  <circle cx="41" cy="14" r="4.5" fill="#27c93f" />')
    svg.append(f'  <text x="{width // 2}" y="17" class="title-text" text-anchor="middle">echlouchi@portrait ~ hd</text>')
    
    # Outer glowing ring
    svg.append('  <circle cx="185" cy="165" r="98" class="avatar-glow pulse-ring" />')
    svg.append('  <circle cx="185" cy="165" r="95" class="avatar-ring" />')
    
    # Photo image inside circle
    svg.append(f'  <image href="data:image/png;base64,{img_data}" x="85" y="65" width="200" height="200" preserveAspectRatio="xMidYMid slice" clip-path="url(#avatar-clip)" />')
    
    # Online status dot on avatar
    svg.append('  <circle cx="250" cy="230" r="12" fill="#0d1117" />')
    svg.append('  <circle cx="250" cy="230" r="9" fill="#3fb950" />')
    
    # Text underneath
    svg.append('  <text x="185" y="295" class="role-title" text-anchor="middle">Ali Echlouchi</text>')
    svg.append('  <text x="185" y="318" class="role-sub" text-anchor="middle">AI &amp; Full-Stack Engineer Student</text>')
    
    # Status pill
    svg.append('  <rect x="95" y="332" width="180" height="24" class="status-badge" />')
    svg.append('  <text x="185" y="348" class="status-text" text-anchor="middle">Available for PFE 2027</text>')
    
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"HD Avatar SVG saved to {output_path}")

if __name__ == "__main__":
    generate_avatar_svg("photo/portrait-professionnel (1).png", "avi-ascii.svg")

import os
import base64

def generate_animated_avatar_svg(photo_path, output_path="avi-ascii.svg"):
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
    svg.append('    .avatar-glow { stroke: #58a6ff; stroke-width: 8; opacity: 0.25; fill: none; }')
    svg.append('    .status-badge { fill: #238636; rx: 12px; ry: 12px; }')
    svg.append('    .status-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #ffffff; font-weight: bold; }')
    svg.append('    .role-title { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 14px; fill: #58a6ff; font-weight: bold; }')
    svg.append('    .role-sub { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    
    # Keyframe animations for futuristic scanner wipe & entrance
    svg.append('    @keyframes scanlineWipe {')
    svg.append('      0% { height: 0px; }')
    svg.append('      100% { height: 210px; }')
    svg.append('    }')
    svg.append('    @keyframes laserMove {')
    svg.append('      0% { y: 60px; opacity: 1; }')
    svg.append('      95% { opacity: 1; }')
    svg.append('      100% { y: 270px; opacity: 0; }')
    svg.append('    }')
    svg.append('    @keyframes fadeIn {')
    svg.append('      from { opacity: 0; transform: translateY(8px); }')
    svg.append('      to { opacity: 1; transform: translateY(0); }')
    svg.append('    }')
    svg.append('    .scan-wipe { animation: scanlineWipe 1.4s ease-in-out forwards; }')
    svg.append('    .laser-line { stroke: #58a6ff; stroke-width: 2; opacity: 0; animation: laserMove 1.4s ease-in-out forwards; }')
    svg.append('    .anim-text-1 { opacity: 0; animation: fadeIn 0.4s ease-out 1.2s forwards; }')
    svg.append('    .anim-text-2 { opacity: 0; animation: fadeIn 0.4s ease-out 1.5s forwards; }')
    svg.append('    .anim-text-3 { opacity: 0; animation: fadeIn 0.4s ease-out 1.8s forwards; }')
    svg.append('  </style>')
    
    svg.append('  <defs>')
    # Wipe clip path for scanning effect on portrait
    svg.append('    <clipPath id="scan-clip">')
    svg.append('      <rect x="80" y="60" width="210" class="scan-wipe" />')
    svg.append('    </clipPath>')
    svg.append('    <clipPath id="avatar-circle">')
    svg.append('      <circle cx="185" cy="165" r="92" />')
    svg.append('    </clipPath>')
    svg.append('  </defs>')
    
    # Background & border
    svg.append(f'  <rect width="{width}" height="{height}" class="bg" />')
    svg.append(f'  <rect width="{width}" height="{height}" class="border" />')
    
    # Header buttons
    svg.append('  <circle cx="15" cy="14" r="4.5" fill="#ff5f56" />')
    svg.append('  <circle cx="28" cy="14" r="4.5" fill="#ffbd2e" />')
    svg.append('  <circle cx="41" cy="14" r="4.5" fill="#27c93f" />')
    svg.append(f'  <text x="{width // 2}" y="17" class="title-text" text-anchor="middle">echlouchi@portrait ~ animated</text>')
    
    # Outer glowing ring
    svg.append('  <circle cx="185" cy="165" r="95" class="avatar-glow" />')
    svg.append('  <circle cx="185" cy="165" r="92" class="avatar-ring" />')
    
    # Animated scanning reveal of user's photo
    svg.append('  <g clip-path="url(#avatar-circle)">')
    svg.append(f'    <image href="data:image/png;base64,{img_data}" x="85" y="65" width="200" height="200" preserveAspectRatio="xMidYMid slice" clip-path="url(#scan-clip)" />')
    svg.append('  </g>')
    
    # Scanning laser line effect
    svg.append('  <line x1="80" y1="60" x2="290" y2="60" class="laser-line" />')
    
    # Online indicator
    svg.append('  <g class="anim-text-1">')
    svg.append('    <circle cx="248" cy="228" r="11" fill="#0d1117" />')
    svg.append('    <circle cx="248" cy="228" r="8" fill="#3fb950" />')
    svg.append('  </g>')
    
    # Animated Bio text
    svg.append('  <g class="anim-text-1">')
    svg.append('    <text x="185" y="295" class="role-title" text-anchor="middle">Ali Echlouchi</text>')
    svg.append('  </g>')
    
    svg.append('  <g class="anim-text-2">')
    svg.append('    <text x="185" y="318" class="role-sub" text-anchor="middle">AI &amp; Full-Stack Engineer Student</text>')
    svg.append('  </g>')
    
    # Animated status badge
    svg.append('  <g class="anim-text-3">')
    svg.append('    <rect x="95" y="332" width="180" height="24" class="status-badge" />')
    svg.append('    <text x="185" y="348" class="status-text" text-anchor="middle">Available for PFE 2027</text>')
    svg.append('  </g>')
    
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Animated Avatar SVG saved to {output_path}")

if __name__ == "__main__":
    generate_animated_avatar_svg("photo/portrait-professionnel (1).png", "avi-ascii.svg")

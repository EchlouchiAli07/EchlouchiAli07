import os
import base64
import cv2
import numpy as np

def generate_animated_avatar_svg(photo_path, output_path="avi-ascii.svg"):
    if not os.path.exists(photo_path):
        raise FileNotFoundError(f"Photo not found at {photo_path}")
        
    # Read image using OpenCV
    img = cv2.imread(photo_path)
    if img is None:
        raise ValueError(f"Could not load image {photo_path}")
        
    # Crop to head & upper chest
    h, w, _ = img.shape
    crop_top = int(h * 0.02)
    crop_bottom = int(h * 0.82)
    crop_left = int(w * 0.10)
    crop_right = int(w * 0.90)
    cropped = img[crop_top:crop_bottom, crop_left:crop_right]
    
    # Replace white background (RGB > 215, 215, 215) with dark terminal background #0d1117 (BGR: 23, 17, 13)
    bg_mask = (cropped[:, :, 0] > 200) & (cropped[:, :, 1] > 200) & (cropped[:, :, 2] > 200)
    
    # Soft edge blending for natural hair cut-out
    cropped_bg = cropped.copy()
    cropped_bg[bg_mask] = [23, 17, 13]  # #0d1117 in BGR
    
    # Save temporary processed png
    temp_path = os.path.join("data", "avatar-darkbg.png")
    os.makedirs("data", exist_ok=True)
    cv2.imwrite(temp_path, cropped_bg)
    
    with open(temp_path, "rb") as f:
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
    svg.append('    .avatar-glow { stroke: #58a6ff; stroke-width: 6; opacity: 0.35; fill: none; }')
    svg.append('    .status-badge { fill: #238636; rx: 12px; ry: 12px; }')
    svg.append('    .status-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #ffffff; font-weight: bold; }')
    svg.append('    .role-title { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 14px; fill: #58a6ff; font-weight: bold; }')
    svg.append('    .role-sub { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    
    # Keyframe animations
    svg.append('    @keyframes scanlineWipe {')
    svg.append('      0% { height: 0px; }')
    svg.append('      100% { height: 210px; }')
    svg.append('    }')
    svg.append('    @keyframes laserMove {')
    svg.append('      0% { y: 55px; opacity: 1; }')
    svg.append('      95% { opacity: 1; }')
    svg.append('      100% { y: 265px; opacity: 0; }')
    svg.append('    }')
    svg.append('    @keyframes fadeIn {')
    svg.append('      from { opacity: 0; transform: translateY(6px); }')
    svg.append('      to { opacity: 1; transform: translateY(0); }')
    svg.append('    }')
    svg.append('    .scan-wipe { animation: scanlineWipe 1.3s ease-in-out forwards; }')
    svg.append('    .laser-line { stroke: #58a6ff; stroke-width: 2; opacity: 0; animation: laserMove 1.3s ease-in-out forwards; }')
    svg.append('    .anim-text-1 { opacity: 0; animation: fadeIn 0.4s ease-out 1.1s forwards; }')
    svg.append('    .anim-text-2 { opacity: 0; animation: fadeIn 0.4s ease-out 1.4s forwards; }')
    svg.append('    .anim-text-3 { opacity: 0; animation: fadeIn 0.4s ease-out 1.7s forwards; }')
    svg.append('  </style>')
    
    svg.append('  <defs>')
    svg.append('    <clipPath id="scan-clip">')
    svg.append('      <rect x="80" y="55" width="210" class="scan-wipe" />')
    svg.append('    </clipPath>')
    svg.append('    <clipPath id="avatar-circle">')
    svg.append('      <circle cx="185" cy="160" r="92" />')
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
    svg.append('  <circle cx="185" cy="160" r="95" class="avatar-glow" />')
    svg.append('  <circle cx="185" cy="160" r="92" class="avatar-ring" />')
    
    # Animated scanning reveal of user's photo with dark background
    svg.append('  <g clip-path="url(#avatar-circle)">')
    svg.append(f'    <image href="data:image/png;base64,{img_data}" x="85" y="60" width="200" height="200" preserveAspectRatio="xMidYMid slice" clip-path="url(#scan-clip)" />')
    svg.append('  </g>')
    
    # Laser line
    svg.append('  <line x1="80" y1="55" x2="290" y2="55" class="laser-line" />')
    
    # Online indicator
    svg.append('  <g class="anim-text-1">')
    svg.append('    <circle cx="248" cy="223" r="11" fill="#0d1117" />')
    svg.append('    <circle cx="248" cy="223" r="8" fill="#3fb950" />')
    svg.append('  </g>')
    
    # Animated Bio text
    svg.append('  <g class="anim-text-1">')
    svg.append('    <text x="185" y="285" class="role-title" text-anchor="middle">Ali Echlouchi</text>')
    svg.append('  </g>')
    
    svg.append('  <g class="anim-text-2">')
    svg.append('    <text x="185" y="308" class="role-sub" text-anchor="middle">AI &amp; Full-Stack Engineer Student</text>')
    svg.append('  </g>')
    
    # Animated status badge
    svg.append('  <g class="anim-text-3">')
    svg.append('    <rect x="95" y="325" width="180" height="24" class="status-badge" />')
    svg.append('    <text x="185" y="341" class="status-text" text-anchor="middle">Available for PFE 2027</text>')
    svg.append('  </g>')
    
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Dark BG Animated Avatar SVG saved to {output_path}")

if __name__ == "__main__":
    generate_animated_avatar_svg("photo/portrait-professionnel (1).png", "avi-ascii.svg")

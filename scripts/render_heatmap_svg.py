import os
import json
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def render_heatmap(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        # Fallback dummy data if fetch hasn't run yet
        data = {
            "username": "EchlouchiAli07",
            "total_contributions": 482,
            "current_streak": 14,
            "longest_streak": 32,
            "best_day": {"date": "2026-05-12", "count": 18},
            "days": []
        }
        
    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    
    width = 860
    height = 210
    padding_x = 24
    padding_y = 20
    
    box_size = 11
    gap = 3
    
    # 53 weeks x 7 days
    grid_start_x = padding_x + 35
    grid_start_y = 65
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg.append('    .border { stroke: #30363d; stroke-width: 1; fill: none; rx: 10px; ry: 10px; }')
    svg.append('    .title-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('    .stat-label { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; fill: #c9d1d9; font-weight: bold; }')
    svg.append('    .stat-sub { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #8b949e; }')
    svg.append('    .day-label { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 9px; fill: #8b949e; }')
    svg.append('    .month-label { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 10px; fill: #8b949e; }')
    svg.append('    .day-box { rx: 2px; ry: 2px; }')
    svg.append('    @keyframes popIn {')
    svg.append('      from { opacity: 0; transform: scale(0.3); }')
    svg.append('      to { opacity: 1; transform: scale(1); }')
    svg.append('    }')
    svg.append('    .anim-box { opacity: 0; animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; transform-origin: center; }')
    svg.append('  </style>')
    
    # Background & border
    svg.append(f'  <rect width="{width}" height="{height}" class="bg" />')
    svg.append(f'  <rect width="{width}" height="{height}" class="border" />')
    
    # Terminal header
    svg.append('  <circle cx="15" cy="14" r="4.5" fill="#ff5f56" />')
    svg.append('  <circle cx="28" cy="14" r="4.5" fill="#ffbd2e" />')
    svg.append('  <circle cx="41" cy="14" r="4.5" fill="#27c93f" />')
    svg.append(f'  <text x="{width // 2}" y="17" class="title-text" text-anchor="middle">echlouchi@github ~ ./contributions.sh</text>')
    
    # Top stats bar
    svg.append(f'  <text x="{padding_x}" y="45" class="stat-label">{total_contribs:,} <tspan class="stat-sub">contributions in the last year</tspan></text>')
    svg.append(f'  <text x="{width - padding_x}" y="45" class="stat-label" text-anchor="end">🔥 {current_streak} days streak <tspan class="stat-sub">(max: {longest_streak}d)</tspan></text>')
    
    # Day of week labels (Mon, Wed, Fri)
    day_names = ["Mon", "Wed", "Fri"]
    day_indices = [1, 3, 5]
    for name, idx in zip(day_names, day_indices):
        dy = grid_start_y + idx * (box_size + gap) + 9
        svg.append(f'  <text x="{padding_x + 10}" y="{dy}" class="day-label">{name}</text>')
        
    # Process grid columns (53 weeks)
    # If we have days, place them week by week
    # Each week has 7 days (Sun=0..Sat=6)
    if days:
        # Group days into weeks
        weeks = []
        current_week = []
        for d in days:
            current_week.append(d)
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []
        if current_week:
            weeks.append(current_week)
    else:
        # Generate dummy 53x7 grid if no data yet
        weeks = []
        import random
        random.seed(42)
        for w in range(53):
            week = []
            for d in range(7):
                lvl = random.choices([0, 1, 2, 3, 4], weights=[60, 15, 12, 8, 5])[0]
                week.append({"level": lvl, "count": lvl * 3, "date": "2026-01-01"})
            weeks.append(week)
            
    for w_idx, week in enumerate(weeks[:53]):
        bx = grid_start_x + w_idx * (box_size + gap)
        for d_idx, day_info in enumerate(week[:7]):
            by = grid_start_y + d_idx * (box_size + gap)
            level = min(day_info.get("level", 0), len(PALETTE) - 1)
            color = PALETTE[level]
            
            # Diagonal stagger delay calculation
            delay = 0.1 + (w_idx + d_idx) * 0.015
            
            svg.append(f'  <rect x="{bx}" y="{by}" width="{box_size}" height="{box_size}" fill="{color}" class="day-box anim-box" style="animation-delay: {delay:.2f}s;" />')
            
    # Footer legend
    legend_y = grid_start_y + 7 * (box_size + gap) + 18
    svg.append(f'  <text x="{padding_x + 35}" y="{legend_y + 9}" class="day-label">Less</text>')
    for idx, col in enumerate(PALETTE):
        lx = padding_x + 62 + idx * (box_size + gap)
        svg.append(f'  <rect x="{lx}" y="{legend_y}" width="{box_size}" height="{box_size}" fill="{col}" class="day-box" />')
    svg.append(f'  <text x="{padding_x + 62 + len(PALETTE) * (box_size + gap) + 5}" y="{legend_y + 9}" class="day-label">More</text>')
    
    svg.append('</svg>')
    
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Heatmap SVG saved to {output_path}")

if __name__ == "__main__":
    render_heatmap()

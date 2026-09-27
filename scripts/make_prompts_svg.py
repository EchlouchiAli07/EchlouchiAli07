import os

def create_prompt_svg(command_text, output_path, width=450, height=36):
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .prompt-bg { fill: #161b22; rx: 8px; ry: 8px; stroke: #30363d; stroke-width: 1; }')
    svg.append('    .user { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; font-weight: bold; fill: #58a6ff; }')
    svg.append('    .at { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; fill: #8b949e; }')
    svg.append('    .host { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; fill: #79c0ff; }')
    svg.append('    .path { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; fill: #d2a8ff; }')
    svg.append('    .dollar { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; font-weight: bold; fill: #3fb950; }')
    svg.append('    .cmd { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 13px; font-weight: bold; fill: #f0f6fc; }')
    svg.append('  </style>')
    
    svg.append(f'  <rect width="{width}" height="{height}" class="prompt-bg" />')
    
    # Text positioning
    x = 16
    y = 23
    svg.append(f'  <text x="{x}" y="{y}">')
    svg.append(f'    <tspan class="user">echlouchi</tspan>')
    svg.append(f'    <tspan class="at">@</tspan>')
    svg.append(f'    <tspan class="host">github</tspan>')
    svg.append(f'    <tspan class="at"> </tspan>')
    svg.append(f'    <tspan class="path">~</tspan>')
    svg.append(f'    <tspan class="dollar"> $ </tspan>')
    
    escaped_cmd = command_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    svg.append(f'    <tspan class="cmd">{escaped_cmd}</tspan>')
    svg.append(f'  </text>')
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Prompt SVG saved to {output_path}")

if __name__ == "__main__":
    create_prompt_svg("./contributions.sh", "prompt-contributions.svg", width=420, height=36)
    create_prompt_svg("whoami --neofetch", "prompt-whoami.svg", width=380, height=36)
    create_prompt_svg("cat skills.json", "prompt-skills.svg", width=340, height=36)

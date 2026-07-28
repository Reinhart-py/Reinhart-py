#!/usr/bin/env python3
import sys
import os
import re
from PIL import Image

def get_dithered_points(img_path, max_width=300, max_height=338, threshold=128):
    """Loads an image, resizes it, converts to grayscale, and returns coordinate points of dark pixels."""
    try:
        img = Image.open(img_path)
    except Exception as e:
        print(f"Error opening {img_path}: {e}")
        sys.exit(1)
        
    img = img.convert("L")
    img.thumbnail((max_width, max_height))
    
    # Calculate offset to center the image within the bounding frame (300 x 338)
    w, h = img.size
    dx = (max_width - w) // 2
    dy = (max_height - h) // 2
    
    points = []
    for y in range(h):
        for x in range(w):
            val = img.getpixel((x, y))
            if val < threshold:  # Dark pixel
                points.append((x + dx, y + dy))
    return points

def build_portrait_paths(points):
    """Splits points into scanlines and constructs SVG <path> elements with animation fade-ins."""
    # Group points by y coordinate
    lines = {}
    for x, y in points:
        lines.setdefault(y, []).append(x)
        
    paths = []
    # Total animation duration is 0.9s. Start timings stretch from 0.20s to 0.70s based on vertical position
    y_min = min(lines.keys()) if lines else 0
    y_max = max(lines.keys()) if lines else 1
    y_range = max(1, y_max - y_min)
    
    for y in sorted(lines.keys()):
        x_coords = sorted(lines[y])
        # Group contiguous pixels on same row to create continuous horizontal lines
        runs = []
        if not x_coords:
            continue
            
        start_x = x_coords[0]
        prev_x = x_coords[0]
        for x in x_coords[1:]:
            if x == prev_x + 1:
                prev_x = x
            else:
                runs.append((start_x, prev_x))
                start_x = x
                prev_x = x
        runs.append((start_x, prev_x))
        
        # Build path data string
        d_parts = []
        for sx, ex in runs:
            length = ex - sx + 1
            d_parts.append(f"M{sx} {y}h{length}")
            
        d_str = "".join(d_parts)
        
        # Calculate fade-in timing based on scanline height
        norm_y = (y - y_min) / y_range
        begin_time = 0.20 + (norm_y * 0.50)
        
        path_str = (
            f'<g opacity="0">'
            f'<animate attributeName="opacity" values="0;1" dur="0.9s" begin="{begin_time:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".4 0 .2 1"/>'
            f'<path d="{d_str}"/></g>'
        )
        paths.append(path_str)
        
    return "\n".join(paths)

def patch_svg(template_path, target_path, portrait_paths_str, logo_points):
    print(f"Generating customized SVG: {target_path}...")
    with open(template_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    # Determine theme fill color from template
    fill_match = re.search(r'shape-rendering="crispEdges"\s*fill="([^"]+)"', svg_content)
    fill_color = fill_match.group(1) if fill_match else "#A78BFA"
    href_type = "tvlight" if "light" in target_path else "tvdark"

    # 1. Replace the first portrait scanline group (Group 1: lines 32 to 94)
    # Start tag: <g transform="translate(50,86) scale(1.2400,1.4471)" fill="..." shape-rendering="crispEdges">
    # End tag: start of Group 2 (which has opacity="0")
    portrait_pattern = re.compile(
        r'(<g transform="translate\(50,86\) scale\(1\.2400,1\.4471\)" fill="[^"]+" shape-rendering="crispEdges">).*?(</g>\s*<g transform="translate\(50,86\) scale\(1\.2400,1\.4471\)" fill="[^"]+" shape-rendering="crispEdges" opacity="0">)',
        re.DOTALL
    )
    
    new_portrait = r'\1\n' + portrait_paths_str + r'\n\2'
    svg_content = portrait_pattern.sub(new_portrait, svg_content)

    # 2. Empty the shatter group (Group 2: lines 95 to 191) to prevent old face fragments from flying around
    shatter_pattern = re.compile(
        r'(<g transform="translate\(50,86\) scale\(1\.2400,1\.4471\)" fill="[^"]+" shape-rendering="crispEdges" opacity="0">).*?(</g>\s*</g>\s*<defs>)',
        re.DOTALL
    )
    # We replace its inner contents with just the opacity setter, a single closing tag, and defs
    new_shatter = r'\1\n<set attributeName="opacity" to="1" begin="3.2s"/>\n</g>\n<defs>'
    svg_content = shatter_pattern.sub(new_shatter, svg_content)

    # 3. Find existing particles count
    import random
    random.seed(42)
    
    # Let's count how many <use tags exist in the template before we modify it
    with open(template_path, "r", encoding="utf-8") as f:
        orig_content = f.read()
    num_particles = len(re.findall(rf'<use href="#{href_type}"', orig_content))
    if num_particles == 0:
        num_particles = 900
        
    print(f"Mapping {num_particles} animated particles for {href_type}...")

    # Scale logo points to center region x: [80, 220], y: [120, 260]
    logo_x = [p[0] for p in logo_points]
    logo_y = [p[1] for p in logo_points]
    
    lx_min, lx_max = min(logo_x) if logo_x else 0, max(logo_x) if logo_x else 1
    ly_min, ly_max = min(logo_y) if logo_y else 0, max(logo_y) if logo_y else 1
    
    scaled_logo_points = []
    for x, y in logo_points:
        sx = int(80 + ((x - lx_min) / max(1, lx_max - lx_min)) * 140)
        sy = int(120 + ((y - ly_min) / max(1, ly_max - ly_min)) * 140)
        scaled_logo_points.append((sx, sy))
        
    sampled_points = []
    if len(scaled_logo_points) > 0:
        while len(sampled_points) < num_particles:
            sampled_points.extend(scaled_logo_points)
        sampled_points = sampled_points[:num_particles]
        random.shuffle(sampled_points)
    else:
        sampled_points = [(random.randint(80, 220), random.randint(120, 260)) for _ in range(num_particles)]

    # Re-build <use> tags
    new_particles = []
    for i in range(num_particles):
        tx, ty = sampled_points[i]
        x0, y0 = random.randint(10, 290), random.randint(90, 330)
        x2, y2 = tx, ty
        x4, y4 = tx + random.randint(-8, 8), ty + random.randint(-8, 8)
        
        val_str = f"{x0} {y0};{x0} {y0};{x2} {y2};{x2} {y2};{x4} {y4};{x4} {y4};{x2} {y2};{x2} {y2};{x0} {y0}"
        
        particle_str = (
            f'<use href="#{href_type}" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;1;1;1;1;1;0" keyTimes="0.000;0.194;0.288;0.432;0.525;0.669;0.763;0.906;1.000" dur="13.9s" begin="3.2s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="{val_str}" keyTimes="0.000;0.194;0.288;0.432;0.525;0.669;0.763;0.906;1.000" dur="13.9s" begin="3.2s" repeatCount="indefinite"/>'
            f'</use>'
        )
        new_particles.append(particle_str)
        
    # Replace particles block using exact indices
    first_use_idx = svg_content.find(f'<use href="#{href_type}"')
    last_use_idx = svg_content.rfind('</use>')
    
    if first_use_idx != -1 and last_use_idx != -1:
        last_use_idx += 6  # include length of </use>
        svg_content = svg_content[:first_use_idx] + "\n".join(new_particles) + svg_content[last_use_idx:]
    else:
        print(f"Warning: Could not locate particle positions in {template_path}.")    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

def main():
    print("Extracting coordinates from images...")
    # Your photo: convert to dither coordinates (width=300, height=338 to fit frame)
    portrait_points = get_dithered_points("photo.png", max_width=300, max_height=338, threshold=120)
    print(f"Extracted {len(portrait_points)} portrait points.")
    
    # Your logo: extract points to guide the 900 floating particles
    logo_points = get_dithered_points("logo.png", max_width=180, max_height=180, threshold=128)
    print(f"Extracted {len(logo_points)} logo points.")
    
    portrait_paths = build_portrait_paths(portrait_points)
    
    # Patch both dark and light SVGs
    patch_svg("dark.svg", "dark.svg", portrait_paths, logo_points)
    patch_svg("light.svg", "light.svg", portrait_paths, logo_points)
    print("Successfully updated both dark and light SVGs!")

if __name__ == "__main__":
    main()

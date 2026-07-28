#!/usr/bin/env python3
import sys
import os
import re
from PIL import Image

def get_dithered_photo_points(img_path, max_width=300, max_height=338, target_light=False):
    """Applies Floyd-Steinberg error diffusion dithering to get high-fidelity shaded points."""
    try:
        img = Image.open(img_path).convert("RGB")
    except Exception as e:
        print(f"Error opening {img_path}: {e}")
        sys.exit(1)
        
    # Apply soft elliptical vignette to clean out background corners
    w, h = img.size
    cx, cy = w / 2.0, h * 0.45
    rx, ry = w * 0.42, h * 0.46
    
    bg_color = (0, 0, 0) if target_light else (255, 255, 255)
    
    pixels = img.load()
    for y in range(h):
        for x in range(w):
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            dist = dx*dx + dy*dy
            if dist > 1.0:
                pixels[x, y] = bg_color
            else:
                factor = 1.0
                if dist > 0.5:
                    # Smoothly fade to background at the edges
                    factor = (1.0 - dist) / 0.5
                
                r, g, b = pixels[x, y]
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                
                if target_light:
                    # Dark theme: map gray [0, 255] to [60, 255] and fade to black (0)
                    adjusted_gray = int(60 + (gray / 255.0) * (255.0 - 60))
                    final_gray = int(adjusted_gray * factor)
                else:
                    # Light theme: map gray [0, 255] to [0, 195] and fade to white (255)
                    adjusted_gray = int((gray / 255.0) * 195)
                    final_gray = int(255 - (255 - adjusted_gray) * factor)
                
                pixels[x, y] = (final_gray, final_gray, final_gray)
                
    img = img.convert("L")
    img.thumbnail((max_width, max_height))
    w, h = img.size
    
    # Centering offsets
    dx = (max_width - w) // 2
    dy = (max_height - h) // 2
    
    # Load pixels into a 2D float array to distribute errors without rounding issues
    pixels_data = list(img.getdata())
    arr = [[float(pixels_data[y * w + x]) for x in range(w)] for y in range(h)]
    
    points = []
    for y in range(h):
        for x in range(w):
            old_val = arr[y][x]
            # Clamp value
            old_val = max(0.0, min(255.0, old_val))
            
            # Quantize to 0 (black) or 255 (white)
            new_val = 0.0 if old_val < 128.0 else 255.0
            arr[y][x] = new_val
            
            error = old_val - new_val
            
            # Diffuse error to neighbors
            if x + 1 < w:
                arr[y][x+1] += error * 7.0 / 16.0
            if y + 1 < h:
                if x - 1 >= 0:
                    arr[y+1][x-1] += error * 3.0 / 16.0
                arr[y+1][x] += error * 5.0 / 16.0
                if x + 1 < w:
                    arr[y+1][x+1] += error * 1.0 / 16.0
            
            # For dark theme (target_light=True), we want light pixels (new_val == 255.0)
            # For light theme (target_light=False), we want dark pixels (new_val == 0.0)
            target_val = 255.0 if target_light else 0.0
            if new_val == target_val:
                points.append((x + dx, y + dy))
                
    return points

def get_logo_points(img_path, max_width=180, max_height=180):
    """Extracts points representing the white shape/mask on a black background."""
    try:
        img = Image.open(img_path).convert("L")
    except Exception as e:
        print(f"Error opening {img_path}: {e}")
        sys.exit(1)
        
    img.thumbnail((max_width, max_height))
    w, h = img.size
    
    # Center offsets
    dx = (max_width - w) // 2
    dy = (max_height - h) // 2
    
    points = []
    for y in range(h):
        for x in range(w):
            val = img.getpixel((x, y))
            # We want the white pixels (representing the mask/logo)
            if val > 128:
                points.append((x + dx, y + dy))
    return points

def build_portrait_paths(points):
    """Splits points into scanlines and constructs SVG <path> elements with closed loop coordinates."""
    # Group points by y coordinate
    lines = {}
    for x, y in points:
        lines.setdefault(y, []).append(x)
        
    paths = []
    y_min = min(lines.keys()) if lines else 0
    y_max = max(lines.keys()) if lines else 1
    y_range = max(1, y_max - y_min)
    
    for y in sorted(lines.keys()):
        x_coords = sorted(lines[y])
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
        
        # Build path data string with filled 1px height boxes: M{x} {y}h{w}v1h-{w}z
        d_parts = []
        for sx, ex in runs:
            length = ex - sx + 1
            d_parts.append(f"M{sx} {y}h{length}v1h-{length}z")
            
        d_str = "".join(d_parts)
        
        # Timing calculation based on scanline height
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

    fill_match = re.search(r'shape-rendering="crispEdges"\s*fill="([^"]+)"', svg_content)
    fill_color = fill_match.group(1) if fill_match else "#A78BFA"
    href_type = "tvlight" if "light" in target_path else "tvdark"

    # 1. Replace first portrait scanline group (Group 1)
    portrait_pattern = re.compile(
        r'(<g transform="translate\(50,86\) scale\(1\.2400,1\.4471\)" fill="[^"]+" shape-rendering="crispEdges">).*?(</g>\s*<g transform="translate\(50,86\) scale\(1\.2400,1\.4471\)" fill="[^"]+" shape-rendering="crispEdges" opacity="0">)',
        re.DOTALL
    )
    # Restore the timer to hide the face at 3.2s
    new_portrait = r'\1\n<set attributeName="opacity" to="0" begin="3.2s"/>\n' + portrait_paths_str + r'\n\2'
    svg_content = portrait_pattern.sub(new_portrait, svg_content)

    # 2. Empty the shatter group (Group 2)
    shatter_pattern = re.compile(
        r'(<g transform="translate\(50,86\) scale\(1\.2400,1\.4471\)" fill="[^"]+" shape-rendering="crispEdges" opacity="0">).*?(</g>\s*</g>\s*<defs>)',
        re.DOTALL
    )
    new_shatter = r'\1\n<set attributeName="opacity" to="1" begin="3.2s"/>\n</g>\n<defs>'
    svg_content = shatter_pattern.sub(new_shatter, svg_content)

    # 3. Find existing particles count
    import random
    random.seed(42)
    
    with open(template_path, "r", encoding="utf-8") as f:
        orig_content = f.read()
    num_particles = len(re.findall(rf'<use href="#{href_type}"', orig_content))
    if num_particles == 0:
        num_particles = 900
        
    print(f"Mapping {num_particles} animated particles for {href_type}...")

    # Scale logo points to center region x: [80, 220], y: [120, 260]
    print(f"DEBUG inside patch_svg for {target_path}: logo_points len={len(logo_points)}")
    logo_x = [p[0] for p in logo_points]
    logo_y = [p[1] for p in logo_points]
    print(f"DEBUG inside patch_svg: logo_x range={min(logo_x) if logo_x else None} to {max(logo_x) if logo_x else None}")
    print(f"DEBUG inside patch_svg: logo_y range={min(logo_y) if logo_y else None} to {max(logo_y) if logo_y else None}")
    
    lx_min, lx_max = min(logo_x) if logo_x else 0, max(logo_x) if logo_x else 1
    ly_min, ly_max = min(logo_y) if logo_y else 0, max(logo_y) if logo_y else 1
    
    scaled_logo_points = []
    for x, y in logo_points:
        sx = int(80 + ((x - lx_min) / max(1, lx_max - lx_min)) * 140)
        sy = int(120 + ((y - ly_min) / max(1, ly_max - ly_min)) * 140)
        scaled_logo_points.append((sx, sy))
        
    print(f"DEBUG inside patch_svg: scaled Y range={min(p[1] for p in scaled_logo_points) if scaled_logo_points else None} to {max(p[1] for p in scaled_logo_points) if scaled_logo_points else None}")
        
    sampled_points = []
    if len(scaled_logo_points) > 0:
        while len(sampled_points) < num_particles:
            sampled_points.extend(scaled_logo_points)
        random.shuffle(sampled_points)
        sampled_points = sampled_points[:num_particles]
    else:
        sampled_points = [(random.randint(80, 220), random.randint(120, 260)) for _ in range(num_particles)]

    # Re-build <use> tags
    new_particles = []
    tys = []
    for i in range(num_particles):
        tx, ty = sampled_points[i]
        tys.append(ty)
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
    print(f"DEBUG: generated particles ty range: {min(tys)} to {max(tys)}")
        
    first_use_idx = svg_content.find(f'<use href="#{href_type}"')
    last_use_idx = svg_content.rfind('</use>')
    
    if first_use_idx != -1 and last_use_idx != -1:
        last_use_idx += 6
        svg_content = svg_content[:first_use_idx] + "\n".join(new_particles) + svg_content[last_use_idx:]
    else:
        print(f"Warning: Could not locate particle positions in {template_path}.")
        
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

def main():
    print("Extracting coordinates from images...")
    # Get points for logo (white shape on black background)
    logo_points = get_logo_points("logo.png", max_width=180, max_height=180)
    print(f"Extracted {len(logo_points)} logo points.")
    
    # Generate for dark.svg (target_light=True to render light parts on a dark background)
    dark_portrait_points = get_dithered_photo_points("photo.png", max_width=300, max_height=338, target_light=True)
    print(f"Extracted {len(dark_portrait_points)} dark portrait points.")
    dark_portrait_paths = build_portrait_paths(dark_portrait_points)
    patch_svg("dark.svg", "dark.svg", dark_portrait_paths, logo_points)
    
    # Generate for light.svg (target_light=False to render dark parts on a light background)
    light_portrait_points = get_dithered_photo_points("photo.png", max_width=300, max_height=338, target_light=False)
    print(f"Extracted {len(light_portrait_points)} light portrait points.")
    light_portrait_paths = build_portrait_paths(light_portrait_points)
    patch_svg("light.svg", "light.svg", light_portrait_paths, logo_points)
    
    print("Successfully updated both dark and light SVGs!")

if __name__ == "__main__":
    main()

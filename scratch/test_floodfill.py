import collections
from PIL import Image, ImageFilter

def remove_background(img_path, tolerance=32):
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    
    # Visited/mask array: 0 = foreground (person), 1 = background
    mask = [[0 for _ in range(w)] for _ in range(h)]
    pixels = img.load()
    
    # Queue for BFS flood fill
    queue = collections.deque()
    
    # Seed queue with all edge pixels (top, bottom, left, right edges)
    # We omit the bottom edge since the shirt might touch the bottom.
    for x in range(w):
        queue.append((x, 0)) # Top edge
    for y in range(h):
        queue.append((0, y)) # Left edge
        queue.append((w - 1, y)) # Right edge
        
    # Mark seed pixels as background
    for x, y in queue:
        mask[y][x] = 1
        
    # Neighbors directions
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # BFS flood fill
    while queue:
        cx, cy = queue.popleft()
        cr, cg, cb = pixels[cx, cy]
        
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < w and 0 <= ny < h:
                if mask[ny][nx] == 0:
                    # Check color similarity
                    nr, ng, nb = pixels[nx, ny]
                    diff = ((cr - nr)**2 + (cg - ng)**2 + (cb - nb)**2) ** 0.5
                    if diff < tolerance:
                        mask[ny][nx] = 1
                        queue.append((nx, ny))
                        
    # Create mask image and apply a small blur for soft edges
    mask_img = Image.new("L", (w, h), 0)
    mask_pixels = mask_img.load()
    for y in range(h):
        for x in range(w):
            if mask[y][x] == 1:
                mask_pixels[x, y] = 255
                
    # Blur mask slightly for smooth anti-aliasing
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(2))
    
    return mask_img

# Test floodfill background removal
mask = remove_background("photo.png")
mask.save("scratch/flood_mask.png")

# Save a preview of the masked image
img = Image.open("photo.png").convert("RGB")
w, h = img.size
pixels = img.load()
mask_pixels = mask.load()

for y in range(h):
    for x in range(w):
        m = mask_pixels[x, y] / 255.0
        # Blend with black to preview the dark theme background
        r, g, b = pixels[x, y]
        pixels[x, y] = (int(r * (1 - m)), int(g * (1 - m)), int(b * (1 - m)))
        
pixels_img = img
pixels_img.save("scratch/flood_masked_photo.png")
print("Saved flood mask and preview successfully!")

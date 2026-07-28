from PIL import Image

img = Image.open("photo.png").convert("RGB")
w, h = img.size
cx, cy = w / 2.0, h * 0.45
rx, ry = w * 0.42, h * 0.46

pixels = img.load()
for y in range(h):
    for x in range(w):
        dx = (x - cx) / rx
        dy = (y - cy) / ry
        dist = dx*dx + dy*dy
        if dist > 1.0:
            pixels[x, y] = (0, 0, 0)
        elif dist > 0.5:
            factor = (1.0 - dist) / 0.5
            r, g, b = pixels[x, y]
            pixels[x, y] = (int(r * factor), int(g * factor), int(b * factor))

img.save("scratch/vignetted_photo.png")
print("Saved vignetted photo successfully!")

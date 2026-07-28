import xml.etree.ElementTree as ET

tree = ET.parse("dark.svg")
root = tree.getroot()

# Find all animateTransform elements
namespace = {"svg": "http://www.w3.org/2000/svg"}
elements = root.findall(".//svg:animateTransform", namespace)

target_ys = []
for elem in elements:
    values = elem.get("values")
    if not values:
        continue
    parts = values.split(";")
    if len(parts) > 2:
        # Third keyframe is the logo position
        x2, y2 = parts[2].split()
        target_ys.append(int(y2))

print("Total elements:", len(elements))
print("Target Y range:", min(target_ys) if target_ys else None, max(target_ys) if target_ys else None)
print("Target Y sample:", target_ys[:30])

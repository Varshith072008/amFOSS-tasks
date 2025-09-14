import os
from PIL import Image
import math

def stitch_map(folder, output_file="treasure_map.png"):
    images = sorted(
        [f for f in os.listdir(folder) if f.lower().endswith(".png") and "blank" not in f.lower()]
    )
    
    if not images:
        print("No block images found in folder:", folder)
        return
    
    sample = Image.open(os.path.join(folder, images[0]))
    w, h = sample.size
    
   
    total = len(images)
    grid_size = math.ceil(math.sqrt(total))
    
    print(f"Found {total} blocks → arranging in {grid_size}x{grid_size} grid")

    while len(images) < grid_size * grid_size:
        blank = Image.new("RGB", (w, h), (255, 255, 255))  # white filler
        blank_name = f"auto_blank{len(images)+1}.png"
        blank.save(os.path.join(folder, blank_name))
        images.append(blank_name)

    map_img = Image.new("RGB", (w * grid_size, h * grid_size), (0, 0, 0))

    for idx, img_name in enumerate(images):
        img_path = os.path.join(folder, img_name)
        img = Image.open(img_path)
        x = (idx % grid_size) * w
        y = (idx // grid_size) * h
        map_img.paste(img, (x, y))

    map_img.save(output_file)
    print(f"Treasure map saved as {output_file}")


if __name__ == "__main__":
    folder = r"C:\Users\Varshith\OneDrive\Desktop\Treasure-Map\assets"
    stitch_map("Treasure-Map/assets")
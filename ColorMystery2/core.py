"""
ColorMystery Core Module

This module contains the main logic for generating a "coloriage mystère" image.
Depending on the mode selected, it either produces a coloring-by-number image with visible grid outlines,
or a mystery coloring image with uniform color zones and hidden outlines.
In both cases, each grid cell is filled with the average color of the corresponding region in the resized
input image and is annotated with its cell number.
"""

from math import ceil
from PIL import Image, ImageDraw, ImageFont

def compute_average_color(region: Image.Image) -> tuple:
    """
    Compute the average color of the given image region.
    Uses a 1x1 resize trick for fast averaging.
    """
    avg = region.resize((1,1)).getpixel((0,0))
    return avg

def process_image(image_path: str, mode: str, difficulty: str, detail: str,
                  id_set: str, palette: str, width: int, tile_size: int) -> str:
    """
    Process the image and generate a coloring mystery or numbered coloring output.

    Args:
        image_path: Input image file path.
        mode: Coloring mode ('number', 'mystery', or 'both'). 
              For "mystery": outlines are hidden, for "number": outlines are visible.
              "both" applies the "number" style (outlines visible).
        difficulty: Difficulty level ('easy', 'medium', 'hard').
        detail: Level of detail ('low', 'medium', 'high').
        id_set: Identifiers set ('numbers', 'letters', or 'symbols').
        palette: Palette option ('auto' or 'daltonism-friendly').
        width: Target width for resizing the image.
        tile_size: Size (in pixels) of each grid cell.

    Returns:
        output_path: The file path of the processed image.
    """
    try:
        # Open and resize the image while preserving aspect ratio.
        img = Image.open(image_path).convert("RGB")
        original_width, original_height = img.size
        ratio = width / original_width
        new_height = int(original_height * ratio)
        img = img.resize((width, new_height))
    except Exception as e:
        print(f"Erreur lors de l'ouverture ou du redimensionnement de l'image: {e}")
        return ""
    
    # Create a new image for output.
    output_img = Image.new("RGB", (width, new_height), "white")
    draw = ImageDraw.Draw(output_img)
    
    # Determine number of grid cells.
    cols = (width + tile_size - 1) // tile_size
    rows = (new_height + tile_size - 1) // tile_size
    count = 1
    
    for row in range(rows):
        for col in range(cols):
            x0 = col * tile_size
            y0 = row * tile_size
            x1 = min((col + 1) * tile_size, width)
            y1 = min((row + 1) * tile_size, new_height)
            
            # Crop the corresponding region from the resized input image.
            region = img.crop((x0, y0, x1, y1))
            avg_color = compute_average_color(region)
            
            # Fill the cell with the average color.
            draw.rectangle([x0, y0, x1, y1], fill=avg_color)
            
            # Draw grid outline if mode is "number" or "both".
            if mode in ["number", "both"]:
                draw.rectangle([x0, y0, x1, y1], outline="black", width=2)
            
            # Place cell number at the center.
            text = str(count)
            font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x0 + ((x1 - x0) - text_width) / 2
            text_y = y0 + ((y1 - y0) - text_height) / 2
            draw.text((text_x, text_y), text, fill="black", font=font)
            
            count += 1

    output_path = "result.png"
    output_img.save(output_path)
    print(f"Processing complete. Result saved as {output_path}")
    return output_path

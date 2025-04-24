"""
ColorMystery Core Module

This module contains the main logic for generating a "coloriage mystère" image.
The processing splits the image into grid cells with black contours and places a number in each cell,
while using a white background.
"""

from math import ceil
from PIL import Image, ImageDraw, ImageFont

def process_image(image_path: str, mode: str, difficulty: str, detail: str,
                  id_set: str, palette: str, width: int, tile_size: int) -> str:
    """
    Process the image and generate a coloring mystery output.
    
    Args:
        image_path: Input image file path.
        mode: Coloring mode ('number', 'mystery', or 'both') - for this demonstration, only 'mystery' style is produced.
        difficulty: Difficulty level ('easy', 'medium', 'hard').
        detail: Level of detail ('low', 'medium', 'high').
        id_set: Identifiers set ('numbers', 'letters', 'symbols').
        palette: Palette option ('auto' or 'daltonism-friendly').
        width: Target width for resizing the image.
        tile_size: Size (in pixels) of each grid cell.
    
    Returns:
        output_path: The file path of the processed image.
    """
    try:
        # Open and resize the image to the provided width, preserving aspect ratio.
        img = Image.open(image_path).convert("RGB")
        original_width, original_height = img.size
        ratio = width / original_width
        new_height = int(original_height * ratio)
        img = img.resize((width, new_height))
    except Exception as e:
        print(f"Erreur lors de l'ouverture ou du redimensionnement de l'image: {e}")
        return ""
    
    # Create a new image with white background.
    output_img = Image.new("RGB", (width, new_height), "white")
    draw = ImageDraw.Draw(output_img)
    
    # Determine number of grid cells horizontally and vertically.
    cols = (width + tile_size - 1) // tile_size
    rows = (new_height + tile_size - 1) // tile_size
    count = 1
    for row in range(rows):
        for col in range(cols):
            x0 = col * tile_size
            y0 = row * tile_size
            x1 = min((col + 1) * tile_size, width)
            y1 = min((row + 1) * tile_size, new_height)
            # Draw cell rectangle with black outline.
            draw.rectangle([x0, y0, x1, y1], outline="black", width=2)
            # Place the cell number at the center.
            text = str(count)
            font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x0 + (x1 - x0 - text_width) / 2
            text_y = y0 + (y1 - y0 - text_height) / 2
            draw.text((text_x, text_y), text, fill="black", font=font)
            count += 1

    output_path = "result.png"
    output_img.save(output_path)
    print(f"Processing complete. Result saved as {output_path}")
    return output_path
``` ````

````python name=app.py
"""
Streamlit UI for ColorMystery

This UI allows users to upload an image, process it into a coloring mystery style
(with grid cells, black outlines, numbers in each cell, and a white background),
display the processed result, and download the resulting image.
"""

import streamlit as st
from core import process_image
from PIL import Image

def main():
    st.title("ColorMystery")
    lang = st.selectbox("Choisir la langue / Select language", ["fr", "en"])
    mode = st.selectbox("Mode de coloriage", ["number", "mystery", "both"])
    difficulty = st.selectbox("Difficulté", ["easy", "medium", "hard"])
    detail = st.selectbox("Niveau de détail", ["low", "medium", "high"])
    id_set = st.selectbox("Jeu d'identifiants", ["numbers", "letters", "symbols"])
    palette = st.selectbox("Palette couleur", ["auto", "daltonism-friendly"])
    width = st.number_input("Largeur", value=1024)
    tile_size = st.number_input("Taille de tuile", value=1024)
    
    uploaded_file = st.file_uploader("Télécharger une image (max 50MB)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Display the uploaded image.
        image = Image.open(uploaded_file)
        st.image(image, caption="Image chargée", use_column_width=True)
        
        if st.button("Processer"):
            # Save the uploaded file temporarily.
            temp_path = "temp_image"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process the image and retrieve the output file path.
            output_path = process_image(temp_path, mode, difficulty, detail, id_set, palette, width, tile_size)
            
            if output_path:
                processed_image = Image.open(output_path)
                st.image(processed_image, caption="Image traitée", use_column_width=True)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Télécharger le résultat",
                        data=file,
                        file_name=output_path,
                        mime="image/png"
                    )
                st.success("Traitement terminé et image prête au téléchargement!")
            else:
                st.error("Échec du traitement de l'image.")

if __name__ == "__main__":
    main()
``` ````

````text name=requirements.txt
streamlit
numpy
opencv-python
Pillow
pytest
``` ````

````json name=fr.json
{
  "title": "ColorMystery",
  "upload": "Télécharger une image (max 50MB)",
  "process": "Processer",
  "success": "Image traitée et prête au téléchargement!"
}
``` ````

````json name=en.json
{
  "title": "ColorMystery",
  "upload": "Upload an image (max 50MB)",
  "process": "Process",
  "success": "Image processed and ready for download!"
}
``` ````

````dockerfile name=Dockerfile
# Base image with Python
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Streamlit
EXPOSE 8501

# Command to run Streamlit app
CMD ["streamlit", "run", "app.py"]
``` ````

````yaml name=.github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install black flake8
      - name: Lint with flake8
        run: flake8 .
      - name: Format with black --check
        run: black --check .
      - name: Run tests
        run: pytest --maxfail=1 --disable-warnings -q
``` ````

````text name=LICENSE
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
``` ````

````python name=tests/test_core.py
import pytest
from core import process_image

def test_process_image():
    # Create a dummy white image for testing.
    from PIL import Image
    dummy = Image.new("RGB", (200, 200), "white")
    dummy_path = "dummy.png"
    dummy.save(dummy_path)
    
    result_path = process_image(dummy_path, "mystery", "medium", "medium", "numbers", "auto", 200, 50)
    # Check if the result file exists and is not empty.
    with open(result_path, "rb") as f:
        content = f.read()
    assert len(content) > 0

if __name__ == "__main__":
    pytest.main()
``` ````

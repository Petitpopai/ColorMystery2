"""
Streamlit UI for ColorMystery

This UI allows users to upload an image, process it, display the processed result, and download the resulting image.
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
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Image chargée", use_column_width=True)
        
        if st.button("Processer"):
            # Save file temporarily
            temp_path = "temp_image"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process the image and get the output file path
            output_path = process_image(temp_path, mode, difficulty, detail, id_set, palette, width, tile_size)
            
            if output_path:
                # Load and display the processed image
                processed_image = Image.open(output_path)
                st.image(processed_image, caption="Image traitée", use_column_width=True)
                
                # Provide a download button for the processed image
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
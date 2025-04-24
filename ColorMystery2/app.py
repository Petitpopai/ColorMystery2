"""
Streamlit UI for ColorMystery
"""

import streamlit as st
from core import process_image

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
        st.image(uploaded_file, caption="Image chargée", use_column_width=True)
        if st.button("Processer"):
            # Save file temporarily
            with open("temp_image", "wb") as f:
                f.write(uploaded_file.getbuffer())
            process_image("temp_image", mode, difficulty, detail, id_set, palette, width, tile_size)
            st.success("Image traitée avec succès!")

if __name__ == "__main__":
    main()
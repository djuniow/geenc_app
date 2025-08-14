import streamlit as st
import rastro
from camera_input_live import camera_input_live

num_obj = st.text_input(label="Objeto")
image = camera_input_live()

if image:
  st.image(image)

if st.button('Pesquisar'):
    resultado = rastro.get_postagem(data=num_obj)
    resultado
import streamlit as st
import rastro

num_obj = st.text_input(label="Objeto")

if st.button('Pesquisar'):
    resultado = rastro.get_postagem(data=num_obj)
    resultado
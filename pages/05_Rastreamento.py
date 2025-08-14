import streamlit as st
import rastro
from streamlit_qrcode_scanner import qrcode_scanner

num_obj = st.text_input(label="Objeto")
qr_code = qrcode_scanner(key='qrcode_scanner')

if qr_code:
  st.write(qr_code)

if st.button('Pesquisar'):
    resultado = rastro.get_postagem(data=num_obj)
    resultado
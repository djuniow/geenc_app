import streamlit as st
import rastro
from datetime import datetime
from streamlit_qrcode_scanner import qrcode_scanner



qr_code = qrcode_scanner()
if qr_code:
    num_correto = rastro.get_num_obj(qr_code)
    st.write(num_correto)
else:
    num_correto = ''

num_obj = st.text_input(label="Objeto",value=num_correto)

if st.button('Pesquisar'):
    resultado = rastro.get_postagem(data=num_obj)
    col1, col2 = st.columns(2)
    with col1:
        data_str = resultado['dtPrevista']
        data_convertida = datetime.fromisoformat(data_str)
        agora = datetime.now()

        st.write(f"Categoria: {resultado['categoria']}")
        with st.container():

            st.markdown(f"""
                <div style="background-color:#dff0d8; padding:15px; border-radius:8px;">
                    <h4 style="color:#3c763d;">{data_convertida - agora}</h4>
                </div>
            """, unsafe_allow_html=True)
        st.write(f"Data max: {resultado['dtPrevista']}")
        st.write(f"largura: {resultado['largura']}")
        st.write(f"comprimento: {resultado['comprimento']}")
        st.write(f"altura: {resultado['altura']}")

    with col2:

        resultado





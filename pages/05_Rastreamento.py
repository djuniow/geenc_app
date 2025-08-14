import streamlit as st
import rastro
from datetime import datetime
from streamlit_qrcode_scanner import qrcode_scanner
st.set_page_config(layout='wide',initial_sidebar_state="collapsed",page_icon='images/caminhão.PNG')

st.page_link(label='Voltar',page='Endereços.py',icon='⬅️',use_container_width=True)

qr_code = qrcode_scanner()
if qr_code:
    num_correto = rastro.get_num_obj(qr_code)
    st.write(num_correto)
else:
    num_correto = ''

num_obj = st.text_input(label="Objeto",value=num_correto)
num_obj = num_obj.upper()

if st.button('Pesquisar'):
    resultado = rastro.get_postagem(data=num_obj)
    col1, col2 = st.columns(2)

    with col1:
        data_str = resultado['dtPrevista']
        data_convertida = datetime.fromisoformat(data_str)
        agora = datetime.now()
        data_formatada = data_convertida.strftime("%d/%m/%Y")

        st.write(f"Categoria: {resultado['categoria']}")
        with st.container():
            prazo = data_convertida - agora
            st.markdown(rastro.cor_prazo(int(prazo.days)), unsafe_allow_html=True)
        st.write(f"Data max: {data_formatada}")
        st.write(f"largura: {resultado['largura']}")
        st.write(f"comprimento: {resultado['comprimento']}")
        st.write(f"altura: {resultado['altura']}")

    with col2:
        st.write('')





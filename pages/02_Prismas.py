import streamlit as st
import pandas as pd
st.set_page_config(layout='wide',initial_sidebar_state="collapsed",page_icon='images/caminhão.PNG')
st.title('Prismas')

st.page_link(label='Voltar',page='Endereços.py',icon='⬅️',use_container_width=True)

data = pd.read_excel('dados/prismas.xlsx')

opcoes = pd.concat([data['PRISMA'],data['UNIDADE']])

busca = st.selectbox('Selecione o prisma ou unidade', options=opcoes)

if type(busca) is int:
    data_busca = data.loc[data['PRISMA']==busca]
    st.table(data_busca)
elif type(busca) is str:
    data_busca = data.loc[data['UNIDADE']== busca]
    st.table(data_busca)
else:
    st.table(data)

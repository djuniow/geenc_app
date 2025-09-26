import pandas as pd
import streamlit as st
st.set_page_config(layout='wide',initial_sidebar_state="collapsed",page_icon='images/caminhão.PNG')



st.page_link(label='Voltar',page='Endereços.py',icon='⬅️',use_container_width=True)

import streamlit as st
import malha as m





@st.fragment
def aba_malha():
    st.subheader('Malha de Transporte')
    col1, col2, col3 = st.columns(3)
    with col1:
        linha = st.text_input(label='Linha')

    with col2:
        tonelagem = st.selectbox(label='Tonelagem',
                                 options=lista_ton,
                                 index=None)
    with col3:
        transportadora = st.selectbox(label='Transportadora',
                                      options=lista_transportadora,
                                      index=None)

    listaDuplaUnidades = lista_unidades + lista_unidades
    unidade = st.multiselect(label='Unidades',
                             options=listaDuplaUnidades,
                             max_selections=2)

    with st.spinner('Buscando'):
        with st.container(height=1000, border=False):
            df_teste = m.busca_banco(linha=linha,
                                     transportadora=transportadora,
                                     tonelagem=tonelagem,
                                     unidades=unidade)

            m.mostra_linhas(data_frames=df_teste,
                            dataframeEndereco=dfEnderecos)

def carregamento():
    lista_unidades = m.carregamento_unidades()
    lista_linhas = m.carregamento_linhas()
    lista_ton = m.carregamento_ton()
    lista_transportadora = m.carregamento_transportadora()
    return lista_linhas,lista_unidades, lista_ton, lista_transportadora
lista_linhas,lista_unidades, lista_ton, lista_transportadora = carregamento()

dfEnderecos = m.carregamentoEnderecos()


aba_malha()


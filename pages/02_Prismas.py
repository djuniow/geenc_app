import streamlit as st
import pandas as pd
st.set_page_config(layout='wide',initial_sidebar_state="collapsed",page_icon='images/caminhão.PNG')
st.page_link(label='Voltar',page='Endereços.py',icon='⬅️',use_container_width=True)
st.title('⚠️Prismas')

data = pd.read_excel('dados/prismas.xlsx')

opcoes = pd.concat([data['PRISMA'].drop_duplicates(),data['UNIDADE'].drop_duplicates()])

busca = st.selectbox('Selecione o prisma ou unidade', options=opcoes)

if type(busca) is int:
    data_busca = data.loc[data['PRISMA']==busca]
    html_tabela = data_busca.to_html(index=False, classes='minha-tabela')

    # Define o estilo CSS para a tabela
    css = """
    <style>
    .minha-tabela {
       border-collapse: collapse;
       width: 100%;
       font-family: Arial, sans-serif;
    }
    .minha-tabela th, .minha-tabela td {
       border: 1px solid black;
       padding: 8px;
       text-align: left;
    }
    .minha-tabela th {
       background-color: #f2f2f2;
    }
    </style>"""

    # Renderiza o CSS + HTML da tabela no Streamlit
    st.markdown(css + html_tabela, unsafe_allow_html=True)
elif type(busca) is str:
    data_busca = data.loc[data['UNIDADE']== busca]
    html_tabela = data_busca.to_html(index=False, classes='minha-tabela')

    # Define o estilo CSS para a tabela
    css = """
    <style>
    .minha-tabela {
       border-collapse: collapse;
       width: 100%;
       font-family: Arial, sans-serif;
    }
    .minha-tabela th, .minha-tabela td {
       border: 1px solid black;
       padding: 8px;
       text-align: left;
    }
    .minha-tabela th {
       background-color: #f2f2f2;
    }
    </style>"""

    # Renderiza o CSS + HTML da tabela no Streamlit
    st.markdown(css + html_tabela, unsafe_allow_html=True)
else:
    st.table(data)
# Gera a tabela HTML a partir do DataFrame 'mostra_linhas' com as colunas selecionadas

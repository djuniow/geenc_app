import streamlit as st
import pandas as pd
st.title('Prismas')


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
    print('foi')
import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import  Hasher
import yaml
from yaml.loader import SafeLoader

hashed_password = Hasher(['abc','def']).generate()

with open ('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)



authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)
name, authenticator_status, username = authenticator.login()

@st.cache_resource
def carregamento_uni():
    df_unidades = pd.read_excel(r'dados\endereco_unidades.xlsx')
    df_unidades_lista = df_unidades['UNIDADE:'].drop_duplicates()

    return df_unidades_lista , df_unidades

if authenticator_status:
    with st.sidebar:
        authenticator.logout()
    df_unidades_lista, df_unidades = carregamento_uni()

    uni_pesquisa = st.selectbox(label='Unidade',options=df_unidades_lista)


    endereco_unidade = df_unidades.loc[df_unidades['UNIDADE:']==uni_pesquisa]
    endereco_unidade = endereco_unidade.reset_index()
    lat_unidade = endereco_unidade['LATITUDE:'][0]
    log_unidade = endereco_unidade['LONGITUDE:'][0]
    nome_unidade = str(endereco_unidade["UNIDADE:"][0]).replace(' ', '2%')
    end_unidade = str(endereco_unidade["CEP:"][0]).replace(' ', '2%')
    st.subheader(endereco_unidade['UNIDADE:'][0])
    st.write('Endereço:')
    st.write(endereco_unidade['CEP:'][0])

    st.write('Compartilhar')
    st.markdown(f'[![Foo](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/50px-WhatsApp.svg.png)](https://api.whatsapp.com/send?text="{nome_unidade}2%{end_unidade})')
elif authenticator_status == False:
    st.error('Usuário errado')
elif authenticator_status == None:
    st.warning('Efetuar login')

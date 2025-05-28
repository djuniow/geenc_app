import streamlit as st
import pandas as pd


st.set_page_config(layout='wide')

@st.cache_resource
def carregamento_uni():
    df_unidades = pd.read_excel(r'dados/endereco_unidades.xlsx')
    df_unidades_lista = df_unidades['UNIDADE:'].drop_duplicates()

    return df_unidades_lista , df_unidades


df_unidades_lista, df_unidades = carregamento_uni()

uni_pesquisa = st.selectbox(label='Unidade',options=df_unidades_lista)


endereco_unidade = df_unidades.loc[df_unidades['UNIDADE:']==uni_pesquisa]
endereco_unidade = endereco_unidade.reset_index()
lat_unidade = endereco_unidade['LATITUDE:'][0]
log_unidade = endereco_unidade['LONGITUDE:'][0]
nome_unidade = str(endereco_unidade["UNIDADE:"][0]).replace(' ', '%20')
end_unidade = str(endereco_unidade["CEP:"][0]).replace(' ', '%20')
texto = str('*UNIDADE*'+'%20%0A'+nome_unidade+'%20%0A'+'*ENDEREÇO*'+'%20%0A'+end_unidade)
st.subheader(endereco_unidade['UNIDADE:'][0])
st.write('Endereço:')
st.write(endereco_unidade['CEP:'][0])

st.write('Compartilhar')
st.markdown(f'[![Foo](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/50px-WhatsApp.svg.png)](https://wa.me/?text={texto})')

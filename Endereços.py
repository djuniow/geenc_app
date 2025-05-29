import streamlit as st

st.title('CTCE INDAIATUBA/GEENC')
st.subheader('Menu')
st.page_link(label='🚚Conexões🚚',page='pages/01_Conexões.py',use_container_width=True)
st.divider()
st.page_link(label='⚠️Prismas⚠️', page='pages/02_Prismas.py', use_container_width=True)
st.divider()
st.page_link(label='🔥Contingencia🔥', page='pages/01_Conexões.py', use_container_width=True)
st.divider()
st.page_link(label='🌎Locais🌎', page='pages/04_Locais.py', use_container_width=True)


st.write('Desenvolvido por Djalma Luis')
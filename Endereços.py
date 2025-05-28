import streamlit as st

st.title('CTCE INDAIATUBA/GEENC')

col1, col2 = st.columns(2)

with col1:
    st.page_link(label='🚚Conexões🚚',page='pages/01_Conexões.py',icon='🔴',use_container_width=True)
    st.divider()
    st.page_link(label='⚠️Prismas⚠️', page='pages/02_Prismas.py', icon='🔵', use_container_width=True)

with col2:
    st.page_link(label='🔥Contingencia🔥', page='pages/01_Conexões.py', icon='🔵', use_container_width=True)
    st.divider()
    st.page_link(label='🌎Locais🌎', page='pages/02_Prismas.py', icon='🔴', use_container_width=True)


st.write('Desenvolvido por Djalma Luis')
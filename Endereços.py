import streamlit as st


# col1, col2 = st.columns(2)
#
#
# with col1:
#     st.markdown(
#         """<a href="https://idugeenc.streamlit.app/Conexões">
#         <img src="data:image/png;base64,{}" width="65">
#         </a>""".format(
#             base64.b64encode(open("images/mapa.png", "rb").read()).decode()
#         ),
#         unsafe_allow_html=True,
#     )
#     st.markdown(
#         """<a href="https://idugeenc.streamlit.app/Locais">
#         <img src="data:image/jpg;base64,{}" width="65">
#         </a>""".format(
#             base64.b64encode(open("images/endereços.jpg", "rb").read()).decode()
#         ),
#         unsafe_allow_html=True,
#     )

st.page_link(page='pages/01_Conexões.py',icon=":material/analytics:" )
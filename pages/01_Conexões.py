import pandas as pd
import streamlit as st
st.set_page_config(layout='wide',initial_sidebar_state="collapsed",page_icon='images/caminhão.PNG')

def carregamentos(caminho):
    df_linhas = pd.read_excel(caminho, sheet_name='bd')
    return df_linhas

def color_survived(val):
    if val == pesq_linha:
        color = '#f3fc88'

    else:
        color = 'white'


    return f'background-color: {color}'


def entrada(chamada_pesquisa):

    valida = ["['0']","['1']", "['2']", "['3']", "['4']", "['5']", "['6']", "['7']", "['8']", "['9']"]
    linha_entri = str(list(chamada_pesquisa[0]))
    linha_pesquisa = pesq_linha
    if linha_entri in valida:

        df_resultadoPesquisa = df_linhas[(df_linhas['No. da Linha'] == linha_pesquisa.upper())][cl]


        rod = list(df_resultadoPesquisa['No. da Linha'].unique())

        ajuste_freq = {1.0: 'Dom', 2.0: 'Seg', 3.0: 'Ter', 4.0: 'Qua', 5.0: 'Qui', 6.0: 'Sex', 7.0: 'Sab'}

        quantidade = 0
        distancia = 0
        #rod
        colunas = ['Sentido','Seq.', 'Local', 'Hora Chegada', 'Hora Partida']
        for i in rod:
            quantidade = quantidade + 1
            mostra_linhas = df_linhas[df_linhas['No. da Linha'] == i][cl]

            mostra_linhas['Segunda'] = mostra_linhas['Segunda'].map(ajuste_freq)
            mostra_linhas['Terça'] = mostra_linhas['Terça'].map(ajuste_freq)
            mostra_linhas['Quarta'] = mostra_linhas['Quarta'].map(ajuste_freq)
            mostra_linhas['Quinta'] = mostra_linhas['Quinta'].map(ajuste_freq)
            mostra_linhas['Sexta'] = mostra_linhas['Sexta'].map(ajuste_freq)
            mostra_linhas['Sábado'] = mostra_linhas['Sábado'].map(ajuste_freq)
            mostra_linhas['Domingo'] = mostra_linhas['Domingo'].map(ajuste_freq)

            mostra_linhas['Segunda'].fillna('-', inplace=True)
            mostra_linhas['Terça'].fillna('-', inplace=True)
            mostra_linhas['Quarta'].fillna('-', inplace=True)
            mostra_linhas['Quinta'].fillna('-', inplace
            =True)
            mostra_linhas['Sexta'].fillna('-', inplace=True)
            mostra_linhas['Sábado'].fillna('-', inplace=True)
            mostra_linhas['Domingo'].fillna('-', inplace=True)
            mostra_linhas['Distância'].fillna(0, inplace=True)
            mostra_linhas['Distância'].replace(" ", 0, inplace=True)
            mostra_linhas['Distância'] = mostra_linhas['Distância'].astype(int)
            tempo_percurso = mostra_linhas.iloc[0]['Tempo Percurso']

            transportadora = mostra_linhas.iloc[0]['Transportada.1']
            nunlinha = mostra_linhas.iloc[0]['No. da Linha']
            contrato = mostra_linhas.iloc[0]['No. Seq. Contrato']
            veiculo = mostra_linhas.iloc[0]['Descrição Modelo']
            ffreq = mostra_linhas[freq]

            ##########################################
            seg = mostra_linhas.iloc[0]['Segunda']
            ter = mostra_linhas.iloc[0]['Terça']
            qua = mostra_linhas.iloc[0]['Quarta']
            qui = mostra_linhas.iloc[0]['Quinta']
            sex = mostra_linhas.iloc[0]['Sexta']
            sab = mostra_linhas.iloc[0]['Sábado']
            dom = mostra_linhas.iloc[0]['Domingo']

            distancia = mostra_linhas['Distância'].sum()

            ############################################
            tabela = str(mostra_linhas[colunas])
            transp = str(transportadora)
            linha_pesquisa = str(nunlinha)
            tamanhocam = str(veiculo)
            se = str(seg)
            t = str(ter)
            q = str(qua)
            qi = str(qui)
            s = str(sex)
            sa = str(sab)
            d = str(dom)
            st.info('Linha: ' + linha_pesquisa + '  \n ' + ' Tansportadora:  ' + transp + '  \nVeiculo: ' + tamanhocam)
            st.warning('Frequência: ' + '|' + se + '|' + '|' + t + '|' + '|' + q + '|' + '|' + qi + '|' + '|' + s + '|' + '|' + sa + '|' + '|' + d + '|')

            # Gera a tabela HTML a partir do DataFrame 'mostra_linhas' com as colunas selecionadas
            html_tabela = mostra_linhas[colunas].to_html(index=False, classes='minha-tabela')

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

            # Adiciona um divisor visual


            st.divider()








    else:

        df_teste = df_linhas[(df_linhas['Local'] == pesq_unid)]
        df_teste2 = df_teste['No. da Linha'].drop_duplicates()
        rod1 = list(df_teste2)
        for s in rod1:
            df_linhas.loc[df_linhas['No. da Linha'] == s, 'conect'] = pesq_unid

        df_resultadoPesquisa = df_linhas[(df_linhas['Local'] == linha_pesquisa.upper()) & (df_linhas['conect'] == pesq_unid) ][cl]
        df_resultadoPesquisa.style.hide()



        rod = list(df_resultadoPesquisa['No. da Linha'].unique())
        ajuste_freq = {1.0: 'Dom', 2.0: 'Seg', 3.0: 'Ter', 4.0: 'Qua', 5.0: 'Qui', 6.0: 'Sex', 7.0: 'Sab'}

        quantidade = 0
        distancia = 0



        colunas = ['Sentido','Seq.', 'Local', 'Hora Chegada', 'Hora Partida']
        for i in rod:
            quantidade = quantidade + 1
            mostra_linhas = df_linhas.loc[(df_linhas['No. da Linha'] == i)][cl]
            #mostra_linhas = df_linhas[df_linhas['No. da Linha'] == i][cl] & df_linhas[df_linhas['conect'] == 'CTCE INDAIATUBA'][cl]

            mostra_linhas['Segunda'] = mostra_linhas['Segunda'].map(ajuste_freq)
            mostra_linhas['Terça'] = mostra_linhas['Terça'].map(ajuste_freq)
            mostra_linhas['Quarta'] = mostra_linhas['Quarta'].map(ajuste_freq)
            mostra_linhas['Quinta'] = mostra_linhas['Quinta'].map(ajuste_freq)
            mostra_linhas['Sexta'] = mostra_linhas['Sexta'].map(ajuste_freq)
            mostra_linhas['Sábado'] = mostra_linhas['Sábado'].map(ajuste_freq)
            mostra_linhas['Domingo'] = mostra_linhas['Domingo'].map(ajuste_freq)

            mostra_linhas['Segunda'].fillna('-', inplace=True)
            mostra_linhas['Terça'].fillna('-', inplace=True)
            mostra_linhas['Quarta'].fillna('-', inplace=True)
            mostra_linhas['Quinta'].fillna('-', inplace=True)
            mostra_linhas['Sexta'].fillna('-', inplace=True)
            mostra_linhas['Sábado'].fillna('-', inplace=True)
            mostra_linhas['Domingo'].fillna('-', inplace=True)
            mostra_linhas['Distância'].fillna(0, inplace=True)
            # mostra_linhas['Distância'].apply(lambda x:int(x))
            mostra_linhas['Distância'].replace(" ", 0, inplace=True)
            mostra_linhas['Distância'] = mostra_linhas['Distância'].astype(int)
            tempo_percurso = mostra_linhas.iloc[0]['Tempo Percurso']

            transportadora = mostra_linhas.iloc[0]['Transportada.1']
            nunlinha = mostra_linhas.iloc[0]['No. da Linha']
            contrato = mostra_linhas.iloc[0]['No. Seq. Contrato']
            veiculo = mostra_linhas.iloc[0]['Descrição Modelo']
            ffreq = mostra_linhas[freq]

            ##########################################
            seg = mostra_linhas.iloc[0]['Segunda']
            ter = mostra_linhas.iloc[0]['Terça']
            qua = mostra_linhas.iloc[0]['Quarta']
            qui = mostra_linhas.iloc[0]['Quinta']
            sex = mostra_linhas.iloc[0]['Sexta']
            sab = mostra_linhas.iloc[0]['Sábado']
            dom = mostra_linhas.iloc[0]['Domingo']

            distancia = mostra_linhas['Distância'].sum()
            ############################################

            tabela = mostra_linhas[colunas]

            transp = str(transportadora)
            linha_pesquisa = str(nunlinha)
            tamanhocam = str(veiculo)
            se = str(seg)
            t = str(ter)
            q = str(qua)
            qi = str(qui)
            s = str(sex)
            sa = str(sab)
            d = str(dom)
            st.info('Linha: ' + linha_pesquisa +'  \n '+' Tansportadora:  '+transp+'  \nVeiculo: '+tamanhocam)
            st.warning('Frequência: '+'|'+se+'|'+'|'+t+'|'+'|'+q+'|'+'|'+qi+'|'+'|'+s+'|'+'|'+sa+'|'+'|'+d+'|')
            #st.table(mostra_linhas[colunas].style.applymap(color_survived, subset=['Local']))
            html_tabela = mostra_linhas[colunas].style.applymap(color_survived, subset=['Local'])

            html_tabela = mostra_linhas[colunas].to_html(index=False, classes='minha-tabela')

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

            # Adiciona um divisor visual


            st.divider()

            st.divider()


df_linhas = carregamentos('dados/malha.xlsx')

df_linhas['No. da Linha'].fillna('00000', inplace=True)
df_linhas['conect'] = ""



df_linhas['radical_f'] = df_linhas['Local'].apply(lambda x: x[0:10])

frequencia = list(df_linhas.columns[0:16])
linha = list(df_linhas.columns[1:3])

outras_informacoes = [
    'Local', 'Distância', 'Hora Chegada', 'Hora Partida',
    'Transportada', 'Descrição Modelo', 'Seq.']
cl = frequencia + linha + outras_informacoes

cl = ['Tipo Linha', 'No. da Linha', 'Modelo Veículo', 'Descrição Modelo', 'No. Seq. Contrato', 'Domingo', 'Segunda',
      'Terça',
      'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Transportada', 'Transportada.1', 'Seq.', 'Local',
      'Distância', 'Hora Chegada', 'Hora Partida', 'Tempo Serviço',
      'Tempo Espera', 'Tempo Percurso', 'Sentido']

freq = ['Domingo', 'Segunda', 'Terça',
        'Quarta', 'Quinta', 'Sexta', 'Sábado']
suges_linha = df_linhas['No. da Linha'].drop_duplicates()
suges_unid = df_linhas['Local'].drop_duplicates()
sele = pd.DataFrame({'item':['Selecione']})
sele1 = pd.DataFrame({'item':['CTCE INDAIATUBA']})
junt = pd.concat([sele['item'],suges_linha, suges_unid]).dropna()
junt1 = pd.concat([sele1['item'],suges_linha, suges_unid]).dropna()


st.page_link(label='Voltar',page='Endereços.py',icon='⬅️',use_container_width=True)


st.title('Consulta conexões')


pesq_linha = st.selectbox(label='Selecione a Linha ou Unidade', options=junt.sort_index())

pesq_unid = st.selectbox(label='Selecione a Unidade para conexão:', options=junt1.sort_index())

entrada(chamada_pesquisa=pesq_linha)

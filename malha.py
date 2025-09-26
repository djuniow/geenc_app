import pandas as pd
import sqlite3 as s
import requests
import streamlit as st

def get_token():
    '''
    função para gerar token para consulta nas apis dos correios
    retorna
    status da chamada
    response_token tokem para utilização
    '''
    headers = {"Authorization": "Basic MTQ0OTE6OTUxMzgy"}
    response = requests.post('https://api.correios.com.br/token/v1/autentica', headers=headers)
    status = response.status_code
    response_token = response.json()
    response_token = response_token['token']

    return response_token, status
def carregamento_linhas():

    conn = s.connect('dados_rotas/malha.db')
    df = pd.read_sql_query("SELECT * FROM conexao WHERE `No da Linha` IS NOT NULL", con=conn)
    conn.close()

    df = df.drop_duplicates()
    lista_linhas = list(set(df['No da Linha'].tolist()))

    return lista_linhas
def carregamento_fichas(linha):

    if linha == 'todas':
        query = "SELECT * FROM conexao WHERE 1=1"
        params = []


        df = consulta_banco(query, params)

        lista_fichas = list(set(df['N Ficha'].tolist()))

        return lista_fichas


    query = "SELECT * FROM conexao WHERE 1=1"
    params = []

    if linha:
        query += " AND `No da Linha` = ?"
        params.append(f"{linha}")

    df = consulta_banco(query, params)

    lista_fichas = list(set(df['N Ficha'].tolist()))

    return lista_fichas
def carregamento_unidades():

    df_unidades = pd.read_excel('dados_rotas/base.xlsx',
                                sheet_name='unidades')
    lista_unidades = df_unidades['unidade'].tolist()


    return lista_unidades
def carregamento_transportadora():
    df_unidades = pd.read_excel('dados_rotas/base.xlsx',
                                sheet_name='transportadora')
    lista_transportadora = df_unidades['transportadora'].tolist()
    return lista_transportadora

def carregamentoEnderecos():
    df_unidades = pd.read_excel('dados_rotas/base.xlsx',
                                sheet_name='unidades')
    return df_unidades

def carregamento_ton():
    df_unidades = pd.read_excel('dados_rotas/base.xlsx',
                                sheet_name='ton')
    lista_ton = df_unidades['ton'].tolist()
    return lista_ton
def consulta_banco(query, params):
    try:
        conn = s.connect('dados_rotas/malha.db')
        df = pd.read_sql_query(sql=query, con=conn, params=params)
        conn.close()
        return df
    except Exception as e:
        print(f"Erro na consulta: {e}")
        return pd.DataFrame()
@st.fragment
def busca_banco(linha, unidades, transportadora, tonelagem):
    '''
    Função para buscar dados no banco e retornar um dicionário de DataFrames por unidade ou por ficha.
    '''

    # Caso unidades esteja vazia e haja filtros
    if (linha or transportadora or tonelagem) and not unidades:
        query = "SELECT * FROM conexao WHERE 1=1"
        params = []

        if linha:
            query += " AND `No da Linha` LIKE ?"
            params.append(f"%{linha}%")
        if transportadora:
            query += " AND `Transportada1` LIKE ?"
            params.append(f"%{transportadora}%")
        if tonelagem:
            query += " AND `Descrição Modelo` LIKE ?"
            params.append(f"%{tonelagem}%")

        df_fichas = consulta_banco(query, params)
        fichas = df_fichas['N Ficha'].drop_duplicates()

        dataframes = {}
        for i, ficha in enumerate(fichas):
            df = consulta_banco("SELECT * FROM conexao WHERE `N Ficha` LIKE ?", [f"%{ficha}%"])
            dataframes[i] = df
        return dataframes

    # Caso unidades esteja preenchida
    if isinstance(unidades, str):
        unidades = [unidades]

    dataframes = {}
    for i, unidade in enumerate(unidades):
        query = "SELECT * FROM conexao WHERE 1=1"
        params = []

        if linha:
            query += " AND `No da Linha` LIKE ?"
            params.append(f"%{linha}%")
        if unidade:
            query += " AND `Local1` LIKE ?"
            params.append(f"%{unidade}%")
        if transportadora:
            query += " AND `Transportada1` LIKE ?"
            params.append(f"%{transportadora}%")
        if tonelagem:
            query += " AND `Descrição Modelo` LIKE ?"
            params.append(f"%{tonelagem}%")

        df = consulta_banco(query, params)
        dataframes[i] = df

    # Verifica se há pelo menos duas unidades para cruzar fichas
    if len(dataframes) < 2:
        print("Menos de duas unidades encontradas. Não é possível cruzar fichas.")
        return {}

    df_unidade1 = dataframes[0]
    df_unidade2 = dataframes[1]

    df_ft = pd.merge(
        df_unidade1[['N Ficha']],
        df_unidade2[['N Ficha']],
        how='inner',
        on='N Ficha'
    ).drop_duplicates()

    # Consulta todas as fichas cruzadas
    fichas = df_ft['N Ficha'].tolist()
    if not fichas:
        print("Nenhuma ficha comum encontrada entre as unidades.")
        return {}

    query = f"SELECT * FROM conexao WHERE `N Ficha` IN ({','.join(['?'] * len(fichas))})"
    df_resultado = consulta_banco(query, fichas)

    # Agrupa por ficha
    dataframes = {}
    for i, ficha in enumerate(df_ft['N Ficha']):
        df_ficha = df_resultado[df_resultado['N Ficha'] == ficha]
        df_ficha = df_ficha.reset_index()
        dataframes[i] = df_ficha

    return dataframes
def busca_banco_alterar(linha, ficha):

    # Caso unidades esteja vazia e haja filtros
    query = "SELECT * FROM conexao WHERE 1=1"
    params = []
    if linha:
        query += " AND `No da Linha` LIKE ?"
        params.append(f"%{linha}%")
    if ficha:
        query += " AND `N Ficha` LIKE ?"
        params.append(f"%{ficha}%")


    df_fichas = consulta_banco(query, params)

    return df_fichas

def buscaEndereco(df_ft, df_endereco):
    dfCompleto = pd.merge(df_ft,df_endereco,
                          left_on='Local1',
                          right_on='unidade',
                          how='left')
    return dfCompleto
@st.fragment
def mostra_linhas(data_frames, dataframeEndereco):

    dic_dias = {
        1: 'dom',
        2: 'seg',
        3: 'ter',
        4: 'qua',
        5: 'qui',
        6: 'sex',
        7: 'sab',
    }
    dic_semana = {
        'Domingo': 'dom',
        'Segunda': 'seg',
        'Terça': 'ter',
        'Quarta': 'qua',
        'Quinta': 'qui',
        'Sexta': 'sex',
        'Sábado': 'sab',
    }
    key= 0
    for df_linha in data_frames.values():
        n_linha = df_linha['No da Linha'][0]
        transportadora = df_linha['Transportada1'][0]
        tonelagem = df_linha['Descrição Modelo'][0]
        ficha = df_linha['N Ficha'][0]
        sentido = df_linha['Sentido'][0]
        situacao = df_linha['Recurso 5'][0]
        freq = df_linha[['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado']]
        freq = freq.head(1)
        freq = freq.replace(dic_dias)
        freq = freq.rename(columns=dic_semana)
        freq = freq.fillna('')
        freq = freq.transpose()


        tabela_ft = df_linha[['Local1','Distância','Hora Chegada','Hora Partida','Tempo Serviço','Tempo Percurso']]

        st.write(f"**Linha:** {n_linha} {sentido}")

        st.write(f"**Transportadora:** {transportadora} **Ton:** {tonelagem}  \n  **FT:** {ficha} **Situação:** {situacao}")
        st.pills(label='Dias', options=freq, key=str(df_linha)+str(key))

        html_code = """
        <div style='  width: 100%;'>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    font-size: 15px;
                    line-height: 1.0;
                    padding: 8px 2px; /* aumenta a altura das linhas */
                    text-align: center;
                    word-wrap: break-word;
                }}
            </style>
            {tabela}
        </div>
        """.format(tabela=tabela_ft.to_html(index=False))

        st.markdown(html_code, unsafe_allow_html=True)

        #st.table(tabela_ft)
        key = key +1
        with st.expander(label='Endereços'):
            tabelaEnderecos = df_linha[['Local1']].drop_duplicates()
            dfCompleto = buscaEndereco(df_ft=tabelaEnderecos,
                                       df_endereco=dataframeEndereco)
            for index, row in dfCompleto.iterrows():
                st.write('**'+str(row['Local1'])+'**'+': '+str(row['enderecos']))

        st.divider()
def inserir_ft(linha,sentido, transportadora, ton, frequencia, rota, ficha):
    """
        Insere dados de conexão de rota no banco de dados SQLite.

        Parâmetros:
        - linha (str): Identificador da linha de transporte.
        - transportadora (str): Nome da transportadora responsável.
        - ton (str): Descrição do modelo ou tipo de transporte.
        - frequencia (list): Lista de dias da semana em que a rota ocorre. Ex: ['seg', 'qua', 'sex'].
        - rota (DataFrame): DataFrame contendo os dados da rota, com colunas:
            'Local1', 'Distância', 'Hora Chegada', 'Hora Partida', 'Tempo Serviço', 'Tempo Percurso'.

        A função converte os dias da semana em uma lista de frequência numérica,
        e insere os dados linha por linha na tabela 'conexao' do banco 'malha.db'.
        """

    conn = s.connect('dados_rotas/malha.db')
    freq = [''] * 8
    dias_map = {'dom': 1, 'seg': 2, 'ter': 3, 'qua': 4, 'qui': 5, 'sex': 6, 'sab': 7}
    for dia in frequencia:
        if dia in dias_map:
            freq[dias_map[dia]] = dias_map[dia]

    try:
        for _, row in rota.iterrows():
            query = '''
            INSERT INTO conexao (
                "No da Linha","Sentido","N Ficha", Transportada1, "Descrição Modelo", Domingo, Segunda, terça, Quarta, Quinta, Sexta, Sábado,
                Local1, Distância, "Hora Chegada", "Hora Partida", "Tempo Serviço", "Tempo Percurso"
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            print(freq)
            values = (
                linha,sentido,ficha,transportadora, ton,
                freq[1], freq[2], freq[3], freq[4], freq[5], freq[6], freq[7],
                row['Local1'], row['Distância'], row['Hora Chegada'], row['Hora Partida'],
                row['Tempo Serviço'], row['Tempo Percurso']
            )
            conn.execute(query, values)
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao inserir dados: {e}")
    finally:
        conn.close()
@st.cache_resource
def carga():
    #   carregamento de dados carga
    df_carga = pd.read_csv(r'\\msi75324191\SERVER_GEENC\Relatorios\DADOS\TUDO\CARGA\CARGA_MES.csv', sep=",")
    df_carga['Quantidade'] = df_carga['Quantidade'].str.replace(',00', '')
    df_carga['Quantidade'] = df_carga['Quantidade'].str.replace(',', '0.')
    df_carga['Quantidade'] = df_carga['Quantidade'].astype(float)
    df_carga['CARGA CONVERTIDA'] = "0"
    df_carga['CARGA CONVERTIDA'] = df_carga['CARGA CONVERTIDA'].astype(float).round()
    # df_carga['Controle Viagem'] = df_carga['Controle Viagem'].astype(str)
    # df_carga['Sequencia do CV'] = df_carga['Sequencia do CV'].astype(str)
    df_carga['rastreio'] = df_carga['Controle Viagem'].astype(str) + df_carga['Sequencia do CV'].astype(str)

    #   carregamento de dados apontamentos
    df_apontamentos = pd.read_csv(r'\\msi75324191\SERVER_GEENC\Relatorios\DADOS\TUDO\APONTAMENTOS\APONTAMENTOS_MES.csv',
                                  sep=",")
    # df_apontamentos['Controle Viagem'] = df_apontamentos['Controle Viagem'].astype(str)
    # df_apontamentos['Sequencia do CV'] = df_apontamentos['Sequencia do CV'].astype(str)
    df_apontamentos['rastreio'] = df_apontamentos['Controle Viagem'].astype(str) + df_apontamentos[
        'Sequencia do CV'].astype(str)

    #   ESQUEMA DE CONVERÇÃO DE CARGA

    # CONVERSÃO PARA UNITIZADOR EM DEVOLUÇÃO
    df_carga.loc[(df_carga['Unitizador'] == 'CAF') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 3
    df_carga.loc[(df_carga['Unitizador'] == 'CDL01-BASE') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 17
    df_carga.loc[(df_carga['Unitizador'] == 'CDL01-MANG') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 16
    df_carga.loc[(df_carga['Unitizador'] == 'CDL1MANG G') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 16
    df_carga.loc[(df_carga['Unitizador'] == 'CDL1MANG M') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 16
    df_carga.loc[(df_carga['Unitizador'] == 'CDL1MANG P') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 32
    df_carga.loc[(df_carga['Unitizador'] == 'CDL01-TAMP') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 20
    df_carga.loc[(df_carga['Unitizador'] == 'CDL02-BASE') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 20
    df_carga.loc[(df_carga['Unitizador'] == 'CDL02-MANG') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 35
    df_carga.loc[(df_carga['Unitizador'] == 'CDL02-TAMP') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 25
    df_carga.loc[(df_carga['Unitizador'] == 'CTA01') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 56
    df_carga.loc[(df_carga['Unitizador'] == 'CTA02') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 44
    df_carga.loc[(df_carga['Unitizador'] == 'CTA05') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 84
    df_carga.loc[(df_carga['Unitizador'] == 'CTA06') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 66
    df_carga.loc[(df_carga['Unitizador'] == 'CXTA-TAMP') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 150
    df_carga.loc[(df_carga['Unitizador'] == 'MALA') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 100
    df_carga.loc[(df_carga['Unitizador'] == 'MALA SOLTA') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 100
    df_carga.loc[(df_carga['Unitizador'] == 'PLT') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 15
    df_carga.loc[(df_carga['Unitizador'] == 'SAMBAG') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 20
    df_carga.loc[(df_carga['Unitizador'] == 'CDL1G') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 17
    df_carga.loc[(df_carga['Unitizador'] == 'GRANEL') & (df_carga['Tipo de Serviço'] == 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 55

    # CONVERSÃO PARA O RESTO
    df_carga.loc[(df_carga['Unitizador'] == 'CDL1G') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 1
    df_carga.loc[(df_carga['Unitizador'] == 'CDL1M') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 1
    df_carga.loc[(df_carga['Unitizador'] == 'CDL1P') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 2
    df_carga.loc[(df_carga['Unitizador'] == 'CDL2G') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 2
    df_carga.loc[(df_carga['Unitizador'] == 'CDL2M') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 2
    df_carga.loc[(df_carga['Unitizador'] == 'CDL2P') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 4
    df_carga.loc[(df_carga['Unitizador'] == 'CP01') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 48
    df_carga.loc[(df_carga['Unitizador'] == 'CTA01') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 36
    df_carga.loc[(df_carga['Unitizador'] == 'CTA02') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 18
    df_carga.loc[(df_carga['Unitizador'] == 'CTA05') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 36
    df_carga.loc[(df_carga['Unitizador'] == 'CTA06') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 18
    df_carga.loc[(df_carga['Unitizador'] == 'GRANEL') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 55
    df_carga.loc[(df_carga['Unitizador'] == 'IATA01') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 12
    df_carga.loc[(df_carga['Unitizador'] == 'MALA') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 4
    df_carga.loc[(df_carga['Unitizador'] == 'NPR') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 0.5
    df_carga.loc[(df_carga['Unitizador'] == '3TNPR') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 0.67
    df_carga.loc[(df_carga['Unitizador'] == 'PLT') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 0.5
    df_carga.loc[(df_carga['Unitizador'] == 'PLT EMPILH') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 1
    df_carga.loc[(df_carga['Unitizador'] == 'PLT EMPILH') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 0.5
    df_carga.loc[(df_carga['Unitizador'] == 'PA') & (df_carga['Tipo de Serviço'] != 'UD'), 'CARGA CONVERTIDA'] = \
        df_carga['Quantidade'] / 0.15
    df_carga.loc[df_carga['Tipo de Serviço'] == 'NC', 'CARGA CONVERTIDA'] = 0

    df_carga['CARGA CONVERTIDA'] = round(df_carga['CARGA CONVERTIDA'], 1)

    return df_carga, df_apontamentos

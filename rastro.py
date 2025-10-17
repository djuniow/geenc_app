import requests
import pandas as pd
import streamlit as st
import re

def get_token():
    '''
    Função para retornar o token dos correios
    '''
    headers = {"Authorization": "Basic NTY3MToxNjU3MTYxMA=="}
    response = requests.post('https://api.correios.com.br/token/v1/autentica', headers=headers)
    status = response.status_code
    response_token = response.json()
    response_token = response_token['token']

    return response_token, status

#________________________________________________________________________________________________________________________
def get_rastreamento(objetos, token, evento, resultado):
    '''função que chama na api dos correios e retorna um dicionário
    arg objetos recebe uma lista
    arg token recebe uma string'''

    headers = {"Authorization": f"Bearer {token}"}



    response = requests.get(
        f'https://api.correios.com.br/srorastro/v1/objetos?codigosObjetos={objetos}&resultado={resultado}&evento={evento}&texto=I',
        headers=headers)

    response = response.json()
    return response

def get_rastreamento_data_prazo(objetos):
    token, status_token = get_token()
    '''função que chama na api dos correios e retorna um dicionário
    arg objetos recebe uma lista
    arg token recebe uma string'''

    headers = {"Authorization": f"Bearer {token}"}



    response = requests.get(
        f'https://api.correios.com.br/datamaxima/v1/objetos/{objetos}',
        headers=headers)

    response = response.json()
    resultado = get_dados_prazo(response)
    return resultado
def get_dados_prazo(data):
    def get_values(value):
        return str(value) if value is not None else ""
    print('aaaaaaaaaaaaaaaaa',data)

    dados = {
        'codigo': get_values(data.get('codigo')),
        'servico': get_values(data.get('servico')),
        'cepOrigem': get_values(data.get('cepOrigem')),
        'cepDestino': get_values(data.get('cepDestino')),
        'prazoEntrega': get_values(data.get('prazoEntrega')),
        'dataPostagem': get_values(data.get('dataPostagem')),
        'dataMaxEntrega': get_values(data.get('dataMaxEntrega')),
        'postagemDH': get_values(data.get('postagemDH')),
        'dataUltimoEvento': get_values(data.get('dataUltimoEvento')),
        'codigoUltimoEvento': get_values(data.get('codigoUltimoEvento')),
        'tipoUltimoEvento': get_values(data.get('tipoUltimoEvento')),
        'descricaoUltimoEvento': get_values(data.get('descricaoUltimoEvento')),
        'nuTicket': get_values(data.get('nuTicket')),
        'formaPagamento': get_values(data.get('formaPagamento')),
        'valorPagamento': get_values(data.get('valorPagamento')),
        'nuContrato': get_values(data.get('nuContrato')),
        'nuCartaoPostagem': get_values(data.get('nuCartaoPostagem')),
        'cepDestinoValido': get_values(data.get('cepDestinoValido'))
    }

    return dados

def get_postagem(data):
    token, status_token = get_token()
    print(token)

    def get_values(data):
        return str(data) if data is not None else ""

    response = get_rastreamento(objetos=data, token=token, evento="PO", resultado='T')
    print(response)

    objetos = response.get('objetos', [])
    if not objetos:
        return {}

    objeto = objetos[0]
    tipo_postal = objeto.get('tipoPostal', {})

    dados = {
        'categoria': get_values(tipo_postal.get('categoria')),
        'dtPrevista': get_values(objeto.get('dtPrevista')),
        'largura': get_values(objeto.get('largura')),
        'comprimento': get_values(objeto.get('comprimento')),
        'altura': get_values(objeto.get('altura')),
        'peso': get_values(objeto.get('peso')),
        'eventos': get_values(objeto.get('eventos'))
    }

    return dados


def get_num_obj(num):
    padrao = r'[A-Z]{2}\d{9}[A-Z]{2}'
    result = re.search(padrao, num)
    return result.group(0)

def cor_prazo(prazo):
    '''

    :param prazo:
    :return:
    '''

    if prazo > 4:
        back = '#dff0d8' #verde


    elif prazo <= 4 and prazo > 0:
        back = '#f5e105' #amarelo
    elif prazo == 0:
        back = '#f50505' #vermelho
    elif prazo < 0:
        back = '#050505' #preto
    ajuste = f"""
                <div style="background-color:{back}; padding:15px; border-radius:8px;">
                    <h4 style="color:#3c763d;">{prazo}</h4>
                </div>
            """
    return ajuste























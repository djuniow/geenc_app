import requests
import pandas as pd
import streamlit as st
import re

def get_token():
    '''
    Função para retornar o token dos correios
    '''
    headers = {"Authorization": "Basic MTQ0OTE6OTUxMzgy"}
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


def get_postagem(data):
    token, status_token = get_token()

    def get_values(data):
        try:
            info = str(data)
            print(data)
            return info

        except:
            return "NÂO ENCONTRADO"



    response = get_rastreamento(objetos=data,
                                token=token,
                                evento="PO",
                                resultado='T')


    print(response)
    dados = {
        'categoria':get_values(response['objetos'][0]['tipoPostal']['categoria']),
        'dtPrevista':get_values(response['objetos'][0]['dtPrevista']),
        'largura':get_values(response['objetos'][0]['largura']),
        'comprimento':get_values(response['objetos'][0]['comprimento']),
        'altura':get_values(response['objetos'][0]['altura']),
        'peso':get_values(response['objetos'][0]['peso']),
        'eventos':get_values(response['objetos'][0]['eventos'])


    }

    print(dados)
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























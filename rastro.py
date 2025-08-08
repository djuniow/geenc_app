import requests
import pandas as pd
import streamlit as st


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

    colunas = [
        "codObjeto",
        "tipoPostal_sigla",
        "tipoPostal_descricao",
        "tipoPostal_categoria",
        "tipoPostal_familia",
        "dtPrevista",
        "multiVolume",
        "postagemDH",
        "volume",
        "valorRecebido",
        "contrato",
        "codAdm",
        "cartaoPostagem",
        "largura",
        "comprimento",
        "altura",
        "diametro",
        "peso",
        "formato",
        "celRemetSMS",
        "modalidade",
        "evento_codigo",
        "evento_tipo",
        "evento_dtHrCriado",
        "evento_descricao",
        "evento_estacao",
        "evento_usuario",
        "evento_descCodigo",
        "evento_dtHrGravado",
        "unidade_nome",
        "unidade_codSro",
        "unidade_codMcu",
        "unidade_cidade",
        "unidade_uf",
        "unidade_codse",
        "unidade_se",
        "remetente_nome",
        "remetente_documento",
        "remetente_cep",
        "remetente_logradouro",
        "remetente_complemento",
        "remetente_numero",
        "remetente_bairro",
        "remetente_cidade",
        "remetente_uf",
        "remetente_telefone_tipo",
        "remetente_telefone_ddd",
        "remetente_telefone_numero",
        "destinatario_nome",
        "destinatario_documento",
        "destinatario_cep",
        "destinatario_logradouro",
        "destinatario_complemento",
        "destinatario_numero",
        "destinatario_bairro",
        "destinatario_cidade",
        "destinatario_uf",
        "servico_codigo",
        "servico_ar",
        "servico_tipoAr",
        "servico_mp",
        "servico_vd",
        "servico_eVizinho",
        "servico_fotoFachada",
        "servico_eControlada",
        "servico_eInterativa",
        "servico_eLocker",
        "dgr"
    ]


    response = get_rastreamento(objetos=data,
                                token=token,
                                evento="PO",
                                resultado='T')

    print(response)


    try:
        codObjeto = str(response['objetos'][0].get('codObjeto', ''))

    except:
        codObjeto = ""
    try:
        tipoPostal_sigla = str(response['objetos'][0]['tipoPostal'].get('sigla', ''))
    except:
        tipoPostal_sigla = ""

    try:
        tipoPostal_descricao = str(response['objetos'][0]['tipoPostal'].get('descricao', ''))
    except:
        tipoPostal_descricao = ""

    try:
        tipoPostal_categoria = str(response['objetos'][0]['tipoPostal'].get('categoria', ''))
    except:
        tipoPostal_categoria = ""

    try:
        tipoPostal_familia = str(response['objetos'][0]['tipoPostal'].get('familia', ''))
    except:
        tipoPostal_familia = ""

    try:
        dtPrevista = str(response['objetos'][0].get('dtPrevista', ''))
    except:
        dtPrevista = ""

    try:
        multiVolume = str(response['objetos'][0].get('multiVolume', ''))
    except:
        multiVolume = ""

    try:
        postagemDH = str(response['objetos'][0].get('postagemDH', ''))
    except:
        postagemDH = ""

    try:
        volume = int(response['objetos'][0].get('volume', 0))
    except:
        volume = 0

    try:
        valorRecebido = str(response['objetos'][0].get('valorRecebido', ''))
    except:
        valorRecebido = ""

    try:
        contrato = str(response['objetos'][0].get('contrato', ''))
    except:
        contrato = ""

    try:
        codAdm = str(response['objetos'][0].get('codAdm', ''))
    except:
        codAdm = ""

    try:
        cartaoPostagem = str(response['objetos'][0].get('cartaoPostagem', ''))
    except:
        cartaoPostagem = ""

    try:
        largura = int(response['objetos'][0].get('largura', 0))
    except:
        largura = 0

    try:
        comprimento = int(response['objetos'][0].get('comprimento', 0))
    except:
        comprimento = 0

    try:
        altura = int(response['objetos'][0].get('altura', 0))
    except:
        altura = 0

    try:
        diametro = int(response['objetos'][0].get('diametro', 0))
    except:
        diametro = 0

    try:
        peso = float(response['objetos'][0].get('peso', 0.0))
    except:
        peso = 0.0

    try:
        formato = str(response['objetos'][0].get('formato', ''))
    except:
        formato = ""

    try:
        celRemetSMS = str(response['objetos'][0].get('celRemetSMS', ''))
    except:
        celRemetSMS = ""

    try:
        modalidade = str(response['objetos'][0].get('modalidade', ''))
    except:
        modalidade = ""

    # Evento
    try:
        evento_codigo = str(response['objetos'][0]['eventos'][0].get('codigo', ''))
    except:
        evento_codigo = ""

    try:
        evento_tipo = str(response['objetos'][0]['eventos'][0].get('tipo', ''))
    except:
        evento_tipo = ""

    try:
        evento_dtHrCriado = str(response['objetos'][0]['eventos'][0].get('dtHrCriado', ''))
    except:
        evento_dtHrCriado = ""

    try:
        evento_descricao = str(response['objetos'][0]['eventos'][0].get('descricao', ''))
    except:
        evento_descricao = ""

    try:
        evento_estacao = str(response['objetos'][0]['eventos'][0].get('estacao', ''))
    except:
        evento_estacao = ""

    try:
        evento_usuario = str(response['objetos'][0]['eventos'][0].get('usuario', ''))
    except:
        evento_usuario = ""

    try:
        evento_descCodigo = str(response['objetos'][0]['eventos'][0].get('descCodigo', ''))
    except:
        evento_descCodigo = ""

    try:
        evento_dtHrGravado = str(response['objetos'][0]['eventos'][0].get('dtHrGravado', ''))
    except:
        evento_dtHrGravado = ""

    # Unidade
    try:
        unidade_nome = str(response['objetos'][0]['eventos'][0]['unidade'].get('nome', ''))
    except:
        unidade_nome = ""

    try:
        unidade_codSro = str(response['objetos'][0]['eventos'][0]['unidade'].get('codSro', ''))
    except:
        unidade_codSro = ""

    try:
        unidade_codMcu = str(response['objetos'][0]['eventos'][0]['unidade'].get('codMcu', ''))
    except:
        unidade_codMcu = ""

    try:
        unidade_cidade = str(response['objetos'][0]['eventos'][0]['unidade']['endereco'].get('cidade', ''))
    except:
        unidade_cidade = ""

    try:
        unidade_uf = str(response['objetos'][0]['eventos'][0]['unidade']['endereco'].get('uf', ''))
    except:
        unidade_uf = ""

    try:
        unidade_codse = str(response['objetos'][0]['eventos'][0]['unidade'].get('codse', ''))
    except:
        unidade_codse = ""

    try:
        unidade_se = str(response['objetos'][0]['eventos'][0]['unidade'].get('se', ''))
    except:
        unidade_se = ""

    # Remetente
    try:
        remetente_nome = str(response['objetos'][0]['eventos'][0]['remetente'].get('nome', ''))
    except:
        remetente_nome = ""

    try:
        remetente_documento = str(response['objetos'][0]['eventos'][0]['remetente'].get('documento', ''))
    except:
        remetente_documento = ""

    try:
        remetente_cep = str(response['objetos'][0]['eventos'][0]['remetente']['endereco'].get('cep', ''))
    except:
        remetente_cep = ""

    try:
        remetente_logradouro = str(
            response['objetos'][0]['eventos'][0]['remetente']['endereco'].get('logradouro', ''))
    except:
        remetente_logradouro = ""

    try:
        remetente_complemento = str(
            response['objetos'][0]['eventos'][0]['remetente']['endereco'].get('complemento', ''))
    except:
        remetente_complemento = ""

    try:
        remetente_numero = str(response['objetos'][0]['eventos'][0]['remetente']['endereco'].get('numero', ''))
    except:
        remetente_numero = ""

    try:
        remetente_bairro = str(response['objetos'][0]['eventos'][0]['remetente']['endereco'].get('bairro', ''))
    except:
        remetente_bairro = ""

    try:
        remetente_cidade = str(response['objetos'][0]['eventos'][0]['remetente']['endereco'].get('cidade', ''))
    except:
        remetente_cidade = ""

    try:
        remetente_uf = str(response['objetos'][0]['eventos'][0]['remetente']['endereco'].get('uf', ''))
    except:
        remetente_uf = ""

    try:
        remetente_telefone_tipo = str(
            response['objetos'][0]['eventos'][0]['remetente']['telefones'][0].get('tipo', ''))
    except:
        remetente_telefone_tipo = ""

    try:
        remetente_telefone_ddd = str(
            response['objetos'][0]['eventos'][0]['remetente']['telefones'][0].get('ddd', ''))
    except:
        remetente_telefone_ddd = ""

    try:
        remetente_telefone_numero = str(
            response['objetos'][0]['eventos'][0]['remetente']['telefones'][0].get('numero', ''))
    except:
        remetente_telefone_numero = ""

    # Destinatario
    try:
        destinatario_nome = str(response['objetos'][0]['eventos'][0]['destinatario'].get('nome', ''))
    except:
        destinatario_nome = ""

    try:
        destinatario_documento = str(response['objetos'][0]['eventos'][0]['destinatario'].get('documento', ''))
    except:
        destinatario_documento = ""

    try:
        destinatario_cep = str(response['objetos'][0]['eventos'][0]['destinatario']['endereco'].get('cep', ''))
    except:
        destinatario_cep = ""

    try:
        destinatario_logradouro = str(
            response['objetos'][0]['eventos'][0]['destinatario']['endereco'].get('logradouro', ''))
    except:
        destinatario_logradouro = ""

    try:
        destinatario_complemento = str(
            response['objetos'][0]['eventos'][0]['destinatario']['endereco'].get('complemento', ''))
    except:
        destinatario_complemento = ""

    try:
        destinatario_numero = str(
            response['objetos'][0]['eventos'][0]['destinatario']['endereco'].get('numero', ''))
    except:
        destinatario_numero = ""

    try:
        destinatario_bairro = str(
            response['objetos'][0]['eventos'][0]['destinatario']['endereco'].get('bairro', ''))
    except:
        destinatario_bairro = ""

    try:
        destinatario_cidade = str(
            response['objetos'][0]['eventos'][0]['destinatario']['endereco'].get('cidade', ''))
    except:
        destinatario_cidade = ""

    try:
        destinatario_uf = str(response['objetos'][0]['eventos'][0]['destinatario']['endereco'].get('uf', ''))
    except:
        destinatario_uf = ""

    # Serviço
    try:
        servico_codigo = str(response['objetos'][0]['servico'].get('codigo', ''))
    except:
        servico_codigo = ""

    try:
        servico_ar = str(response['objetos'][0]['servico'].get('ar', ''))
    except:
        servico_ar = ""

    try:
        servico_tipoAr = str(response['objetos'][0]['servico'].get('tipoAr', ''))
    except:
        servico_tipoAr = ""

    try:
        servico_mp = str(response['objetos'][0]['servico'].get('mp', ''))
    except:
        servico_mp = ""

    try:
        servico_vd = str(response['objetos'][0]['servico'].get('vd', ''))
    except:
        servico_vd = ""

    try:
        servico_eVizinho = str(response['objetos'][0]['servico'].get('eVizinho', ''))
    except:
        servico_eVizinho = ""

    try:
        servico_fotoFachada = str(response['objetos'][0]['servico'].get('fotoFachada', ''))
    except:
        servico_fotoFachada = ""

    try:
        servico_eControlada = str(response['objetos'][0]['servico'].get('eControlada', ''))
    except:
        servico_eControlada = ""

    try:
        servico_eInterativa = str(response['objetos'][0]['servico'].get('eInterativa', ''))
    except:
        servico_eInterativa = ""

    try:
        servico_eLocker = str(response['objetos'][0]['servico'].get('eLocker', ''))
    except:
        servico_eLocker = ""

    try:
        dgr = str(response['objetos'][0]['servico'].get('dgr', ''))
    except:
        dgr = ""

    variaveis = [
        codObjeto,
        tipoPostal_sigla,
        tipoPostal_descricao,
        tipoPostal_categoria,
        tipoPostal_familia,
        dtPrevista,
        multiVolume,
        postagemDH,
        volume,
        valorRecebido,
        contrato,
        codAdm,
        cartaoPostagem,
        largura,
        comprimento,
        altura,
        diametro,
        peso,
        formato,
        celRemetSMS,
        modalidade,
        evento_codigo,
        evento_tipo,
        evento_dtHrCriado,
        evento_descricao,
        evento_estacao,
        evento_usuario,
        evento_descCodigo,
        evento_dtHrGravado,
        unidade_nome,
        unidade_codSro,
        unidade_codMcu,
        unidade_cidade,
        unidade_uf,
        unidade_codse,
        unidade_se,
        remetente_nome,
        remetente_documento,
        remetente_cep,
        remetente_logradouro,
        remetente_complemento,
        remetente_numero,
        remetente_bairro,
        remetente_cidade,
        remetente_uf,
        remetente_telefone_tipo,
        remetente_telefone_ddd,
        remetente_telefone_numero,
        destinatario_nome,
        destinatario_documento,
        destinatario_cep,
        destinatario_logradouro,
        destinatario_complemento,
        destinatario_numero,
        destinatario_bairro,
        destinatario_cidade,
        destinatario_uf,
        servico_codigo,
        servico_ar,
        servico_tipoAr,
        servico_mp,
        servico_vd,
        servico_eVizinho,
        servico_fotoFachada,
        servico_eControlada,
        servico_eInterativa,
        servico_eLocker,
        dgr
    ]






    return variaveis




















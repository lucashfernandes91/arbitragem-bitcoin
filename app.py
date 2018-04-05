# CONSULTA COTAÇÃO ATUAL DO BITCOIN NAS EXCHANGES
import requests, json
import time, datetime
import numpy

spread_desejado = 1 # PREENCHER CAMPO APENAS COM O VALOR INTERNO, DESCONSIDERANDO A (%)

while True:
    requisicao = requests.get('http://api.bitvalor.com/v1/ticker.json')
    informacoes = json.loads(requisicao.text)

    # RETORNA O VALOR DO BITCOIN EM CADA EXCHANGE
    exchange = {}
    exchange['bitcoin_to_you'] = informacoes['ticker_24h']['exchanges']['B2U']['last']
    exchange['foxbit'] = informacoes['ticker_24h']['exchanges']['FOX']['last']
    exchange['mercado_bicoin'] = informacoes['ticker_24h']['exchanges']['MBT']['last']
    exchange['negocie_coins'] = informacoes['ticker_24h']['exchanges']['NEG']['last']
    exchange['flowbtc'] = informacoes['ticker_24h']['exchanges']['FLW']['last']

    # ATRIBUI O PREÇO DO BITCOIN ÁS VARIÁVEIS
    b2u = exchange['bitcoin_to_you']
    foxbit = exchange['foxbit']
    mercado_bicoin = exchange['mercado_bicoin']
    negocie_coins = exchange['negocie_coins']
    flowbtc = exchange['flowbtc']

    # CRIA UMA TUPLA COM OS TODOS OS PREÇOS DE BITCOIN
    valores = (b2u, foxbit, mercado_bicoin, negocie_coins, flowbtc)

    # RETORNA O MENOR PREÇO
    menor_preco = numpy.amin(valores)

    # RETORNA O MAIOR PREÇO
    maior_preco = numpy.amax(valores)

    # CALCULA A DIFERENCA ENTRE OS PRECOS (EM PORCENTAGEM)
    spread = (((maior_preco - menor_preco) * 100) / menor_preco)

    # VERIFICA SE O SPREAD DO MERCADO É MAIOR QUE O SOLICITADO
    if spread >= spread_desejado:
        print("## ALERTA!! SPREAD SOLICITADO ATINGIDO ##")
        print("## HORA DO ALARME: {:%d/%m/%Y as %H:%M} ##". format(datetime.datetime.now()))
        print("Spread Atual:  {0:.3f}%" .format(spread))

        # VERIFICA O NOME DE QUAL EXCHANGE O PREÇO ESTÁ MENOR
        for key in exchange:
            if exchange[key] == menor_preco:
                print("MENOR preço em {}: {}".format(key, exchange[key]))

        # VERIFICA O NOME DE QUAL EXCHANGE O PREÇO ESTÁ MAIOR
        for key in exchange:
            if exchange[key] == maior_preco:
                print("MAIOR preço em {}: {}".format(key,exchange[key]))
        break
    time.sleep(60)


# CONSULTA COTAÇÃO ATUAL DO BITCOIN NAS EXCHANGES
import requests, json
import time, datetime
import numpy

spread_desejado = 1 # PREENCHER CAMPO APENAS COM O VALOR INTERNO, DESCONSIDERANDO A (%)

while True:
    requisicao = requests.get('https://api.bitvalor.com/v1/ticker.json')
    informacoes = json.loads(requisicao.text)

    # RETORNA O VALOR DO BITCOIN EM CADA EXCHANGE
    exchange = {}
    exchange['Walltime'] = informacoes['ticker_24h']['exchanges']['WAL']['last']
    exchange['Mercado_Bitcoin'] = informacoes['ticker_24h']['exchanges']['MBT']['last']
    exchange['BitCambio'] = informacoes['ticker_24h']['exchanges']['CAM']['last']
    exchange['BZX'] = informacoes['ticker_24h']['exchanges']['BZX']['last']
    exchange['BitcoinTrade'] = informacoes['ticker_24h']['exchanges']['BTD']['last']

    # ATRIBUI O PREÇO DO BITCOIN ÁS VARIÁVEIS
    walltime = exchange['Walltime']
    mbitcoin = exchange['Mercado_Bitcoin']
    bitcambio = exchange['BitCambio']
    bzx = exchange['BZX']
    bitcointrade = exchange['BitcoinTrade']
    
    # CRIA UMA TUPLA COM OS TODOS OS PREÇOS DE BITCOIN
    valores = (walltime, mbitcoin, bitcambio, bzx, bitcointrade)

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


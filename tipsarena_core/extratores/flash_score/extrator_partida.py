# -*- coding: utf-8 -*-
import time
from datetime import datetime

from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.services import log_service as log, auth_service
from tipsarena_core.utils import hash_utils, string_utils, html_utils
from tipsarena_core.models.item_extracao import ItemExtracao
from tipsarena_core.enums.enum_aposta import MERCADO

CASAS_DECIMAIS = 3


def extrairHtmlPartidas(url: str):
  try:
    CSS_LINK_LISTAR_MAIS = "a.event__more"
    CSS_LOADING = ".loadingOverlay"
    CSS_TABELA_PARTIDAS = "#live-table"

    navegador_web.navegar(url)
    browser = navegador_web.obterNavegadorWeb()

    while len(browser.find_elements_by_css_selector(CSS_LINK_LISTAR_MAIS)) > 0:
      linkListarMais = browser.find_elements_by_css_selector(CSS_LINK_LISTAR_MAIS)[0]
      navegador_web.fecharPopupCookies()
      linkListarMais.click()
      navegador_web.aguardarCarregamentoPagina(CSS_LOADING)

    htmlPartidas = navegador_web.obterElementoAposCarregamento(CSS_TABELA_PARTIDAS)

    TIPO_EXTRACAO = "PARTIDAS"
    urlHash = hash_utils.gerarHash(url)
    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    metadados = {
      "url": url,
      "url_hash": urlHash,
      "tipo_extracao": TIPO_EXTRACAO
    }

    htmlFinal = html_utils.incluirMetadadosHtml(
      f"<body>{htmlPartidas.get_attribute('outerHTML')}>/body>",
      metadados)

    return ItemExtracao(
      {
        "id": id,
        "url": url,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"ptd-edc-{urlHash.lower()}.html"
      })

  except Exception as e:
    log.ERRO(f"Não foi possível extrair HTML de partidas da url {url}.", e.args)
    return None


def extrairHtmlPartidasDia(indiceDia=0):
  CSS_LOADING = ".loadingOverlay"
  CSS_LINK_YESTERDAY = "div.calendar__direction--yesterday"
  CSS_LINK_TOMORROW = "div.calendar__direction--tomorrow"

  CSS_SELETOR_DATA = "div.calendar__datepicker"
  CSS_LISTA_DATAS = "div.calendar__datepicker--dates div.day"
  CSS_TABELA_PARTIDAS = "#live-table"

  try:
    url = navegador_web.URL_BASE
    navegador_web.navegar(url)
    browser = navegador_web.obterNavegadorWeb()

    botaoExibirCalendario = browser.find_element_by_css_selector(CSS_SELETOR_DATA)
    botaoExibirCalendario.click()
    listaDatas = browser.find_elements_by_css_selector(CSS_LISTA_DATAS)
    botaoExibirCalendario.click()

    posicaoMeioLista = int(len(listaDatas) / 2)

    navegador_web.aguardarCarregamentoPagina(CSS_LOADING)

    # avançar dias
    if indiceDia > 0:
      posicaoUltimaData = posicaoMeioLista + indiceDia
      for i in range(posicaoMeioLista + 1, posicaoUltimaData + 1):
        botaoIrProximaData = browser.find_element_by_css_selector(CSS_LINK_TOMORROW)
        botaoIrProximaData.click()
        navegador_web.aguardarCarregamentoPagina(CSS_LOADING)

    # retroceder dias
    if indiceDia < 0:
      posicaoPrimeiraData = posicaoMeioLista + indiceDia
      for i in range(posicaoPrimeiraData, posicaoMeioLista):
        botaoIrProximaData = browser.find_element_by_css_selector(CSS_LINK_YESTERDAY)
        botaoIrProximaData.click()
        navegador_web.aguardarCarregamentoPagina(CSS_LOADING)

    expandirPartidasCompeticao(browser)
    htmlPartidas = browser.find_element_by_css_selector(CSS_TABELA_PARTIDAS)

    TIPO_EXTRACAO = "PARTIDAS_DIA"
    urlHash = hash_utils.gerarHash(url)
    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    metadados = {
      "url": url,
      "url_hash": urlHash,
      "tipo_extracao": TIPO_EXTRACAO
    }

    htmlFinal = html_utils.incluirMetadadosHtml(
      f"<body>{htmlPartidas.get_attribute('outerHTML')}</body>",
      metadados)

    return ItemExtracao(
      {
        "id": id,
        "url": url,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"{id.lower()}.html"
      })

  except Exception as e:
    log.ERRO("Não foi possível extrair HTML partidas do dia.", e.args)
    navegador_web.capturarTela()

    return None


def expandirPartidasCompeticao(browser):
  try:
    CSS_LINK_EXPAND_LEAGUE = "div.event__expander.expand"
    linksExpandirPartidasCompeticao = browser.find_elements_by_css_selector(
      CSS_LINK_EXPAND_LEAGUE)

    for link in linksExpandirPartidasCompeticao:
      try:
        link.click()
      except:
        navegador_web.fecharPopupCookies()
        time.sleep(1)
        link.click()

  except Exception as e:
    log.ERRO("Não foi possível exibir todas as partidas ocultas.", e.args)


def extrairHtmlPartida(urlPartida: str) -> ItemExtracao:
  try:
    CSS_DADOS_PARTIDA = "body"
    CSS_VERIFICAR_CARREGAMENTO = "#detail"

    navegador_web.navegar(urlPartida)

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlDadosPartida = navegador_web.obterElementoAposCarregamento(CSS_DADOS_PARTIDA)

    TIPO_EXTRACAO = "PARTIDA"
    urlHash = hash_utils.gerarHash(urlPartida)
    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    metadados = {
      "url": urlPartida,
      "url_hash": urlHash,
      "tipo_extracao": TIPO_EXTRACAO
    }

    htmlFinal = html_utils.incluirMetadadosHtml(htmlDadosPartida.get_attribute("outerHTML"), metadados)

    return ItemExtracao(
      {
        "id": id,
        "url": urlPartida,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"ptd-{urlHash.lower()}.html"
      })

  except Exception as e:
    log.ERRO(f"Não foi possível extrair HTML dados partida: {urlPartida}", e.args)
    return None


def extrairHtmlTimelinePartida(urlPartida: str):
  try:
    CSS_DADOS_TIMELINE = "body"
    CSS_VERIFICAR_CARREGAMENTO = "div[class^=verticalSections]"

    urlTimeline = f"{navegador_web.URL_BASE}{urlPartida}#resumo-de-jogo/estatisticas-de-jogo/"
    navegador_web.navegar(urlTimeline)

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlTimeline = navegador_web.obterElementoAposCarregamento(CSS_DADOS_TIMELINE)

    TIPO_EXTRACAO = "PARTIDA_TIMELINE"
    urlHash = hash_utils.gerarHash(urlPartida)
    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    metadados = {
      "url": urlPartida,
      "url_hash": urlHash,
      "tipo_extracao": TIPO_EXTRACAO
    }

    htmlFinal = html_utils.incluirMetadadosHtml(str(htmlTimeline), metadados)

    return ItemExtracao(
      {
        "id": id,
        "url": urlPartida,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"{id.lower()}.html"
      })

  except Exception as e:
    log.ERRO("Não foi possível obter timeline de eventos da partida.", e.args)
    return None
  finally:
    navegador_web.finalizarNavegadorWeb()


def extrairHtmlEstatisticasPartida(urlPartida: str):
  try:
    CSS_DADOS_ESTATISTICAS = "body"
    CSS_VERIFICAR_CARREGAMENTO = "div[class^=statRow]"

    urlEstatisticas = f"{urlPartida}#resumo-de-jogo/estatisticas-de-jogo/"
    navegador_web.navegar(urlEstatisticas)

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlEstatisticas = navegador_web.obterElementoAposCarregamento(CSS_DADOS_ESTATISTICAS)

    TIPO_EXTRACAO = "PARTIDA_ESTATISTICAS"
    urlHash = hash_utils.gerarHash(urlPartida)
    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    metadados = {
      "url": urlPartida,
      "url_hash": urlHash,
      "tipo_extracao": TIPO_EXTRACAO
    }

    htmlFinal = html_utils.incluirMetadadosHtml(htmlEstatisticas.get_attribute("outerHTML"), metadados)

    return ItemExtracao(
      {
        "id": id,
        "url": urlPartida,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"ptd-stat-{urlHash.lower()}.html"
      })


  except Exception as e:
    log.ERRO("Não foi possível extrair HTML estatísticas da partida.", e.args)
    return None


def extrairHtmlUltimasPartidasEquipes(urlPartida: str):
  try:
    DADOS_H2H = "body"
    CSS_VERIFICAR_CARREGAMENTO = "div[class^=h2h]"

    urlHeadToHead = f"{urlPartida}#h2h/"
    navegador_web.navegar(urlHeadToHead)

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlHeadToHead = navegador_web.obterElementoAposCarregamento(DADOS_H2H)

    TIPO_EXTRACAO = "PARTIDA_H2H"
    urlHash = hash_utils.gerarHash(urlPartida)
    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    metadados = {
      "url": urlPartida,
      "url_hash": urlHash,
      "tipo_extracao": TIPO_EXTRACAO
    }
    htmlFinal = html_utils.incluirMetadadosHtml(htmlHeadToHead.get_attribute("outerHTML"), metadados)

    return ItemExtracao(
      {
        "id": id,
        "url": urlPartida,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"ptd-h2h-{urlHash.lower()}.html"
      })

  except Exception as e:
    log.ERRO("Não foi possível extrair HTML últimas partidas das equipes.", e.args)
    return None


def extrairHtmlOddsPartida(urlPartida: str, mercado: MERCADO):
  try:
    urlOdds = f"{urlPartida}#comparacao-de-odds/"
    tipoExtracao = f"PARTIDA_ODDS_{mercado.name}"
    prefixoArquivo = "ptd-odd-rst"

    if mercado == MERCADO.DNB:
      urlOdds = f"{urlPartida}#comparacao-de-odds/home-away/"
      prefixoArquivo = "ptd-odd-dnb"

    if mercado == MERCADO.DUPLA_CHANCE:
      urlOdds = f"{urlPartida}#comparacao-de-odds/double-chance/"
      prefixoArquivo = "ptd-odd-dc"

    if mercado == MERCADO.IMPAR_PAR:
      urlOdds = f"{urlPartida}#comparacao-de-odds/odd-even/"
      prefixoArquivo = "ptd-odd-ip"

    if mercado == MERCADO.AMBOS_MARCAM:
      urlOdds = f"{urlPartida}#comparacao-de-odds/ambos-marcam/"
      prefixoArquivo = "ptd-odd-btts"

    if mercado == MERCADO.PLACAR_EXATO:
      urlOdds = f"{urlPartida}#comparacao-de-odds/correct-score/"
      prefixoArquivo = "ptd-odd-plc"

    if mercado == MERCADO.UNDER_OVER:
      urlOdds = f"{urlPartida}#comparacao-de-odds/acima-abaixo/"
      prefixoArquivo = "ptd-odd-uo"

    return extrairHtmlOdds(urlOdds, tipoExtracao, prefixoArquivo)
  except Exception as e:
    log.ERRO(f"Não foi possível extrair HTML odds de {mercado.name} da partida.", e.args)
    return None


def extrairHtmlOdds(urlOdds: str, tipoExtracao: str, prefixoArquivo: str):
  try:
    CSS_DADOS_ODDS = "body"
    CSS_VERIFICAR_CARREGAMENTO = "#detail > div > div.subTabs"

    navegador_web.navegar(urlOdds)

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlOdds = navegador_web.obterElementoAposCarregamento(CSS_DADOS_ODDS)

    urlHash = hash_utils.gerarHash(urlOdds)
    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    metadados = {
      "url": urlOdds,
      "url_hash": urlHash,
      "tipo_extracao": tipoExtracao
    }

    htmlFinal = html_utils.incluirMetadadosHtml(htmlOdds.get_attribute("outerHTML"), metadados)

    return ItemExtracao(
      {
        "id": id,
        "url": urlOdds,
        "urlHash": urlHash,
        "tipo": tipoExtracao,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"{prefixoArquivo}-{urlHash.lower()}.html"
      })

  except Exception as e:
    log.ERRO(f"Não foi possível extrair HTML odds da partida. [{urlOdds}][{tipoExtracao}]", e.args)
    return None

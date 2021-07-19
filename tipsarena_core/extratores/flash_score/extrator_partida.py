# -*- coding: utf-8 -*-
import time
from datetime import datetime

from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.services import log_service as log
from tipsarena_core.utils import hash_utils, string_utils
from tipsarena_core.utils.html_utils import DadosExtracao

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

    return DadosExtracao(hash_utils.gerarHash(url),
                       "PARTIDAS",
                         url,
                         string_utils.limparString(
                         htmlPartidas.get_attribute("outerHTML"))
                         )

  except Exception as e:
    log.ERRO(f"Não foi possível extrair HTML de partidas da url {url}.", e.args)
    return None


def extrairHtmlPartidasEdicaoCompeticao(urlEdicao: str, finalizadas=True):
  try:
    situacaoPartidas = "resultados/" if finalizadas else "calendario/"
    urlPartidas = f"{navegador_web.URL_BASE}{urlEdicao}{situacaoPartidas}"

    return extrairHtmlPartidas(urlPartidas)

  except Exception as e:
    log.ERRO(f"Não foi possível extrair HTML lista de IDS de partidas da edição da competicão {urlEdicao}.", e.args)
    return None


def extrairHtmlPartidasDia(indiceDia=0):
  CSS_LOADING = ".loadingOverlay"
  CSS_LINK_YESTERDAY = "div.calendar__direction--yesterday"
  CSS_LINK_TOMORROW = "div.calendar__direction--tomorrow"

  CSS_SELETOR_DATA = "div.calendar__datepicker"
  CSS_LISTA_DATAS = "div.calendar__datepicker--dates div.day"
  CSS_TABELA_PARTIDAS = "#live-table"

  try:
    navegador_web.navegar(navegador_web.URL_BASE)
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
    htmlTabelaPartidas = browser.find_element_by_css_selector(CSS_TABELA_PARTIDAS)

    return DadosExtracao(hash_utils.gerarHash(navegador_web.URL_BASE),
                       "PARTIDAS",
                         navegador_web.URL_BASE,
                         string_utils.limparString(
                         htmlTabelaPartidas.get_attribute("outerHTML"))
                         )

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


def extrairHtmlPartida(urlPartida: str):
  try:
    CSS_DADOS_PARTIDA = "body"
    CSS_VERIFICAR_CARREGAMENTO = "#detail"

    navegador_web.navegar(navegador_web.URL_BASE + urlPartida)

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlDadosPartida = navegador_web.obterElementoAposCarregamento(CSS_DADOS_PARTIDA)

    return DadosExtracao(hash_utils.gerarHash(urlPartida),
                       "PARTIDA",
                         urlPartida,
                         string_utils.limparString(
                         htmlDadosPartida.get_attribute("outerHTML"))
                         )

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

    return DadosExtracao(hash_utils.gerarHash(urlTimeline),
                       "PARTIDA_TIMELINE",
                         urlTimeline,
                         string_utils.limparString(
                         htmlTimeline.get_attribute("outerHTML"))
                         )

  except Exception as e:
    log.ERRO("Não foi possível obter timeline de eventos da partida.", e.args)
    return None


def extrairHtmlEstatisticasPartida(urlPartida: str):
  try:
    CSS_DADOS_ESTATISTICAS = "body"
    CSS_VERIFICAR_CARREGAMENTO = "div[class^=statRow]"

    urlEstatisticas = f"{navegador_web.URL_BASE}{urlPartida}#resumo-de-jogo/estatisticas-de-jogo/"
    navegador_web.navegar(urlEstatisticas)

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlEstatisticas = navegador_web.obterElementoAposCarregamento(CSS_DADOS_ESTATISTICAS)

    return DadosExtracao(hash_utils.gerarHash(urlEstatisticas),
                       "PARTIDA_TIMELINE",
                         urlEstatisticas,
                         string_utils.limparString(
                         htmlEstatisticas.get_attribute("outerHTML"))
                         )


  except Exception as e:
    log.ERRO("Não foi possível extrair HTML estatísticas da partida.", e.args)
    return None


def extrairHtmlUltimasPartidasEquipes(urlPartida: str):
  try:
    DADOS_H2H = "body"
    CSS_VERIFICAR_CARREGAMENTO = "div[class^=h2h]"

    urlHeadToHead = f"{navegador_web.URL_BASE}{urlPartida}#h2h/"
    navegador_web.navegar(urlHeadToHead)

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlHeadToHead = navegador_web.obterElementoAposCarregamento(DADOS_H2H)

    return DadosExtracao(hash_utils.gerarHash(urlHeadToHead),
                       "PARTIDA_H2H",
                         urlHeadToHead,
                         string_utils.limparString(
                         htmlHeadToHead.get_attribute("outerHTML"))
                         )

  except Exception as e:
    log.ERRO("Não foi possível extrair HTML últimas partidas das equipes.", e.args)
    return None


def extrairHtmlOddsPartida(urlPartida: str):
  try:
    CSS_DADOS_ODDS = "body"
    CSS_VERIFICAR_CARREGAMENTO = "#detail > div > div.subTabs"

    urlOdds = f"{navegador_web.URL_BASE}{urlPartida}#comparacao-de-odds/"
    navegador_web.navegar(urlOdds)

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlOdds = navegador_web.obterElementoAposCarregamento(CSS_DADOS_ODDS)

    return DadosExtracao(hash_utils.gerarHash(urlOdds),
                       "PARTIDA_ODDS",
                         urlOdds,
                         string_utils.limparString(
                         htmlOdds.get_attribute("outerHTML"))
                         )

  except Exception as e:
    log.ERRO("Não foi possível extrair HTML últimas partidas das equipes.", e.args)
    return None



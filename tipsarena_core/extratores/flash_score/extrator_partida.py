# -*- coding: utf-8 -*-
import time

from datetime import datetime

from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.models.Partida import Partida
from tipsarena_core.utils import hash_utils, string_utils, datetime_utils, html_utils
from tipsarena_core.utils.html_utils import DadosBrutos
from tipsarena_core.services import log_service as log

CASAS_DECIMAIS = 3


def extrairHtmlPartidas(url: str):
  try:
    CSS_LINK_LISTAR_MAIS = "a.event__more"
    CSS_LOADING = ".loadingOverlay"
    CSS_TABELA_PARTIDAS = "#live-table"

    browser = navegador_web.obterNavegadorWeb()
    browser.get(url)
    navegador_web.fecharPopupCookies()

    while len(browser.find_elements_by_css_selector(CSS_LINK_LISTAR_MAIS)) > 0:
      linkListarMais = browser.find_elements_by_css_selector(CSS_LINK_LISTAR_MAIS)[0]
      navegador_web.fecharPopupCookies()
      linkListarMais.click()
      navegador_web.aguardarCarregamentoPagina(CSS_LOADING)

    htmlPartidas = navegador_web.obterElementoAposCarregamento(CSS_TABELA_PARTIDAS)

    return DadosBrutos(hash_utils.gerarHash(url),
                       "PARTIDAS",
                       url,
                       string_utils.limparString(
                         htmlPartidas.get_attribute("innerHTML"))
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
    browser = navegador_web.obterNavegadorWeb()
    browser.get(navegador_web.URL_BASE)
    navegador_web.fecharPopupCookies()

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

    return DadosBrutos(hash_utils.gerarHash(navegador_web.URL_BASE),
                       "PARTIDAS",
                       navegador_web.URL_BASE,
                       string_utils.limparString(
                         htmlTabelaPartidas.get_attribute("innerHTML"))
                       )

  except Exception as e:
    log.ERRO("Não foi possível extrair HTML partidas do dia.", e.args)
    browser.save_screenshot(f"error_screenshot_{datetime.strftime('%Y%m%d')}.png")

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


def extrairHtmlPartida(urlPartida, extrairTimeline=True, extrairOdds=True, extrairStats=True,
                       extrairUltimasPartidas=True):
  try:
    CSS_CONTAINER_DADOS_PARTIDA = "#datail"

    browser = navegador_web.obterNavegadorWeb()
    browser.get(navegador_web.URL_BASE + urlPartida)

    htmlDadosPartida = navegador_web.obterElementoAposCarregamento(CSS_CONTAINER_DADOS_PARTIDA)

    return DadosBrutos(hash_utils.gerarHash(urlPartida),
                       "PARTIDA",
                       urlPartida,
                       string_utils.limparString(
                         htmlDadosPartida.get_attribute("innerHTML"))
                       )

  except Exception as e:
    log.ERRO(f"Não foi possível extrair HTML dados partida: {urlPartida}", e.args)
    return None


def extrairHtmlEventosPartida(urlPartida: str):
  pass


def verificarInformacoesDisponiveis(htmlLinks):
  try:
    informacoes = {
      "resumo-de-jogo": False,
      "resumo-de-jogo/estatisticas-de-jogo": False,
      "resumo-de-jogo/equipes": False,
      "resumo-de-jogo/comentarios-ao-vivo": False,
      "comparacao-de-odds": False,
      "h2h": False,
      "videos": False,
      "imagens-da-partida": False,
      "noticias": False,
      "classificacao": False
    }

    for href in htmlLinks:
      href = href.get_attribute("href")
      informacoes[href.split("#")[1]] = True

    return informacoes
  except Exception as e:
    log.ERRO("Não foi possível verificar as informações disponíveis para a partida.", e.args)
    return informacoes


def extrairHtmlTimelinePartida(urlPartida: str):
  try:
    CSS_DADOS_TIMELINE = "div[class^=verticalSections]"
    browser = navegador_web.obterNavegadorWeb()
    urlTimeline = f"{navegador_web.URL_BASE}{urlPartida}#resumo-de-jogo/estatisticas-de-jogo/"
    browser.get(urlTimeline)

    htmlTimeline = navegador_web.obterElementoAposCarregamento(CSS_DADOS_TIMELINE)

    return DadosBrutos(hash_utils.gerarHash(urlTimeline),
                       "PARTIDA_TIMELINE",
                       urlTimeline,
                       string_utils.limparString(
                         htmlTimeline.get_attribute("innerHTML"))
                       )

  except Exception as e:
    log.ERRO("Não foi possível obter timeline de eventos da partida.", e.args)
    return None


def extrairHtmlEstatisticasPartida(urlPartida: str):
  try:
    CSS_LINHAS_ESTATISTICAS = "div[class^=statRow]"

    urlEstatisticas = f"{navegador_web.URL_BASE}{urlPartida}#resumo-de-jogo/estatisticas-de-jogo/"
    browser = navegador_web.obterNavegadorWeb()
    browser.get(urlEstatisticas)

    htmlEstatisticas = navegador_web.obterElementoAposCarregamento(CSS_LINHAS_ESTATISTICAS)

    return DadosBrutos(hash_utils.gerarHash(urlEstatisticas),
                       "PARTIDA_TIMELINE",
                       urlEstatisticas,
                       string_utils.limparString(
                         htmlEstatisticas.get_attribute("innerHTML"))
                       )


  except Exception as e:
    log.ERRO("Não foi possível extrair HTML estatísticas da partida.", e.args)
    return None


def extrairHtmlUltimasPartidasEquipes(urlPartida: str):
  try:
    CSS_DADOS_H2H = "div[class^=h2h]"

    urlHeadToHead = f"{navegador_web.URL_BASE}{urlPartida}#h2h/"
    browser = navegador_web.obterNavegadorWeb()
    browser.get(urlHeadToHead)

    htmlHeadToHead = navegador_web.obterElementoAposCarregamento(CSS_DADOS_H2H)

    return DadosBrutos(hash_utils.gerarHash(urlHeadToHead),
                       "PARTIDA_H2H",
                       urlHeadToHead,
                       string_utils.limparString(
                         htmlHeadToHead.get_attribute("innerHTML"))
                       )

  except Exception as e:
    log.ERRO("Não foi possível extrair HTML últimas partidas das equipes.", e.args)
    return None


def extrairHtmlOddsPartida(urlPartida: str):
  try:
    CSS_DADOS_ODDS = "#detail"
    CSS_VERIFICAR_CARREGAMENTO = "#detail > div > div.subTabs"

    urlOdds = f"{navegador_web.URL_BASE}{urlPartida}#comparacao-de-odds/"
    browser = navegador_web.obterNavegadorWeb()
    browser.get(urlOdds)

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlOdds = navegador_web.obterElementoAposCarregamento(CSS_DADOS_ODDS)

    return DadosBrutos(hash_utils.gerarHash(urlOdds),
                       "PARTIDA_ODDS",
                       urlOdds,
                       string_utils.limparString(
                         htmlOdds.get_attribute("innerHTML"))
                       )

  except Exception as e:
    log.ERRO("Não foi possível extrair HTML últimas partidas das equipes.", e.args)
    return None



def normalizarDescricaoStatus(status: str):
  if status == "":
    statusPartida = Partida.Status.AGENDADO.name

  elif status.find("1º tempo") != -1 or status.find("1st Half") != -1:
    statusPartida = Partida.Status.PRIMEIRO_TEMPO.name

  elif status.find("2º tempo") != -1 or status.find("2nd Half") != -1:
    statusPartida = Partida.Status.SEGUNDO_TEMPO.name

  elif status == "Adiado" or status == "Postponed":
    statusPartida = Partida.Status.ADIADO.name

  elif status == "Após Pênaltis" or status == "After Penalties":
    statusPartida = Partida.Status.FINALIZADO.name

  elif status == "Após Prorrogação" or status == "After Extra Time":
    statusPartida = Partida.Status.FINALIZADO.name

  elif status == "Intervalo" or status == "Half Time" or status == "Break Time":
    statusPartida = Partida.Status.INTERVALO.name

  elif status == "Atribuído" or status == "Awarded":
    statusPartida = Partida.Status.RESULTADO_NAO_DISPONIVEL.name

  elif status == "Abandonado" or status == "Abandoned":
    statusPartida = Partida.Status.ABANDONADO.name

  elif status == "Cancelado" or status == "Cancelled":
    statusPartida = Partida.Status.CANCELADO.name

  elif status == "SRF - Só resultado final." or status == "FRO - Final result only.":
    statusPartida = Partida.Status.RESULTADO_NAO_DISPONIVEL.name

  elif status == "SRF " or status == "FRO ":
    statusPartida = Partida.Status.RESULTADO_NAO_DISPONIVEL.name

  elif status == "Encerrado" or status == "Finished":
    statusPartida = Partida.Status.FINALIZADO.name

  elif status == "Walkover":
    statusPartida = Partida.Status.W_O.name

  elif status.find("Walkover") != -1:
    statusPartida = Partida.Status.W_O.name

  elif status == "Ao Vivo" or status == "Live":
    statusPartida = Partida.Status.EM_ANDAMENTO.name

  elif status == "Extra Time":
    statusPartida = Partida.Status.EM_ANDAMENTO.name

  elif status == "Penalties":
    statusPartida = "PENALTIES"

  else:
    log.ALERTA(f"Status '{status}' não mapeado.")
    statusPartida = status

  return statusPartida


def normalizarDescricaoEstatistica(descricao: str):
  novaDescricao = descricao
  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Goal Attempts":
    novaDescricao = "Tentativa de Gols"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Shots on Goal":
    novaDescricao = "Chutes a gol"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  if descricao == "Ball Possession":
    novaDescricao = "Posse de Bola"

  else:
    log.ALERTA(f"Descricao estatística '{descricao}' nao mapeada.")

  return novaDescricao

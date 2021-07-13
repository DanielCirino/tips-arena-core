# -*- coding: utf-8 -*-
import time

from datetime import datetime

from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.models.Partida import Partida
from tipsarena_core.utils import hash_utils, string_utils, datetime_utils, html_utils
from tipsarena_core.utils.html_utils import DadosBrutos
from tipsarena_core.enums.enum_partida import TIPO_MERCADO
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


def extrairListaPartidasHtml():
  try:
    browser = navegador_web.obterNavegadorWeb()
    listaPartidas = []
    CSS_LOADING = ".loadingOverlay"
    CSS_LINK_EXPAND_LEAGUE = "div.event__expander.expand"
    CSS_LINHA_PARTIDA = "div[id^=g_1_]"

    navegador_web.aguardarCarregamentoPagina(CSS_LOADING)

    linksExpandirPartidasCompeticao = browser.find_elements_by_css_selector(
      CSS_LINK_EXPAND_LEAGUE)

    for link in linksExpandirPartidasCompeticao:
      navegador_web.fecharPopupCookies()
      try:
        time.sleep(0.5)
        link.click()
      except Exception as e:
        try:
          link.click()
        except Exception as e:
          pass

    partidas = browser.find_elements_by_css_selector(
      CSS_LINHA_PARTIDA)

    for partida in partidas:
      id = partida.get_attribute("id").split("_")[2]
      listaPartidas.append("/jogo/" + id + "/")

    return listaPartidas
  except Exception as e:
    log.ERRO("Não foi possível obter lista de Id's de partidas das partidas.", e.args)
    return []


def obterDadosPartida(urlPartida, extrairTimeline=True, extrairOdds=True, extrairStats=True,
                      extrairUltimasPartidas=True):
  try:
    browser = navegador_web.obterNavegadorWeb()
    # urlPartida = urlPartida.replace('jogo', 'match')

    CSS_LOADING = "#preload-all"
    CSS_CABECALHO_PARTIDA = "div.tournamentHeaderDescription"
    CSS_DADOS_MANDANTE = "[class^=home] div div a"
    CSS_DADOS_VISITANTE = "[class^=away] div div a"
    CSS_PLACAR_PARTIDA = "div[class^=score]"
    CSS_DATA_PARTIDA = "div[class^=startTime_] div"
    CSS_STATUS_PARTIDA = "[class^=detailStatus]"
    CSS_INFO_PARTIDA = "div[class^=info]"
    CSS_LINKS_INFOS_PARTIDA = "div.tabs__group a.tabs__tab"

    partida = {
      "url": urlPartida.replace(navegador_web.URL_BASE, ""),
      "timeline": [],
      "estatisticas": [],
      "headToHead": {},
      "odds": {}
    }

    browser.get(navegador_web.URL_BASE + urlPartida)

    cabecalhoPartida = navegador_web.obterElementoAposCarregamento(CSS_CABECALHO_PARTIDA)
    dadosMandante = browser.find_element_by_css_selector(
      CSS_DADOS_MANDANTE)
    dadosVisitante = browser.find_element_by_css_selector(
      CSS_DADOS_VISITANTE)
    placarPartida = browser.find_elements_by_css_selector(
      CSS_PLACAR_PARTIDA)

    dataPartida = browser.find_element_by_css_selector(
      CSS_DATA_PARTIDA).text

    partida["dataHora"] = datetime_utils.converterHoraLocalToUtc(datetime.strptime(
      dataPartida, "%d.%m.%Y %H:%M"))

    htmlStatusPartida = browser.find_elements_by_css_selector(
      CSS_STATUS_PARTIDA)
    statusPartida = htmlStatusPartida[1].text.split("-")
    partida["status"] = normalizarDescricaoStatus(
      statusPartida[0])

    if len(statusPartida) > 1:
      partida["minutos"] = statusPartida[1]
    else:
      partida["minutos"] = ""

    informacoesPartida = browser.find_elements_by_css_selector(
      CSS_INFO_PARTIDA)

    if len(informacoesPartida) == 1:
      partida["info"] = informacoesPartida[0].text

    faseCompeticao = cabecalhoPartida.text.split("-")
    partida["faseCompeticao"] = "-".join(faseCompeticao[1:])
    partida["faseCompeticao"] = string_utils.limparString(
      partida["faseCompeticao"])

    urlCompeticao = cabecalhoPartida.find_element_by_css_selector("span a").get_attribute("href")
    urlEquipeMandante = dadosMandante.get_attribute("href")
    urlEquipeVisitante = dadosVisitante.get_attribute("href")

    competicao = {"url": urlCompeticao,
                  "nome": cabecalhoPartida.text.split(":")[1].split(" - ")[0]
                  }

    equipeMandante = {"url": urlEquipeMandante, "nome": dadosMandante.text}
    equipeVisitante = {"url": urlEquipeVisitante, "nome": dadosVisitante.text}

    # competicao = extrator_competicao.obterDadosCompeticao(urlCompeticao)

    # equipeMandante = extrator_equipe.extrairHtmlEquipe(urlEquipeMandante)
    # equipeVisitante = extrator_equipe.extrairHtmlEquipe(urlEquipeVisitante)

    placarMandantePrimeiroTempo = browser.find_elements_by_css_selector(
      ".p1_home")
    placarMandanteSegundoTempo = browser.find_elements_by_css_selector(
      ".p2_home")
    placarMandanteProrrogacao = browser.find_elements_by_css_selector(
      ".p3_home")
    placarMandantePenalties = browser.find_elements_by_css_selector(
      ".p3_home")

    placarVisitantePrimeiroTempo = browser.find_elements_by_css_selector(
      ".p1_away")
    placarVisitanteSegundoTempo = browser.find_elements_by_css_selector(
      ".p2_away")
    placarVisitanteProrrogacao = browser.find_elements_by_css_selector(
      ".p3_away")
    placarVisitantePenalties = browser.find_elements_by_css_selector(
      ".p3_away")

    if len(placarPartida) == 0:
      placarPartida = ["", ""]
    elif len(placarPartida) == 2:
      placarPartida = [placarPartida[0].text, placarPartida[1].text]

    elif len(placarPartida) == 4:
      placarPartida = [placarPartida[2].text, placarPartida[3].text]

    if len(placarMandantePrimeiroTempo) > 0:
      placarMandantePrimeiroTempo = placarMandantePrimeiroTempo[0].text
    else:
      placarMandantePrimeiroTempo = ""

    if len(placarVisitantePrimeiroTempo) > 0:
      placarVisitantePrimeiroTempo = placarVisitantePrimeiroTempo[0].text
    else:
      placarVisitantePrimeiroTempo = ""

    if len(placarMandanteSegundoTempo) > 0:
      placarMandanteSegundoTempo = placarMandanteSegundoTempo[0].text
    else:
      placarMandanteSegundoTempo = ""

    if len(placarVisitanteSegundoTempo) > 0:
      placarVisitanteSegundoTempo = placarVisitanteSegundoTempo[0].text
    else:
      placarVisitanteSegundoTempo = ""

    if len(placarMandanteProrrogacao) > 0:
      placarMandanteProrrogacao = placarMandanteProrrogacao[0].text
    else:
      placarMandanteProrrogacao = ""

    if len(placarVisitanteProrrogacao) > 0:
      placar_visitante_prorrogacao = placarVisitanteProrrogacao[0].text
    else:
      placar_visitante_prorrogacao = ""

    if len(placarMandantePenalties) > 0:
      placarMandantePenalties = placarMandantePenalties[0].text
    else:
      placarMandantePenalties = ""

    if len(placarVisitantePenalties) > 0:
      placarVisitantePenalties = placarVisitantePenalties[0].text
    else:
      placarVisitantePenalties = ""

    partida["placarFinal"] = ":".join(placarPartida)
    partida["placarPrimeiroTempo"] = placarMandantePrimeiroTempo + \
                                     ":" + placarVisitantePrimeiroTempo
    partida["placarSegundoTempo"] = placarMandanteSegundoTempo + \
                                    ":" + placarVisitanteSegundoTempo
    partida["placarProrrogacao"] = placarMandanteProrrogacao + \
                                   ":" + placar_visitante_prorrogacao
    partida["placarPenalties"] = placarMandantePenalties + \
                                 ":" + placarVisitantePenalties

    partida["idEquipeMandante"] = hash_utils.gerarHash(
      equipeMandante["url"])
    partida["idEquipeVisitante"] = hash_utils.gerarHash(
      equipeVisitante["url"])

    partida["competicao"] = competicao
    partida["equipeMandante"] = equipeMandante
    partida["equipeVisitante"] = equipeVisitante

    partida["tags"] = [string_utils.limparString(competicao["nome"]),
                       string_utils.limparString(equipeMandante["nome"]),
                       string_utils.limparString(equipeVisitante["nome"])
                       ]

    linksInformacoesDisponiveis = browser.find_elements_by_css_selector(CSS_LINKS_INFOS_PARTIDA)

    informacoesDiponiveis = verificarInformacoesDisponiveis(
      linksInformacoesDisponiveis)

    partida["timelineDisponivel"] = informacoesDiponiveis["resumo-de-jogo"] or informacoesDiponiveis["summary"]
    partida["estatisticasDisponiveis"] = informacoesDiponiveis["resumo-de-jogo/estatisticas-de-jogo"]
    partida["oddsDisponiveis"] = informacoesDiponiveis["comparacao-de-odds"]
    partida["comentariosDisponiveis"] = informacoesDiponiveis["resumo-de-jogo/comentarios-ao-vivo"]
    partida["escalacaoDisponivel"] = informacoesDiponiveis["resumo-de-jogo/equipes"]
    partida["headToHeadDisponivel"] = informacoesDiponiveis["h2h"]
    partida["videosDisponiveis"] = informacoesDiponiveis["videos"]
    partida["fotosDisponiveis"] = informacoesDiponiveis["imagens-da-partida"]
    partida["noticiasDisponiveis"] = informacoesDiponiveis["noticias"]

    if partida["timelineDisponivel"] and extrairTimeline:
      htmlTimeline = browser.find_elements_by_css_selector(
        "div[class^=verticalSections]")
      partida["timelineDisponivel"] = len(htmlTimeline) > 0

      if len(htmlTimeline) > 0:
        partida["timeline"] = extrairTimelinePartida(urlPartida)

    if partida["estatisticasDisponiveis"] and extrairStats:
      partida["estatisticas"] = extrairEstatisticasPartida(urlPartida)

    if partida["oddsDisponiveis"] and extrairOdds:
      partida["odds"] = getOddsPartida()

    if partida["headToHeadDisponivel"] and extrairUltimasPartidas:
      partida["headToHead"] = obterUltimasPartidasEquipes()

    return partida

  except Exception as e:
    log.ERRO(f"Não foi possível obter dados partida: {urlPartida}", e.args)
    return None


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


def getOddsPartida():
  try:
    browser = navegador_web.obterNavegadorWeb()
    bookmakers = {
      "resultado": {},
      "duplaChance": {},
      "drawNoBet": {},
      "oddEven": {},
      "btts": {},
      "underOver": [],
      "placarExato": []
    }
    mercadosDisponiveis = getMercadosApostaDisponiveis()

    for mercado in mercadosDisponiveis:
      link_mercado = browser.find_element_by_css_selector(
        "#{}>span>a".format(mercado["id_link"]))
      link_mercado.click()
      odds = getOddsPorMercado(mercado)

      if mercado["tipo"] == TIPO_MERCADO.RESULTADO:
        bookmakers["resultado"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.DUPLA_CHANCE:
        bookmakers["duplaChance"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.DNB:
        bookmakers["drawNoBet"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.ODD_EVEN:
        bookmakers["oddEven"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.BTTS:
        bookmakers["btts"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.UNDER_OVER:
        bookmakers["underOver"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.PLACAR:
        bookmakers["placarExato"] = odds

    return bookmakers

  except Exception as e:
    log.ERRO(f"Erro ao obter odds da partida [{browser.current_url}]", e.args)
    return bookmakers


def getMercadosApostaDisponiveis():
  try:
    navegador = navegador_web.obterNavegadorWeb()
    CSS_LINK_ODDS = "#a-match-odds-comparison"
    CSS_LISTA_ODDS = "#tab-match-odds-comparison>#odds-comparison-content>.odds-comparison-bookmark >ul.ifmenu>li"

    linkOdds = navegador.find_element_by_css_selector(
      CSS_LINK_ODDS)
    linkOdds.click()

    navegador_web.aguardarCarregamentoPagina("#odds-comparison-preload")

    listaOdds = navegador.find_elements_by_css_selector(
      CSS_LISTA_ODDS)
    listaBookmakers = []

    for odd in listaOdds:
      id_bookmark = odd.get_attribute("id")
      bookmark = {"id_link": id_bookmark,
                  "tipo": "",
                  "id_url": id_bookmark.replace("bookmark-", "") + "-odds"}

      if id_bookmark == 'bookmark-1x2':
        bookmark["tipo"] = TIPO_MERCADO.RESULTADO
      elif id_bookmark == 'bookmark-under-over':
        bookmark["tipo"] = TIPO_MERCADO.UNDER_OVER
      elif id_bookmark == 'bookmark-moneyline':
        bookmark["tipo"] = TIPO_MERCADO.DNB
      # elif id_bookmark == 'bookmark-asian-handicap':
      #     print('')
      # elif id_bookmark == 'bookmark-european-handicap':
      #     print('')
      elif id_bookmark == 'bookmark-double-chance':
        bookmark["tipo"] = TIPO_MERCADO.DUPLA_CHANCE
      # elif id_bookmark == 'bookmark-ht-ft':
      #     print('')
      elif id_bookmark == 'bookmark-correct-score':
        bookmark["tipo"] = TIPO_MERCADO.PLACAR
      elif id_bookmark == 'bookmark-oddeven':
        bookmark["tipo"] = TIPO_MERCADO.ODD_EVEN
      elif id_bookmark == 'bookmark-both-teams-to-score':
        bookmark["tipo"] = TIPO_MERCADO.BTTS
      else:
        pass

      listaBookmakers.append(bookmark)

    return listaBookmakers

  except Exception as e:
    log.ERRO("Não foi possível obter mercados disponíveis para aposta.", e.args)
    return []


def getOddsPorMercado(mercado):
  try:
    navegador = navegador_web.obterNavegadorWeb()
    CSS_TABELA_ODDS_RESULTADO = "#block-1x2-ft>table>tbody>tr"
    CSS_TABELA_ODDS_UNDER_OVER = "#block-under-over-ft>table"
    CSS_TABELA_ODDS_DNB = "#block-moneyline-ft>table>tbody>tr"
    CSS_TABELA_ODDS_BTTS = "div#block-both-teams-to-score-ft>table>tbody>tr"
    CSS_TABELA_ODDS_PLACAR = "#block-correct-score-ft>table"
    CSS_TABELA_ODDS_ODD_EVEN = "#block-oddeven-ft>table>tbody>tr"
    CSS_TABELA_ODDS_DUPLA_CHANCE = "#block-double-chance-ft>table>tbody>tr"

    listaOdds = []

    if mercado["tipo"] == TIPO_MERCADO.RESULTADO:
      tabelaOdds = navegador.find_elements_by_css_selector(
        CSS_TABELA_ODDS_RESULTADO)
      listaOdds = getOddsResultado(tabelaOdds)

    if mercado["tipo"] == TIPO_MERCADO.UNDER_OVER:
      tabelaOdds = navegador.find_elements_by_css_selector(
        CSS_TABELA_ODDS_UNDER_OVER)

      for tabela in tabelaOdds:
        qtd_gols = tabela.get_attribute("id").split("_")[-1]

        if ".5" in qtd_gols:
          odds = getOddsUnderOver(
            tabela.find_elements_by_css_selector("tbody>tr"), qtd_gols)
          if odds != {}:
            listaOdds.append(odds)

    if mercado["tipo"] == TIPO_MERCADO.DNB:
      tabelaOdds = navegador.find_elements_by_css_selector(
        CSS_TABELA_ODDS_DNB)
      listaOdds = getOddsDrawNoBet(tabelaOdds)

    if mercado["tipo"] == TIPO_MERCADO.BTTS:
      tabelaOdds = navegador.find_elements_by_css_selector(
        CSS_TABELA_ODDS_BTTS)
      listaOdds = getOddsBtts(tabelaOdds)

    if mercado["tipo"] == TIPO_MERCADO.PLACAR:
      tabelaOdds = navegador.find_elements_by_css_selector(
        CSS_TABELA_ODDS_PLACAR)

      for tabela in tabelaOdds:
        odds = getOddsPlacarExato(
          tabela.find_elements_by_css_selector("tbody>tr"))
        listaOdds.append(odds)

    if mercado["tipo"] == TIPO_MERCADO.ODD_EVEN:
      tabelaOdds = navegador.find_elements_by_css_selector(
        CSS_TABELA_ODDS_ODD_EVEN)
      listaOdds = getOddsImparPar(tabelaOdds)

    if mercado["tipo"] == TIPO_MERCADO.DUPLA_CHANCE:
      tabelaOdds = navegador.find_elements_by_css_selector(
        CSS_TABELA_ODDS_DUPLA_CHANCE)
      listaOdds = getOddsDuplaChance(tabelaOdds)

    return listaOdds

  except Exception as e:
    log.ERRO(f"Não foi possível obter ODDS para o mercado {mercado}.", e.args)
    return []


def getOddsResultado(bookmakers):
  quantidadeOdds = len(bookmakers)
  redutorQuantidadeMandante = 0
  redutorQuantidadeEmpate = 0
  redutorQuantidadeVisitante = 0

  valorOddsMandante = 0
  valorOddsEmpate = 0
  valorOddsVisitante = 0

  try:
    for linha in bookmakers:
      campos = linha.find_elements_by_css_selector("td>span")

      oddMandante = campos[0].text.replace("-", "0")
      oddEmpate = campos[1].text.replace("-", "0")
      oddVisitante = campos[2].text.replace("-", "0")

      if oddMandante == "0": redutorQuantidadeMandante += 1
      if oddEmpate == "0": redutorQuantidadeEmpate += 1
      if oddVisitante == "0": redutorQuantidadeVisitante += 1

      valorOddsMandante += float(oddMandante)
      valorOddsEmpate += float(oddEmpate)
      valorOddsVisitante += float(oddVisitante)

    return {
      "mandante": round(valorOddsMandante / (quantidadeOdds - redutorQuantidadeMandante),
                        CASAS_DECIMAIS),
      "empate": round(valorOddsEmpate / (quantidadeOdds - redutorQuantidadeEmpate), CASAS_DECIMAIS),
      "visitante": round(valorOddsVisitante / (quantidadeOdds - redutorQuantidadeVisitante),
                         CASAS_DECIMAIS)
    }

  except Exception as e:
    log.ERRO("Não foi possível obter ODDs de resultado.", e.args)
    return {}


def getOddsDrawNoBet(tabelaOdds):
  quantidadeOdds = len(tabelaOdds)
  redutorQuantidadeMandante = 0
  redutorQuantidadeVisitante = 0

  valorOddsMandante = 0
  valorOddsVisitante = 0

  try:

    for linha in tabelaOdds:
      campos = linha.find_elements_by_css_selector("td>span")

      oddMandante = campos[0].text.replace("-", "0")
      oddVisitante = campos[1].text.replace("-", "0")

      if oddMandante == "0": redutorQuantidadeMandante += 1
      if oddVisitante == "0": redutorQuantidadeVisitante += 1

      valorOddsMandante += float(oddMandante)
      valorOddsVisitante += float(oddVisitante)

    return {
      "mandante": round(valorOddsMandante / (quantidadeOdds - redutorQuantidadeMandante),
                        CASAS_DECIMAIS),
      "visitante": round(valorOddsVisitante / (quantidadeOdds - redutorQuantidadeVisitante),
                         CASAS_DECIMAIS)
    }

  except Exception as e:
    log.ERRO(f"Não foi possível obter odds DNB.", e.args)
    return {}


def getOddsUnderOver(tabelaOdds, quantidadeGols):
  quantidadeOdds = len(tabelaOdds)
  redutorQuantidadeUnder = 0
  redutorQuantidadeOver = 0

  valorOddsOver = 0
  valorOddsUnder = 0

  try:
    for linha in tabelaOdds:
      campos = linha.find_elements_by_css_selector("td>span")

      oddOver = campos[0].text.replace("-", "0")
      oddUnder = campos[1].text.replace("-", "0")

      if oddOver == "0": redutorQuantidadeOver += 1
      if oddUnder == "0": redutorQuantidadeUnder += 1

      valorOddsOver += float(oddOver)
      valorOddsUnder += float(oddUnder)

    return {
      "totalGols": quantidadeGols,
      "under": round(valorOddsUnder / (quantidadeOdds - redutorQuantidadeUnder), CASAS_DECIMAIS),
      "over": round(valorOddsOver / (quantidadeOdds - redutorQuantidadeOver), CASAS_DECIMAIS)
    }

  except Exception as e:
    log.ERRO("Não foi possível obter odds under/over.", e.args)
    return {}


def getOddsPlacarExato(tabelaOdds):
  quantidadeOdds = len(tabelaOdds)
  redutorQuantidadeOdds = 0

  valorOddsPlacar = 0

  try:
    for linha in tabelaOdds:
      campos = linha.find_elements_by_css_selector("td>span")
      placar = linha.find_element_by_css_selector(
        "td.correct_score").text

      oddPlacar = campos[0].text.replace("-", "0")
      if oddPlacar == "0": redutorQuantidadeOdds += 1

      valorOddsPlacar += float(oddPlacar)

    placar = placar.split(":")

    return {
      "placarMandante": placar[0],
      "placarVisitante": placar[1],
      "valor": round(valorOddsPlacar / (quantidadeOdds - redutorQuantidadeOdds), CASAS_DECIMAIS)
    }
  except Exception as e:
    log.ERRO("Não foi possível obter ODDs de placar exato.", e.args)
    return {}


def getOddsBtts(tabelaOdds):
  quantidadeOdds = len(tabelaOdds)
  redutorQuantidadeBtts = 0
  redutorQuantidadeNoBtts = 0

  valorOddsBtts = 0
  valorOddsNoBtts = 0

  try:

    for linha in tabelaOdds:
      campos = linha.find_elements_by_css_selector("td>span")

      oddBtts = campos[0].text.replace("-", "0")
      oddNoBtts = campos[1].text.replace("-", "0")

      if oddBtts == "0": redutorQuantidadeBtts += 1
      if oddNoBtts == "0": redutorQuantidadeNoBtts += 1

      valorOddsBtts += float(oddBtts)
      valorOddsNoBtts += float(oddNoBtts)

    return {
      "yes": round(valorOddsBtts / (quantidadeOdds - redutorQuantidadeBtts), CASAS_DECIMAIS),
      "no": round(valorOddsNoBtts / (quantidadeOdds - redutorQuantidadeNoBtts), CASAS_DECIMAIS)
    }

  except Exception as e:
    log.ERRO("Não foi possível obter ODDs BTTS.", e.args)
    return {}


def getOddsImparPar(tabelaOdds):
  quantidadeOdds = len(tabelaOdds)
  redutorQuantidadeImpar = 0
  redutorQuantidadePar = 0

  valorOddImpar = 0
  valorOddPar = 0

  try:
    for linha in tabelaOdds:
      campos = linha.find_elements_by_css_selector("td>span")

      oddImpar = campos[0].text.replace("-", "0")
      oddPar = campos[1].text.replace("-", "0")

      if oddImpar == "0": redutorQuantidadeImpar += 1
      if oddPar == "0": redutorQuantidadePar += 1

      valorOddImpar += float(oddImpar)
      valorOddPar += float(oddPar)

    return {
      "odd": round(valorOddImpar / (quantidadeOdds - redutorQuantidadeImpar), CASAS_DECIMAIS),
      "even": round(valorOddPar / (quantidadeOdds - redutorQuantidadePar), CASAS_DECIMAIS)
    }

  except Exception as e:
    log.ERRO("Não foi possível obter ODDs IMPAR/PAR.", e.args)
    return {}


def getOddsDuplaChance(tabelaOdds):
  total_odds = len(tabelaOdds)
  redutorQuantidadeContraMandante = 0
  redutorQuantidadeContraEmpate = 0
  redutorQuantidadeContraVisitante = 0

  valorOddContraMandante = 0
  valorOddContraEmpate = 0
  valorOddContraVisitante = 0

  try:
    for linha in tabelaOdds:
      campos = linha.find_elements_by_css_selector("td>span")

      oddContraVisitante = campos[0].text.replace("-", "0")
      oddContraEmpate = campos[1].text.replace("-", "0")
      oddContraMandante = campos[2].text.replace("-", "0")

      if oddContraMandante == "0": redutorQuantidadeContraMandante += 1
      if oddContraEmpate == "0": redutorQuantidadeContraEmpate += 1
      if oddContraVisitante == "0": redutorQuantidadeContraVisitante += 1

      valorOddContraMandante += float(oddContraMandante)
      valorOddContraEmpate += float(oddContraEmpate)
      valorOddContraVisitante += float(oddContraVisitante)

    return {
      "contraVisitante": round(valorOddContraVisitante / (total_odds - redutorQuantidadeContraVisitante),
                               CASAS_DECIMAIS),
      "contraMandante": round(valorOddContraMandante / (total_odds - redutorQuantidadeContraEmpate),
                              CASAS_DECIMAIS),
      "contraEmpate": round(valorOddContraEmpate / (total_odds - redutorQuantidadeContraEmpate),
                            CASAS_DECIMAIS)
    }

  except Exception as e:
    log.ERRO("Não foi possível obter ODDs dupla chance.", e.args)
    return {}


def extrairTimelinePartida(urlPartida: str):
  try:
    CSS_DADOS_TIMELINE = "div[class^=verticalSections]"
    CSS_EVENTOS_MANDANTE = "div[class*=homeParticipant] "
    CSS_EVENTOS_VISITANTE = "div[class*=awayParticipant] "

    browser = navegador_web.obterNavegadorWeb()
    urlTimeline = f"{navegador_web.URL_BASE}{urlPartida}#resumo-de-jogo/estatisticas-de-jogo/"
    browser.get(urlTimeline)

    htmlTimeline = navegador_web.obterElementoAposCarregamento(CSS_DADOS_TIMELINE)
    htmlEventosMandante = htmlTimeline.find_elements_by_css_selector(CSS_EVENTOS_MANDANTE)
    htmlEventosVisitante = htmlTimeline.find_elements_by_css_selector(CSS_EVENTOS_VISITANTE)

    listaEventos = []
    contadorEventos = 1

    for html in htmlEventosMandante:
      htmlTipoEvento = html.find_element_by_css_selector("div[class^=incidentIcon] div svg")
      eventoPartida = {
        "tipo": "",
        "equipe": "",
        "minutos": "",
        "participante_01": "",
        "participante_02": ""
      }

    dadosHtml = html_utils.converterStringParaHtml(htmlEventos)

    htmlEventos = dadosHtml.select(".detailMS__incidentRow")

    for html in htmlEventos:

      eventoPartida = {"seq": contadorEventos,
                       "tipo": "",
                       "equipe": "",
                       "minutos": "",
                       "participante_01": "",
                       "participante_02": ""
                       }

      classeCss = html.attrs["class"][1]

      if classeCss != "--empty":
        if classeCss == "incidentRow--away":
          eventoPartida["equipe"] = "V"
        elif classeCss == "incidentRow--home":
          eventoPartida["equipe"] = "M"

        eventoPartida["tipo"] = \
          html.select(".icon-box span")[0].attrs["class"][1]
        eventoPartida["minutos"] = html.select(
          ".time-box,.time-box-wide")[0].getText()

        participanteUm = {"nome": "", "url": ""}
        participanteDois = {"nome": "", "url": ""}

        htmlParticipantes = html.select(
          ".participant-name a,.substitution-in-name a,.substitution-out-name a")

        if len(htmlParticipantes) >= 1:
          participanteUm["nome"] = string_utils.limparString(
            htmlParticipantes[0].getText())

          participanteUm["url"] = html_utils.obterUrlAtributoOnClick(
            htmlParticipantes[0].attrs["onclick"])

        if len(htmlParticipantes) == 2:
          participanteDois["nome"] = string_utils.limparString(
            htmlParticipantes[1].getText())

          participanteDois["url"] = html_utils.obterUrlAtributoOnClick(
            htmlParticipantes[1].attrs["onclick"])

        eventoPartida["participante_01"] = participanteUm
        eventoPartida["participante_02"] = participanteDois

        eventoPartida["tipo"] = normalizarDescricaoEvento(
          eventoPartida["tipo"])

        listaEventos.append(eventoPartida)
        contadorEventos += 1

    return listaEventos

  except Exception as e:
    log.ERRO("Não foi possível obter timeline de eventos da partida.", e.args)
    return listaEventos


def extrairEstatisticasPartida(urlPartida: str):
  estatisticasPartida = []
  try:
    CSS_LINHAS_ESTATISTICAS = "div[class^=statRow]"
    CSS_VALORES_ESTATISTICA = "div[class^=statCategory] div"

    urlEstatisticas = f"{navegador_web.URL_BASE}{urlPartida}#resumo-de-jogo/estatisticas-de-jogo/"
    browser = navegador_web.obterNavegadorWeb()
    browser.get(urlEstatisticas)

    htmlEstatisticas = navegador_web.obterElementoAposCarregamento(CSS_LINHAS_ESTATISTICAS)

    for html in htmlEstatisticas:
      estatistica = {"desc": "",
                     "valor_mandante": "",
                     "valor_visitante": ""}

      camposEstatistica = html.find_elements_by_css_selector(CSS_VALORES_ESTATISTICA)

      estatistica["desc"] = string_utils.limparString(
        camposEstatistica[1].text)
      estatistica["valor_mandante"] = string_utils.limparString(
        camposEstatistica[0].text)
      estatistica["valor_visitante"] = string_utils.limparString(
        camposEstatistica[2].text)

      estatisticasPartida.append(estatistica)

    return estatisticasPartida

  except Exception as e:
    log.ERRO("Não foi possível obter estatísticas da partida.", e.args)
    return estatisticasPartida


def obterUltimasPartidasEquipes():
  navegador = navegador_web.obterNavegadorWeb()
  ultimasPartidas = {
    "mandante": [],
    "visitante": [],
    "confrontosDiretos": []
  }

  try:
    CSS_LINK_HEAD_2_HEAD = "#a-match-head-2-head"
    CSS_LOADING = "#head-2-head-preload"

    CSS_TABLE_PARTIDAS_MANDANTE = "table.h2h_home"
    CSS_TABLE_PARTIDAS_VISITANTE = "table.h2h_away"
    CSS_TABLE_PARTIDAS_DIRETOS = "table.h2h_mutual"

    linkHeadToHead = navegador.find_element_by_css_selector(CSS_LINK_HEAD_2_HEAD)
    linkHeadToHead.click()

    navegador_web.aguardarCarregamentoPagina(CSS_LOADING)

    html = navegador.find_element_by_css_selector("#tab-h2h-overall").get_attribute("innerHTML")

    dadosHtml = html_utils.converterStringParaHtml(html)

    linhasTabelaPartidasMandante = dadosHtml.select(CSS_TABLE_PARTIDAS_MANDANTE + " tbody tr.highlight")
    linhasTabelaPartidasVisitante = dadosHtml.select(CSS_TABLE_PARTIDAS_VISITANTE + " tbody tr.highlight")
    linhasTabelaPartidasDiretas = dadosHtml.select(CSS_TABLE_PARTIDAS_DIRETOS + " tbody tr.highlight")

    ultimasPartidas["mandante"] = processarTabelaPartidasEquipe(linhasTabelaPartidasMandante)
    ultimasPartidas["visitante"] = processarTabelaPartidasEquipe(linhasTabelaPartidasVisitante)
    ultimasPartidas["confrontosDiretos"] = processarTabelaPartidasEquipe(linhasTabelaPartidasDiretas)

    return ultimasPartidas


  except Exception as e:
    log.ERRO("Não foi possível obter últimas partidas das equipes.", e.args)
    return ultimasPartidas


def processarTabelaPartidasEquipe(linhasTabela):
  try:
    listaPartidas = []

    for linha in linhasTabela:

      atributoOnClick = linha.attrs["onclick"]
      posicaoInicioIdPartida = atributoOnClick.find("g_0_")
      idPartida = atributoOnClick[posicaoInicioIdPartida:posicaoInicioIdPartida + 12].replace("g_0_", "")

      camposTabela = linha.select("td")

      urlPartida = "/jogo/{}/".format(idPartida)
      dataPartida = camposTabela[0].select("span")[0].text
      competicao = camposTabela[1].attrs["title"]
      equipeMandante = camposTabela[2].select("span")[0].text
      equipeVisitante = camposTabela[3].select("span")[0].text
      placar = camposTabela[4].select("span.score")[0].text

      resultado = ""
      if len(camposTabela) == 6:
        resultado = camposTabela[5].select("span a")[0].attrs["title"]

      partidaEmCasa = len(camposTabela[2].attrs["class"]) > 1

      partida = {"idPartida": hash_utils.gerarHash(idPartida),
                 "urlPartida": urlPartida,
                 "data": datetime_utils.converterHoraLocalToUtc(datetime.strptime(dataPartida, "%d.%m.%y")),
                 "competicao": competicao,
                 "mandante": equipeMandante,
                 "visitante": equipeVisitante,
                 "casaFora": "CASA" if partidaEmCasa else "FORA",
                 "placar": placar.replace("(", "|").replace(")", ""),
                 "resultado": resultado.upper()
                 }

      listaPartidas.append(partida)

    return listaPartidas
  except Exception as e:
    log.ERRO("Não foi possível processar tabela de partidas da equipe.", e.args)
    return []


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


def normalizarDescricaoEvento(descricao: str):
  if descricao == "y-card":
    descricao = "CARTAO_AMARELO"

  elif descricao == "soccer-ball":
    descricao = "GOL"

  elif descricao == "substitution-in":
    descricao = "SUBSTITUICAO"

  elif descricao == "yr-card":
    descricao = "CARTAO_AMARELO_VERMELHO"

  elif descricao == "soccer-ball-own":
    descricao = "GOL_CONTRA"

  elif descricao == "Penalty goal":
    descricao = "GOL_PENALTY"

  elif descricao == "r-card":
    descricao = "CARTAO_VERMELHO"

  elif descricao == "Penalty save":
    descricao = "PENALTY_MARCADO"

  elif descricao == "penalty-missed":
    descricao = "PENALTY_PERDIDO"
  else:
    log.ALERTA(f"Descrição do evento '{descricao}' não mapeda.")

  return descricao


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

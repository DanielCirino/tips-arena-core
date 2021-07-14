from tipsarena_core.utils import html_utils, string_utils
from tipsarena_core.services import log_service as log


def processarHtmlListaPartidas(html: str):
  try:
    CSS_LINHAS_PARTIDA = "div[id^=g_1_]"
    CSS_DATA_HORA_PARTIDA = ".event__time"
    CSS_NOME_MANDANTE = ".event__participant--home"
    CSS_ESCUDO_MANDANTE = ".event__logo--home"
    CSS_NOME_VISITANTE = ".event__participant--away"
    CSS_ESCUDO_VISITANTE = ".event__logo--away"
    CSS_PLACAR_FINAL = ".event__scores"
    CSS_PLACAR_PARCIAL = ".event__part"

    tabelaPartidas = html_utils.converterStringParaHtml(html)
    linhasHtml = tabelaPartidas.select(CSS_LINHAS_PARTIDA)

    listaPartidas = []
    sequencial = 1

    for item in linhasHtml:
      idPartida = item.attrs["id"].split("_")[2]
      urlPartida = f"/jogo/{idPartida}/"
      dataHoraPartida = "-" if item.find(CSS_DATA_HORA_PARTIDA) == None else item.select_one(CSS_DATA_HORA_PARTIDA).text

      nomeEquipeMandante = item.select_one(CSS_NOME_MANDANTE).text
      escudoEquipeMandante = item.select_one(CSS_ESCUDO_MANDANTE).attrs["src"] if "src" in item.select_one(
        CSS_ESCUDO_MANDANTE).attrs else "/res/image/data/IgO7K1ZA-Qmtm30D7.png"

      nomeEquipeVisitante = item.select_one(CSS_NOME_VISITANTE).text
      escudoEquipeVisitante = item.select_one(CSS_ESCUDO_VISITANTE).attrs["src"] if "src" in item.select_one(
        CSS_ESCUDO_VISITANTE).attrs else "/res/image/data/IgO7K1ZA-Qmtm30D7.png"

      placarFinal = item.select_one(CSS_PLACAR_FINAL).text

      placarParcial = "-" if item.find(CSS_PLACAR_PARCIAL) == None else item.select_one(CSS_PLACAR_PARCIAL).text

      listaPartidas.append({
        "idPartida": idPartida,
        "url": urlPartida,
        "dataHoraPartida": dataHoraPartida,
        "nomeEquipeMandante": string_utils.limparString(nomeEquipeMandante),
        "escudoEquipeMandante": escudoEquipeMandante,
        "nomeEquipeVisitante": string_utils.limparString(nomeEquipeVisitante),
        "escudoEquipeVisitante": escudoEquipeVisitante,
        "placarParcial": placarParcial,
        "placarFinal": placarFinal,
        "sequencial": sequencial}
      )
      sequencial += 1

    return listaPartidas
  except Exception as e:
    log.ERRO("Não foi possível processar lista de partidas da url {}.", e.args)
    return None


def processarHtmlPartida(html: str):
  try:
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


def processarHtmlEventosPartida(html: str):
  pass

def processarHtmlOddsPartida(html: str):
  pass
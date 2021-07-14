from datetime import datetime
from tipsarena_core.enums.enum_partida import STATUS as STATUS_PARTIDA
from tipsarena_core.utils import html_utils, string_utils, datetime_utils
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
    CSS_CABECALHO_PARTIDA = "[class*=tournamentHeaderDescription]"
    CSS_DADOS_MANDANTE = "[class^=home_]"
    CSS_DADOS_VISITANTE = "[class^=away_]"
    CSS_PLACAR_PARTIDA = "[class^=score_] [class^=matchInfo_] [class^=wrapper_]"
    CSS_DATA_PARTIDA = "[class^=startTime_] div"
    CSS_STATUS_PARTIDA = "[class^=status_]"
    CSS_INFO_PARTIDA = "div[class^=info_]"
    CSS_LINKS_PARTIDA = "div.tabs div.tabs__group a.tabs__tab"

    htmlPartida = html_utils.converterStringParaHtml(html)

    htmlDadosCompeticao = htmlPartida.select_one(CSS_CABECALHO_PARTIDA)
    htmlDadosMandante = htmlPartida.select_one(CSS_DADOS_MANDANTE)
    htmlImageMandante = htmlDadosMandante.select_one("[class^=participantImage_] img")
    htmlNomeMandante = htmlDadosMandante.select_one("[class^=participantName_] a")

    htmlDadosVisitante = htmlPartida.select_one(CSS_DADOS_VISITANTE)
    htmlImageVisitante = htmlDadosVisitante.select_one("[class^=participantImage_] img")
    htmlNomeVisitante = htmlDadosVisitante.select_one("[class^=participantName_] a")

    htmlDataPartida = htmlPartida.select_one(CSS_DATA_PARTIDA)
    htmlStatusPartida = htmlPartida.select_one(CSS_STATUS_PARTIDA)
    htmlInfoPartida = htmlPartida.select_one(CSS_INFO_PARTIDA)
    htmlLinksPartida = htmlPartida.select(CSS_LINKS_PARTIDA)
    htmlPlacarPartida = htmlPartida.select_one(CSS_PLACAR_PARTIDA)
    htmlFaseCompeticao = htmlDadosCompeticao.select_one("[class^=country_] a")

    urlPartida = ""
    status = htmlStatusPartida.text.split("-")
    minutos = status[1] if len(status) > 1 else ""
    dataHora = htmlDataPartida.text
    informacoes = htmlInfoPartida.text.strip()
    placarFinal = htmlPlacarPartida.text.strip()

    urlCompeticao = htmlFaseCompeticao.attrs["href"]
    nomeCompeticao = htmlFaseCompeticao.text.split("-")[0]
    faseCompeticao = "-".join(htmlFaseCompeticao.text.split("-")[1::])

    nomeEquipeMandante = htmlNomeMandante.text
    urlEquipeMandante = htmlNomeMandante.attrs["href"]
    idEquipeMandante = urlEquipeMandante.split("/")[-1]
    urlImageMandante = htmlImageMandante.attrs["src"]

    nomeEquipeVisitante = htmlNomeVisitante.text
    urlEquipeVisitante = htmlNomeVisitante.attrs["href"]
    idEquipeVisitante = urlEquipeVisitante.split("/")[-1]
    urlImageVisitante = htmlImageVisitante.attrs["src"]
    competicao = {"url": urlCompeticao,
                  "nome": nomeCompeticao
                  }

    equipeMandante = {"id": idEquipeMandante, "url": urlEquipeMandante, "nome": nomeEquipeMandante,
                      "urlEscudo": urlImageMandante}
    equipeVisitante = {"id": idEquipeVisitante, "url": urlEquipeVisitante, "nome": nomeEquipeVisitante,
                       "urlEscudo": urlImageVisitante}

    return {
      "url": "",
      "status": normalizarDescricaoStatus(status[0]),
      "dataHora": dataHora,
      "dataHoraUtc": datetime_utils.converterHoraLocalToUtc(datetime.strptime(dataHora, "%d.%m.%Y %H:%M")),
      "minutos": minutos,
      "info": informacoes,
      "faseCompeticao": faseCompeticao,
      "placarFinal": placarFinal,
      "competicao": competicao,
      "equipeMandante": equipeMandante,
      "equipeVisitante": equipeVisitante,
    }

  except Exception as e:
    log.ERRO("Não foi possível processar HMTL da partida.", e.args)
    return None


def processarHtmlEventosPartida(html: str):
  pass


def processarHtmlOddsPartida(html: str):
  pass


def normalizarDescricaoStatus(status: str):
  if status == "":
    statusPartida = STATUS_PARTIDA.AGENDADO.name

  elif status.find("1º tempo") != -1 or status.find("1st Half") != -1:
    statusPartida = STATUS_PARTIDA.PRIMEIRO_TEMPO.name

  elif status.find("2º tempo") != -1 or status.find("2nd Half") != -1:
    statusPartida = STATUS_PARTIDA.SEGUNDO_TEMPO.name

  elif status == "Adiado" or status == "Postponed":
    statusPartida = STATUS_PARTIDA.ADIADO.name

  elif status == "Após Pênaltis" or status == "After Penalties":
    statusPartida = STATUS_PARTIDA.FINALIZADO.name

  elif status == "Após Prorrogação" or status == "After Extra Time":
    statusPartida = STATUS_PARTIDA.FINALIZADO.name

  elif status == "Intervalo" or status == "Half Time" or status == "Break Time":
    statusPartida = STATUS_PARTIDA.INTERVALO.name

  elif status == "Atribuído" or status == "Awarded":
    statusPartida = STATUS_PARTIDA.RESULTADO_NAO_DISPONIVEL.name

  elif status == "Abandonado" or status == "Abandoned":
    statusPartida = STATUS_PARTIDA.ABANDONADO.name

  elif status == "Cancelado" or status == "Cancelled":
    statusPartida = STATUS_PARTIDA.CANCELADO.name

  elif status == "SRF - Só resultado final." or status == "FRO - Final result only.":
    statusPartida = STATUS_PARTIDA.RESULTADO_NAO_DISPONIVEL.name

  elif status == "SRF " or status == "FRO ":
    statusPartida = STATUS_PARTIDA.RESULTADO_NAO_DISPONIVEL.name

  elif status == "Encerrado" or status == "Finished":
    statusPartida = STATUS_PARTIDA.FINALIZADO.name

  elif status == "Walkover":
    statusPartida = STATUS_PARTIDA.W_O.name

  elif status.find("Walkover") != -1:
    statusPartida = STATUS_PARTIDA.W_O.name

  elif status == "Ao Vivo" or status == "Live":
    statusPartida = STATUS_PARTIDA.EM_ANDAMENTO.name

  elif status == "Extra Time":
    statusPartida = STATUS_PARTIDA.EM_ANDAMENTO.name

  elif status == "Penalties":
    statusPartida = "PENALTIES"

  else:
    log.ALERTA(f"Status '{status}' não mapeado.")
    statusPartida = status

  return statusPartida

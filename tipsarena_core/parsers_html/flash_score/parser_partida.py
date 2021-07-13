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


def __processarHtmlItemPartida(html: str):
  pass

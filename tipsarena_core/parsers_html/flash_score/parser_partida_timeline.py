from tipsarena_core.utils import html_utils,string_utils
from tipsarena_core.services import log_service as log

def processarHtmlTimeline(html:str):
  try:
    CSS_EVENTOS_MANDANTE = "div[class*=homeParticipant] "
    CSS_EVENTOS_VISITANTE = "div[class*=awayParticipant] "

    htmlTimeline = html_utils.converterStringParaHtml(html)

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
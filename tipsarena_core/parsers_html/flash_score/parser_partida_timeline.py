from tipsarena_core.utils import html_utils, string_utils
from tipsarena_core.services import log_service as log


def processarHtmlTimeline(html: str):
  try:
    CSS_EVENTOS_MANDANTE = "div[class*=homeParticipant]"
    CSS_EVENTOS_VISITANTE = "div[class*=awayParticipant]"

    htmlTimeline = html_utils.converterStringParaHtml(html)

    htmlEventosMandante = htmlTimeline.select(CSS_EVENTOS_MANDANTE)
    htmlEventosVisitante = htmlTimeline.select(CSS_EVENTOS_VISITANTE)

    eventosMandante = processarEventosTimeline("M", htmlEventosMandante)
    eventosVisitante = processarEventosTimeline("V", htmlEventosVisitante)

    return eventosMandante + eventosVisitante

  except Exception as e:
    log.ERRO("Não foi possível processar HTML timeline de eventos da partida.", e.args)
    return []


def processarEventosTimeline(equipe: str, htmlEventos):
  try:
    listaEventos = []

    for elemento in htmlEventos:
      htmlTimebox = elemento.select_one("[class^=incident_] [class^=timeBox]")
      htmlIconeEvento = elemento.select_one("[class^=incident_] [class^=incidentIcon_]")

      htmlSubstituicaoEntrada = elemento.select_one("[class^=incident_] [class^=incidentIconSub_]")
      htmlSubstituicaoSaida = elemento.select_one("[class^=incident_] [class^=incidentSubOut_]")

      htmlPrimeiroParticipante = elemento.select_one("[class^=playerName_]")
      htmlSegundoParticipantes = htmlSubstituicaoSaida.select_one("a") if htmlSubstituicaoSaida else None
      htmlDetalhesEvento = elemento.select_one("[class^=incident_] [class^=assist_]")
      htmlDetalhesAssistencia = elemento.select_one("[class^=incident_] [class^=assist_] a")

      minutos = htmlTimebox.text
      classeIcone = htmlSubstituicaoEntrada.select_one("div svg").attrs["class"][0] if htmlSubstituicaoEntrada else ''

      if htmlIconeEvento:
        classeIcone = htmlIconeEvento.select_one("div svg").attrs["class"][0]

      tipoEvento = normalizarDescricaoEvento(classeIcone.split("_")[0])

      participante01 = {
        "nome": string_utils.limparString(htmlPrimeiroParticipante.text),
        "url": htmlPrimeiroParticipante.attrs["href"]
      }

      participante02 = None

      if htmlSegundoParticipantes:
        participante02 = {
          "nome": string_utils.limparString(htmlSegundoParticipantes.text),
          "url": htmlSegundoParticipantes.attrs["href"]
        }

      if htmlDetalhesAssistencia:
        participante02 = {
          "nome": string_utils.limparString(htmlDetalhesAssistencia.text),
          "url": htmlDetalhesAssistencia.attrs["href"]
        }

      detalhesEvento = ""
      if htmlDetalhesEvento:
        detalhesEvento = htmlDetalhesEvento.text

      listaEventos.append({
        "tipo": tipoEvento,
        "equipe": equipe,
        "minutos": minutos,
        "participante01": participante01,
        "participante02": participante02,
        "detalhes": detalhesEvento.strip()
      }
      )

    return listaEventos
  except Exception as e:
    log.ERRO("Não foi possível processar eventos da timeline da partida.", e.args)
    return []


def normalizarDescricaoEvento(descricao: str):
  if descricao == "yellowCard":
    descricao = "CARTAO_AMARELO"

  elif descricao == "footballGoal":
    descricao = "GOL"

  elif descricao == "arrowUp":
    descricao = "SUBSTITUICAO"

  elif descricao == "redYellowCard":
    descricao = "CARTAO_AMARELO_VERMELHO"

  elif descricao == "footballOwnGoal":
    descricao = "GOL_CONTRA"

  elif descricao == "Penalty goal":
    descricao = "GOL_PENALTY"

  elif descricao == "card":
    descricao = "CARTAO_VERMELHO"

  elif descricao == "Penalty save":
    descricao = "PENALTY_MARCADO"

  elif descricao == "penaltyMissed":
    descricao = "PENALTY_PERDIDO"
  else:
    log.ALERTA(f"Descrição do evento '{descricao}' não mapeda.")

  return descricao

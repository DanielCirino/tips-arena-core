from tipsarena_core.utils import html_utils, string_utils, hash_utils
from tipsarena_core.services import log_service as log


def processarHtmlUltimasPartidasEquipes(html: str):
  try:
    CSS_SECOES_PARTIDAS = "div[class^=h2h] div[class^=section]"

    htmlUltimasPartidas = html_utils.converterStringParaHtml(html)
    htmlSessoesPartidas = htmlUltimasPartidas.select(CSS_SECOES_PARTIDAS)

    htmlPartidasMandante = htmlSessoesPartidas[0]
    htmlPartidasVisitante = htmlSessoesPartidas[1]
    htmlConfrontosDiretos = htmlSessoesPartidas[2]

    partidasMandante = processarHtmlPartidasEquipe(htmlPartidasMandante)
    partidasVisitante = processarHtmlPartidasEquipe(htmlPartidasVisitante)
    confrontosDiretos = processarHtmlPartidasEquipe(htmlConfrontosDiretos)

    return {
      "mandante": partidasMandante,
      "visitante": partidasVisitante,
      "confrontosDiretos": confrontosDiretos
    }


  except Exception as e:
    log.ERRO("Não foi possível obter últimas partidas das equipes.", e.args)
    return None


def processarHtmlPartidasEquipe(htmlPartidas):
  try:
    CSS_LINHAS_PARTIDA = "[class^=row]"
    CSS_COMPETICAO = "[class^=event]"
    CSS_DATA_PARTIDA = "[class^=date]"
    CSS_MANDANTE = "[class^=homeParticipant]"
    CSS_VISITANTE = "[class^=awayParticipant]"
    CSS_PLACAR_FINAL = "[class^=result]"
    CSS_RESULTADO = "[class^=icon] div"

    listaPartidas = []
    htmlListaPartidas = htmlPartidas.select(CSS_LINHAS_PARTIDA)

    for html in htmlListaPartidas:
      dataPartida = html.select_one(CSS_DATA_PARTIDA).text
      competicao = html.select_one(CSS_COMPETICAO).text
      equipeMandante = html.select_one(CSS_MANDANTE).text
      equipeVisitante = html.select_one(CSS_VISITANTE).text
      placar = html.select_one(CSS_PLACAR_FINAL).text
      resultado = "X" if html.select_one(CSS_RESULTADO) == None else html.select_one(CSS_RESULTADO).text

      informacoesMandante = html.select_one(CSS_MANDANTE).attrs['class']
      partidaEmCasa = len(informacoesMandante) > 1

      listaPartidas.append({"idPartida": "",
                            "urlPartida": "",
                            "data": dataPartida,
                            "competicao": competicao,
                            "mandante": equipeMandante,
                            "visitante": equipeVisitante,
                            "casaFora": "CASA" if partidaEmCasa else "FORA",
                            "placar": placar,
                            "resultado": resultado.upper()
                            })

    return listaPartidas
  except Exception as e:
    log.ERRO("Não foi possível processar tabela de partidas da equipe.", e.args)
    return []

# -*- coding: utf-8 -*-

from tipsarena_core.extratores import navegador_web
from tipsarena_core.utils import string_utils, html_utils
from tipsarena_core.services import log_service as log


def obterListaEquipesEdicaoCompeticao(navegador: navegador_web):
  try:
    browser = navegador.obterNavegadorWeb()
    CSS_LISTA_EQUIPES = "[class^=rowCellParticipantImage]"

    navegador.obterElementoAposCarregamento(CSS_LISTA_EQUIPES)
    htmlEquipes = browser.find_elements_by_css_selector(CSS_LISTA_EQUIPES)

    listaEquipes = []
    sequencial = 1

    for html in htmlEquipes:
      htmlEscudo = html.find_element_by_css_selector("img")
      listaEquipes.append(
        {"nome": htmlEscudo.get_attribute("alt"),
         "url": html.get_attribute("href"),
         "urlEscudo": htmlEscudo.get_attribute("src"),
         "sequencial": sequencial}
      )
      sequencial += 1

    return listaEquipes
  except Exception as e:
    log.ERRO(f"Não foi possível extrair lista de equipes da competição [{browser.current_url}]", e.args)
    return None


def obterDadosEquipe(urlEquipe):
  try:

    documentoHtml = html_utils.obterHtml(navegador_web.URL_BASE + urlEquipe)
    linksCabecalho = html_utils.obterDadosCabecalho(documentoHtml)

    paisEquipe = {"nome": linksCabecalho[1]["text"],
                  "url": linksCabecalho[1]["href"]}

    nomeEquipe = documentoHtml.select(".teamHeader__name")[0].text

    urlEscudoEquipe = documentoHtml.select(".teamHeader__logo")
    urlEscudoEquipe = urlEscudoEquipe[0]["style"].split("(")
    urlEscudoEquipe = urlEscudoEquipe[1].replace(")", "")

    return {
      "nome": string_utils.limparString(nomeEquipe),
      "pais": paisEquipe,
      "urlEscudo": urlEscudoEquipe,
      "url": urlEquipe
    }

  except Exception as e:
    log.ERRO(f"Não foi possível extrair dados da equipe [{urlEquipe}]", e.args)
    return None


def extrairUrlOnclick(textoOnclick):
  try:
    primeiraQuebra = textoOnclick.split("?")[1].split(":")[1]
    urlEquipe = primeiraQuebra.replace("window.open(\'", "").replace("\', \'_blank\');", "")
    return urlEquipe
    pass
  except Exception as e:
    log.ERRO(f"Não foi possível extrair URL do atributo onclick.", e.args)
    return ""

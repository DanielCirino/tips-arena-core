import requests
from bs4 import BeautifulSoup

from tipsarena_core.services import log_service as log


def obterHtml(url):
  try:
    page = requests.get(url)
    documento_html = BeautifulSoup(page.content, "html.parser")
    page.close()
    return documento_html
  except Exception as e:
    log.ERRO("Não foi possível obter o HTML da página:{}.".format(url), e.args)
    return None


def converterStringParaHtml(string):
  try:
    dados_html = BeautifulSoup(string, "html.parser")
    return dados_html
  except Exception as e:
    log.ERRO( "Não foi possível converter o texto para HTML.", e.args)
    return None


def obterDadosCabecalho(html):
  try:
    CSS_LINKS_CABECALHO = "h2.breadcrumb a"
    CSS_TEXTO_CABECALHO = ".teamHeader__text"
    cabecalhoCompeticao = html.select(CSS_LINKS_CABECALHO)
    linksCabecalho = []

    for item in cabecalhoCompeticao:
      linksCabecalho.append(
        {"text": item.text, "href": item.attrs["href"]})

    textoCabecalho = html.select(CSS_TEXTO_CABECALHO)

    if len(textoCabecalho) > 0:
      linksCabecalho.append(
        {"text": textoCabecalho[0].text, "href": "#"})

    return linksCabecalho
  except Exception as e:
    log.ERRO( "Não foi possível obter dados do cabeçalho.", e.args)
    return None


def obterUrlAtributoOnClick(onclick):
  try:
    url = onclick.split("(")[1].split(")")[0].replace("'", "")
    return url
  except Exception as e:
    log.ERRO( "Não foi possível extrair URL do atributo onclick.", e.args)
    return ""

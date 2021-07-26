# -*- coding: utf-8 -*-
from datetime import datetime
from tipsarena_core.extratores.flash_score import navegador_web
from tipsarena_core.services import log_service as log, auth_service
from tipsarena_core.utils import html_utils, hash_utils, string_utils
from tipsarena_core.models.item_extracao import ItemExtracao


def extrairHtmlPaises() -> ItemExtracao:
  try:
    CSS_LISTA_PAISES = "body"
    CSS_VERIFICAR_CARREGAMENTO = "#category-left-menu"
    CSS_LISTAR_MAIS_PAISES = "[class^=itemMore_]"

    TIPO_EXTRACAO = "HTML_LISTA_PAISES"
    url = f"{navegador_web.URL_BASE}/futebol/"
    urlHash = hash_utils.gerarHash(url)
    navegador_web.navegar(url)

    elementoListaMaisPaises = navegador_web.obterElementoAposCarregamento(CSS_LISTAR_MAIS_PAISES)

    elementoListaMaisPaises.click()

    navegador_web.obterElementoAposCarregamento(CSS_VERIFICAR_CARREGAMENTO)
    htmlListaPaises = navegador_web.obterElementoAposCarregamento(CSS_LISTA_PAISES)

    id = auth_service.gerarIdentificadorUniversal()
    dataHoraExtracao = datetime.now()

    metadados = {
      "url": url,
      "url_hash": urlHash,
      "tipo_extracao": TIPO_EXTRACAO
    }

    htmlFinal = html_utils.incluirMetadadosHtml(htmlListaPaises.get_attribute("outerHTML"), metadados)

    return ItemExtracao(
      {
        "id": id,
        "url": url,
        "urlHash": urlHash,
        "tipo": TIPO_EXTRACAO,
        "dataHora": dataHoraExtracao,
        "html": string_utils.limparString(str(htmlFinal)),
        "nomeArquivo": f"ps-{urlHash.lower()}.html"
      })



  except Exception as e:
    log.ERRO("Não foi possível extrair lista de países.", e.args)
    navegador_web.capturarTela()
    return None


if __name__ == "__main__":
  extrairHtmlPaises()

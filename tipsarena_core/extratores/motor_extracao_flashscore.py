import json

from tipsarena_core.extratores.flash_score import extrator_pais
from tipsarena_core import gerenciador_filas
from tipsarena_core.enums.enum_fila import Fila as FILA


def extrairHtmlPaises():
  htmlPaises = extrator_pais.extrairHtmlPaises()
  gerenciador_filas.produzirMensagem(FILA.FILA_PROCESSAMENTO_HTML_PAISES, json.dumps(htmlPaises))

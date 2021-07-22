# -*- coding: utf-8 -*-

from datetime import datetime

from tipsarena_core.models.Competicao import Competicao
from tipsarena_core import repositorio
from tipsarena_core.utils import hash_utils, logUtils as log

NOME_COLECAO = "competicoes"

OPCOES_FILTRO = {
  "pais": []
}

OPCOES_ORDENACAO = [{
  "dataCadastro": -1,
  "dataAtualizacao": -1
}]


def salvarCompeticao(competicao: dict):
  try:
    competicao["dataAtualizacao"] = datetime.utcnow()
    competicao["_id"] = hash_utils.gerarHash(competicao["url"])

    return repositorio.inserirDocumentoCasoNaoExista(NOME_COLECAO, competicao, {"_id": competicao.get("_id")})

  except Exception as e:
    log.imprimirMensagem("ERRO", "Não foi possível salvar item de extração [{}]".format(competicao.get("url")), e.args)
    return None


def obterCompeticaoPorId(id):
  try:
    return repositorio.obterDocumentoPorId(NOME_COLECAO, id)
  except Exception as e:
    log.imprimirMensagem("ERRO",
                         "Não foi possível obter competição pelo ID:.".format(id),
                         e.args)
    return None
    return None

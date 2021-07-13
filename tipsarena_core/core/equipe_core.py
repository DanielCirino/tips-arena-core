# -*- coding: utf-8 -*-

from datetime import datetime

from tipsarena_core.models.Equipe import Equipe
from tipsarena_core.repository import mongodb
from tipsarena_core.utils import hash_utils, logUtils as log

NOME_COLECAO = 'equipes'

OPCOES_FILTRO = {
  "pais": []
}

OPCOES_ORDENACAO = [{
  "dataCadastro": -1,
  "dataAtualizacao": -1
}]


def salvarEquipe(equipe: dict):
  try:
    equipe["dataAtualizacao"] = datetime.utcnow()
    equipe["_id"] = hash_utils.gerarHash(equipe["url"])

    return mongodb.inserirDocumentoCasoNaoExista(NOME_COLECAO, equipe, {"_id": equipe.get("_id")})
  except Exception as e:
    log.imprimirMensagem("ERRO", "Não foi possível salvar equipe [{}]".format(equipe.get("url")), e.args)
    return None


def obterEquipePorId(id):
  try:
    return mongodb.obterDocumentoPorId(NOME_COLECAO, id)
  except Exception as e:
    log.imprimirMensagem("ERRO",
                         "Não foi possível obter equipe pelo ID:.".format(id),
                         e.args)
    return None
    return None

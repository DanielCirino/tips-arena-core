# -*- coding: utf-8 -*-

from datetime import datetime

from tipsarena_core import repositorio
from tipsarena_core.utils import logUtils as log

NOME_COLECAO = "controle_extracao"
OPCOES_FILTRO = {
  "idPai": "",
  "url": "",
  "tipo": [],
  "status": [],
  "prioridadeExtracao":[]
}
OPCOES_ORDENACAO = [{
  "prioridadeExtracao": 1,
}]

def criarIndicesControleExtracao():
  indicesArquivo = [
    (("prioridadeExtracao", repositorio.ASCENDING), False),
    (("tipo", repositorio.ASCENDING), False),
    (("status", repositorio.ASCENDING), False),
  ]

  for indice in indicesArquivo:
    repositorio.criarIndice(NOME_COLECAO, indice[0], indice[1])


def salvarItemExtracao(itemExtracao:dict):
  try:
    itemExtracao["dataAtualizacao"] = datetime.utcnow()
    return repositorio.iserirDocumentoCasoNaoExista(NOME_COLECAO, itemExtracao, {"_id": itemExtracao.get("_id")})
  except Exception as e:
    log.imprimirMensagem("ERRO", "Não foi possível salvar item de extração [{}]".format(itemExtracao["url"]), e.args)
    return None


def salvarItemsExtracaoEmLote(listaItensExtracao):
  try:
    for item in listaItensExtracao:
      item["dataAtualizacao"] = datetime.utcnow()

    return repositorio.iserirVariosDocumentosCasoNaoExistam(NOME_COLECAO, listaItensExtracao, "_id")

  except Exception as e:

    log.imprimirMensagem("ERRO",
                         "Não foi possível salvar {} itens de extração em lote.".format(len(listaItensExtracao)),
                         e.args)
    return None


def obterItemExtracaoPorId(id):
  try:
    return repositorio.obterDocumentoPorId(NOME_COLECAO, id)
  except Exception as e:
    log.imprimirMensagem("ERRO",
                         "Não foi possível obter itens de extração pelo ID:.".format(id),
                         e.args)
    return None


def obterItensExtracaoPorTipo(tipo, status):
  try:
    filtros = OPCOES_FILTRO.copy()

    filtros["tipo"].append(tipo)
    filtros["status"].append(status)

    return listarItensExtracao(filtros, OPCOES_ORDENACAO)
  except Exception as e:
    log.imprimirMensagem("ERRO",
                         "Não foi possível obter itens de extração pelo ID:{}.".format(id),
                         e.args)
    return None


def listarItensExtracao(filtros={}, ordenacao=[], limite=0, offset=0):
  try:
    if filtros != {}:
      if filtros["idPai"] == "":
        del filtros["idPai"]

      if filtros["url"] == "":
        del filtros["url"]

      if filtros["tipo"] == "":
        del filtros["tipo"]
      else:
        filtros["tipo"] = {"$in": filtros["tipo"]}

      if filtros["status"] == "":
        del filtros["status"]
      else:
        filtros["status"] = {"$in": filtros["status"]}

      if filtros["prioridadeExtracao"] == "":
        del filtros["status"]
      else:
        filtros["prioridadeExtracao"] = {"$in": filtros["prioridadeExtracao"]}

    return repositorio.listarDocumentos(NOME_COLECAO,
                                    filtros, ordenacao, limite, offset)
  except Exception as e:
    log.imprimirMensagem("ERRO",
                         "Não foi possível obter lista de itens de extração. Filtros:{}.".format(filtros),
                         e.args)
    return None

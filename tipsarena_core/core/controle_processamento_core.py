# -*- coding: utf-8 -*-
from datetime import datetime

from tipsarena_core.models.Processamento import Processamento
from tipsarena_core.models.ItemExtracao import ItemExtracao
from tipsarena_core.repository import mongodb

NOME_COLECAO = "controle_processamento"
OPCOES_FILTRO = {
  "dataInicio": "",
  "dataFim": "",
  "tipo": [],
  "status": []
}
OPCOES_ORDENACAO = [
  {"dataInicio": -1}
]


def obterProcessamentoPorId(id):
  doc = mongodb.obterDocumentoPorId(NOME_COLECAO, id)
  if doc is not None:
    return Processamento(doc)
  else:
    return Processamento()


def obterScrapWorksPorTipo(tipo, status):
  filtros = OPCOES_FILTRO.copy()
  filtros["tipo"].append(tipo)
  filtros["status"].append(status)

  ordenacao = OPCOES_ORDENACAO.copy()

  return listScrapWorks(filtros, ordenacao)


def listScrapWorks(filtros={}, sort=[], limit=0, skip=0):
  listaScraps = []
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

  docs = mongodb.listar_documentos(NOME_COLECAO, filtros, [("prioridadeExtracao", 1)], limit, skip)

  for doc in docs:
    listaScraps.append(ItemExtracao(doc))

  return listaScraps


def salvarProcessamento(processamento: Processamento):
  try:
    processamento.dataAtualizacao = datetime.utcnow()
    if processamento._id == "":
      delattr(processamento, "_id")
      return mongodb.inserirDocumento(NOME_COLECAO, processamento)
    else:
      return mongodb.atualizarDocumento(NOME_COLECAO, processamento)
  except Exception as e:
    print(e.args)
    return None

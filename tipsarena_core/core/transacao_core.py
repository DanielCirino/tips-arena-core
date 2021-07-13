# -*- coding: utf-8 -*-

from datetime import datetime

from bson import ObjectId

from tipsarena_core.models.Transacao import Transacao
from tipsarena_core.repository import mongodb
from tipsarena_core.utils import logUtils as log

NOME_COLECAO = 'transacoes'

OPCOES_FILTRO = {
  "idUsuario": "",
  "dataCadastroInicio": "",
  "dataCadastroFim": "",
  "tipo": [],
  "operacao": [],
  "efetivado": ""
}

OPCOES_ORDENACAO = {
  "dataCadastro": -1,
  "dataAtualizacao": -1
}


def salvarTransacao(transacao: Transacao):
  try:
    transacao.dataAtualizacao = datetime.now()
    if transacao._id == "":
      delattr(transacao, "_id")
      transacao.idUsuario = ObjectId(transacao.idUsuario)
      transacao.dataCadastro = datetime.now()
      return mongodb.inserirDocumento(NOME_COLECAO, transacao)
    else:
      return mongodb.atualizarDocumento(NOME_COLECAO, transacao)
  except Exception as e:
    log.imprimirMensagem("ERRO", "Não foi possível salvar transação **{}**.".format(transacao), e.args)
    return False


def obterTransacaoPorId(id):
  doc = mongodb.obterDocumentoPorId(NOME_COLECAO,id)
  if doc is not None:
    return Transacao(doc)
  else:
    return Transacao()


def listarTransacoes(filtros={}, ordenacao=[], limite=0, offset=0):
  try:
    filtroDataCadastro = {}

    if filtros != {}:
      if filtros["idUsuario"] == "":
        del filtros["idUsuario"]

      if filtros["efetivado"] == "":
        del filtros["efetivado"]

      if filtros["dataCadastroInicio"] != "":
        filtroDataCadastro["$gte"] = filtros["dataCadastroInicio"]

      del filtros["dataCadastroInicio"]

      if filtros["dataCadastroFim"] != "":
        filtroDataCadastro["$lte"] = filtros["dataCadastroFim"]

      del filtros["dataCadastroFim"]

      if len(filtros["mercado"]) == 0:
        del filtros["mercado"]
      else:
        filtros["mercado"] = {"$in": filtros["mercado"]}

      if len(filtros["status"]) == 0:
        del filtros["status"]
      else:
        filtros["status"] = {"$in": filtros["status"]}

      filtros["dataCadastro"] = filtroDataCadastro

    return mongodb.listarDocumentos(NOME_COLECAO, filtros, [("dataCadastro", -1)], limite, offset)
  except Exception as e:
    log.imprimirMensagem("ERRO", "Não foi possível listar transações.", e.args)
    return None

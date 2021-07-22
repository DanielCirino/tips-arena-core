# -*- coding: utf-8 -*-

from datetime import datetime

from tipsarena_core.core import aposta_core
from tipsarena_core.models.Partida import Partida
from tipsarena_core import repositorio
from tipsarena_core.utils import hash_utils, logUtils as log

NOME_COLECAO = 'partidas'
OPCOES_FILTRO = {
  "idEdicaoCompeticao": "",
  "status": [],
  "dataHora": [],
  "dataHoraInicio": "",
  "dataHoraFim": ""
}

OPCOES_ORDENACAO = [{
  "dataHora": -1,
  "dataCadastro": -1,
  "dataAtualizacao": -1
}]


def salvarPartida(partida: dict):
  try:
    partida["dataAtualizacao"] = datetime.utcnow()
    partida["_id"] = hash_utils.gerarHash(partida["url"])

    return repositorio.iserirDocumentoCasoNaoExista(NOME_COLECAO, partida, {"_id": partida.get("_id")})
  except Exception as e:
    log.imprimirMensagem("ERRO", "Não foi possível salvar partida [{}]".format(partida.get("url")), e.args)
    return None


def obterPartidaPorId(id):
  try:
    return repositorio.obterDocumentoPorId(NOME_COLECAO, id)
  except Exception as e:
    log.imprimirMensagem("ERRO",
                         "Não foi possível obter partida pelo ID:.".format(id),
                         e.args)
    return None


def listPartidas(filtros={}, ordenacao=[], limite=0, offset=0):
  try:

    filtroDataHora = {}

    if filtros != {}:
      if filtros["idEdicaoCompeticao"] == "":
        del filtros["idEdicaoCompeticao"]

      if filtros["dataHoraInicio"] != "":
        filtroDataHora["$gte"] = filtros["dataHoraInicio"]

      del filtros["dataHoraInicio"]

      if filtros["dataHoraFim"] != "":
        filtroDataHora["$lte"] = filtros["dataHoraFim"]

      del filtros["dataHoraFim"]

      if len(filtros["status"]) == 0:
        del filtros["status"]
      else:
        filtros["status"] = {"$in": filtros["status"]}

      if filtros["dataHora"] != {}:
        filtros["dataHora"] = filtroDataHora

    return repositorio.listarDocumentos(NOME_COLECAO, filtros, [("dataHora", -1)], limite, offset)

  except Exception as e:
    log.imprimirMensagem("ERRO",
                         "Não foi possível obter lista de partidas. Filtros:{}.".format(filtros),
                         e.args)
    return None


def analisarAlteracoesPartida(partida: Partida, partidaAtualizada: Partida):
  try:
    listaAlteracoes = []
    partida = partida.__dict__
    partidaAtualizada = partidaAtualizada.__dict__

    for key in partida:
      if partida[key] != partidaAtualizada[key]:
        listaAlteracoes.append(
          {"campo": key,
           "valorAnterior": partida[key],
           "valorNovo": partidaAtualizada[key]})

    return listaAlteracoes
  except Exception as e:
    log.imprimirMensagem("ERRO",
                         "Não foi possível analisar alterações na partida [{}].".format(partida.get("url")),
                         e.args)
    return None


def processarAlteracoesPartida(partida: Partida, alteracoes):
  try:
    for alteracao in alteracoes:
      if alteracao["campo"] == "status":
        if alteracao["valorNovo"] == Partida.Status.FINALIZADO.name:
          aposta_core.finalizarApostasPartida(partida)
      if alteracao["campo"] == "placarFinal":
        aposta_core.finalizarApostasPartida(partida)

  except Exception as e:
    log.imprimirMensagem("ERRO",
                         "Não foi possível processar alterações na partida [{}].".format(partida.get("url")),
                         e.args)

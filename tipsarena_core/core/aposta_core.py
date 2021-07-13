# -*- coding: utf-8 -*-

from datetime import datetime

from bson import ObjectId

from tipsarena_core.core import transacao_core
from tipsarena_core.models.Aposta import Aposta
from tipsarena_core.models.Partida import Partida
from tipsarena_core.models.Transacao import Transacao
from tipsarena_core.repository import mongodb

NOME_COLECAO = 'apostas'
OPCOES_FILTRO = {
  "idUsuario": "",
  "idPartida": "",
  "dataCadastroInicio": "",
  "dataCadastroFim": "",
  "status": [],
  "mercado": []
}

OPCOES_ORDENACAO = {
  "dataCadastro": -1,
  "dataAtualizacao": -1
}

def criarIndicesApostas():
  indicesArquivo = [
    (("idUsuario", mongodb.ASCENDING), False),
    (("idPartida", mongodb.ASCENDING), False),
  ]

  for indice in indicesArquivo:
    mongodb.criarIndice(NOME_COLECAO, indice[0], indice[1])


def salvarAposta(aposta: Aposta):
  try:
    aposta.dataAtualizacao = datetime.utcnow()
    if aposta._id == "":
      delattr(aposta, "_id")
      aposta.idUsuario = ObjectId(aposta.idUsuario)
      aposta.dataCadastro = datetime.utcnow()
      return mongodb.inserirDocumento(NOME_COLECAO,aposta)
    else:
      return mongodb.atualizarDocumento(NOME_COLECAO,aposta)
  except Exception as e:
    print(e.args)
    return False


def obterApostaPorId(id):
  doc = mongodb.obterDocumentoPorId(NOME_COLECAO,id)
  if doc is not None:
    return Aposta(doc)
  else:
    return Aposta()


def listarApostas(filtros={}, ordenacao=[], limite=0, offset=0):
  try:
    filtroDataCadastro = {}

    if filtros != {}:
      if filtros["idUsuario"] == "":
        del filtros["idUsuario"]

      if filtros["idPartida"] == "":
        del filtros["idPartida"]

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

      if filtroDataCadastro != {}:
        filtros["dataCadastro"] = filtroDataCadastro

    return mongodb.listarDocumentos(NOME_COLECAO, filtros, [("dataCadastro", -1)], limite, offset)

  except Exception as e:
    print(e.args)
    return None


def analisarResultadoPartida(placarMandante: int, placarVisitante: int):
  analise = {
    "resultado": "",
    "drawNoBet": "ANULA_APOSTA",
    "duplaChance": "",
    "imparPar": "",
    "btts": "",
    "underOver": [],
    "placar": "PLACAR_{}_{}".format(placarMandante, placarVisitante),
  }
  try:
    totalGols = placarMandante + placarVisitante

    if placarMandante == placarVisitante:
      analise["resultado"] = "EMPATE"

    elif placarMandante > placarVisitante:
      analise["resultado"] = "VITORIA_MANDANTE"
      analise["drawNoBet"] = "DNB_MANDANTE"
    else:
      analise["resultado"] = "VITORIA_VISITANTE"
      analise["drawNoBet"] = "DNB_VISITANTE"

    if analise["resultado"] == "EMPATE" or analise["resultado"] == "VITORIA_MANDANTE":
      analise["duplaChance"] = "CONTRA_VISITANTE"
    elif analise["resultado"] == "EMPATE" or analise["resultado"] == "VITORIA_VISITANTE":
      analise["duplaChance"] = "CONTRA_MANDANTE"
    elif analise["resultado"] == "VITORIA_MANDANTE" or analise["resultado"] == "VITORIA_VISITANTE":
      analise["duplaChance"] = "CONTRA_EMPATE"

    analise["imparPar"] = "EVEN" if totalGols % 2 == 0 else "ODD"

    if placarMandante > 0 and placarVisitante > 0:
      analise["btts"] = "BTTS_YES"
    else:
      analise["btts"] = "BTTS_NO"

    analise["totalGols"] = totalGols

    return analise

  except Exception as e:
    print("[ERRO] Erro análise resultado da partida: [{}]".format(e.argsp[0]))
    return None


def finalizarApostasPartida(partida: Partida):
  try:
    filtrosAposta = OPCOES_FILTRO.copy()
    filtrosAposta["idPartida"] = partida._id
    filtrosAposta["status"].append(Aposta.Status.PENDENTE.name)

    apostasPartida = listarApostas(filtrosAposta)

    for aposta in apostasPartida:
      finalizarApostaPartida(aposta)

  except Exception as e:
    print(e.args[0])


def finalizarApostaPartida(aposta):
  try:
    from tipsarena_core.core.partida_core import PartidaCore
    partida = PartidaCore().obterPartidaPorId(aposta.idPartida)
    placarPartida = partida.placarFinal.split(":")
    analiseResultado = analisarResultadoPartida(int(placarPartida[0]), int(placarPartida[1]))

    if analiseResultado != None:
      if (partida.status == Partida.Status.FINALIZADO.name):
        if aposta.mercado == Aposta.Mercados.RESULT.name:
          finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["resultado"])

        if aposta.mercado == Aposta.Mercados.DNB.name:
          if analiseResultado["drawNoBet"] == "ANULA_APOSTA":
            cancelarAposta(aposta)
          else:
            finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["drawNoBet"])

        if aposta.mercado == Aposta.Mercados.DOUBLE_CHANCE.name:
          finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["duplaChance"])

        if aposta.mercado == Aposta.Mercados.BTTS.name:
          finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["btts"])

        if aposta.mercado == Aposta.Mercados.ODD_EVEN.name:
          finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["imparPar"])

        if aposta.mercado == Aposta.Mercados.CORRECT_SCORE.name:
          finalizarAposta(aposta, aposta.opcaoMercado == analiseResultado["placar"])

        if aposta.mercado == Aposta.Mercados.UNDER_OVER.name:
          finalizarApostaUnderOver(aposta, analiseResultado["totalGols"])
      else:
        if aposta.mercado == Aposta.Mercados.CORRECT_SCORE.name:
          analisarApostaPlacarExato(aposta, int(placarPartida[0]), int(placarPartida[1]))

        if aposta.mercado == Aposta.Mercados.BTTS.name:
          analisarApostaBtts(aposta, int(placarPartida[0]), int(placarPartida[1]))

        if aposta.mercado == Aposta.Mercados.UNDER_OVER.name:
          analisarApostaUnderOver(aposta, analiseResultado["totalGols"])

  except Exception as e:
    print("Erro ao finalizar apostas partida:[{}]".format(e.args[0]))


def finalizarAposta(aposta: Aposta, apostaCerta):
  try:
    lucroAposta = (aposta.valor * aposta.valorOdd) - aposta.valor if apostaCerta else -aposta.valor
    resultadoAposta = Aposta.Resultado.LUCRO.name if apostaCerta else Aposta.Resultado.PREJUIZO.name

    # Salvar transacao da aposta em caso de acerto
    if apostaCerta:
      transacao = Transacao()
      transacao.idUsuario = aposta.idUsuario
      transacao.tipo = Transacao.Tipo.RESULTADO_APOSTA.name
      transacao.operacao = Transacao.Operacao.CREDITO.name
      transacao.descricao = "Muito bem \\0/. Você acertou a aposta {}.".format(aposta.descricao)
      transacao.valor = round(aposta.valor * aposta.valorOdd, 2)

      transacaoSalva = transacao_core.salvarTransacao(transacao)
      print(transacaoSalva.inserted_id)

    aposta.lucro = round(lucroAposta, 2)
    aposta.resultado = resultadoAposta
    aposta.status = Aposta.Status.FINALIZADA.name
    salvarAposta(aposta)

  except Exception as e:
    print(e.args)


def analisarApostaPlacarExato(aposta, placarMandante: int, placarVisitante: int):
  try:
    detalhesAposta = aposta.opcaoMercado.split("_")
    finalizarAposta = int(detalhesAposta[1]) < placarMandante or int(detalhesAposta[2]) < placarVisitante

    if finalizarAposta:
      finalizarAposta(aposta, False)

  except Exception as e:
    print(e.args[0])


def finalizarApostaUnderOver(aposta: Aposta, totalGols: int):
  try:
    detalhesAposta = aposta.opcaoMercado.split("_")  # UNDER_4_5
    totalGolsAposta = int(detalhesAposta[1])

    if detalhesAposta[0] == "UNDER":
      apostaCerta = totalGols <= totalGolsAposta
    if detalhesAposta[0] == "OVER":
      apostaCerta = totalGols > totalGolsAposta

    finalizarAposta(aposta, apostaCerta)

  except Exception as e:
    print(e.args[0])


def analisarApostaUnderOver(aposta: Aposta, totalGols: int):
  try:
    detalhesAposta = aposta.opcaoMercado.split("_")  # UNDER_1_5
    finalizarAposta = totalGols > int(detalhesAposta[1])

    if finalizarAposta:
      apostaCerta = detalhesAposta[0] == "OVER"
      finalizarAposta(aposta, apostaCerta)

  except Exception as e:
    print(e.args[0])


def analisarApostaBtts(aposta, placarMandante: int, placarVisitante: int):
  try:
    ambosMarcaram = placarMandante > 0 and placarVisitante > 0

    if ambosMarcaram:
      apostaCerta = (aposta.opcaoMercado == "BTTS_YES")
      finalizarAposta(aposta, apostaCerta)

  except Exception as e:
    print(e.args[0])


def cancelarAposta(aposta: Aposta):
  try:
    transacao = Transacao()
    transacao.idUsuario = aposta.idUsuario
    transacao.tipo = Transacao.Tipo.CANCELAMENTO_APOSTA.name
    transacao.operacao = Transacao.Operacao.CREDITO.name
    transacao.descricao = "Apota cancelada: {}".format(aposta.descricao)
    transacao.valor = aposta.valor
    transacao.efetivado = True

    transacaoSalva = transacao_core.salvarTransacao(transacao)
    # print(transacaoSalva.inserted_id)

    if transacaoSalva:
      aposta.resultado = Aposta.Resultado.CANCELADA.name
      aposta.status = Aposta.Status.CANCELADA.name
      salvarAposta(aposta)

  except Exception as e:
    print(e.args[0])

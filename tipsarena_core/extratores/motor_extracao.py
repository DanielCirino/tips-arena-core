# -*- coding: utf-8 -*-

from multiprocessing import Pool, cpu_count
from datetime import datetime
from progress.bar import Bar

from tipsarena_core.core import item_extracao_core
from tipsarena_core.utils import hash_utils
from tipsarena_core.services import log_service as log
from tipsarena_core.extratores.flash_score import extrator_partida, navegador_web, extrator_competicao, extrator_equipe, \
  extrator_pais
from tipsarena_core.enums.enum_extracao import TIPO as TIPO_EXTRACAO, STATUS as STATUS_EXTRACAO

INDICADOR_PROGRESSO = '%(percent).1f%% | %(elapsed)ds | %(index)d de %(max)d'


def salvarItemExtracao(url, prioridade: int, tipo: str, status: str, idPai=None):
  try:
    itemExtracao = {
      "_id": hash_utils.gerarHash(url),
      "url": url,
      "tipo": tipo,
      "idPai": idPai,
      "status": status,
      "prioridadeExtracao": prioridade
    }
    return item_extracao_core.salvarItemExtracao(itemExtracao)

  except Exception as e:
    log.ERRO("Não foi possível salvar item de extração [{}].".format(url),
             e.args)
    return None


def salvarListaItensExtracao(listaUrls, status: str, tipo: str, idPai=None):
  try:
    itensExtracao = []
    for item in listaUrls:
      itensExtracao.append({
        "_id": hash_utils.gerarHash(item["url"]),
        "url": item["url"],
        "tipo": tipo,
        "idPai": idPai,
        "status": status,
        "prioridadeExtracao": item["sequencial"]
      })
    return item_extracao_core.salvarItemsExtracaoEmLote(itensExtracao)
  except Exception as e:
    log.ERRO(f"Não foi possível salvar lista de itens de extração. Total itens:{len(listaUrls)}.", e.args)
    return None


def prepararListaParaProcessamento(lista):
  for item in lista:
    yield item


def obterItemProcessamentoPaises():
  try:
    filtros = item_extracao_core.OPCOES_FILTRO.copy()
    filtros["tipo"] = [TIPO_EXTRACAO.PAIS.name]
    filtros["status"] = [STATUS_EXTRACAO.EXTRACAO_COMPETICOES.name]

    itensExtracao = item_extracao_core.listarItensExtracao(filtros, [("prioridadeExtracao", 1)])
    for item in itensExtracao:
      yield item

  except Exception as e:
    log.ERRO("Não foi possível obter lista de países para processamento.", e.args)


def extrairItensProcessamentoCompeticao(itemProcessamentoPais):
  try:
    itemProcessamentoPais["status"] = STATUS_EXTRACAO.PROCESSANDO.name
    item_extracao_core.salvarItemExtracao(itemProcessamentoPais)

    itensProcessamento = extrator_competicao.extrairHtmlCompeticoesPais(itemProcessamentoPais["url"])
    resultado = salvarListaItensExtracao(itensProcessamento,
                                         STATUS_EXTRACAO.EXTRACAO_EDICOES_COMPETICAO.name,
                                         TIPO_EXTRACAO.COMPETICAO.name, itemProcessamentoPais["_id"])

    itemProcessamentoPais["status"] = STATUS_EXTRACAO.OK.name

    return (itemProcessamentoPais, len(itensProcessamento))
  except Exception as e:
    log.ERRO(f"Erro ao extrair itens processamento do pais {itemProcessamentoPais['url']}", e.args)
    return None


def extrairItensProcessamentoEdicoesCompeticao(itemProcessamentoCompeticao):
  try:
    itemProcessamentoCompeticao["status"] = STATUS_EXTRACAO.PROCESSANDO.name
    item_extracao_core.salvarItemExtracao(itemProcessamentoCompeticao)

    itensProcessamento = extrator_competicao.extrairHtmlEdicoesCompeticao(itemProcessamentoCompeticao["url"])
    resultado = salvarListaItensExtracao(itensProcessamento,
                                         STATUS_EXTRACAO.EXTRACAO_PARTIDAS.name,
                                         TIPO_EXTRACAO.EDICAO_COMPETICAO.name, itemProcessamentoCompeticao["_id"])

    itemProcessamentoCompeticao["status"] = STATUS_EXTRACAO.OK.name

    return (itemProcessamentoCompeticao, len(itensProcessamento))
  except Exception as e:
    log.ERRO(f"Erro ao extrair itens processamento da competição {itemProcessamentoCompeticao['url']}", e.args)
    return None


def extrairItensProcessamentoEquipes(itemProcessamentoEdicao):
  try:
    itemProcessamentoEdicao["status"] = STATUS_EXTRACAO.PROCESSANDO.name
    item_extracao_core.salvarItemExtracao(itemProcessamentoEdicao)

    navegador = navegador_web.obterNavegadorWeb()
    navegador.get(navegador_web.URL_BASE + itemProcessamentoEdicao["url"])

    itensProcessamento = extrator_equipe.extrairHtmlEquipesEdicaoCompeticao(navegador)
    if itensProcessamento is None:
      itemProcessamentoEdicao["status"] = STATUS_EXTRACAO.EXTRACAO_PARTIDAS.name
      return (itemProcessamentoEdicao, 0)

    resultado = salvarListaItensExtracao(itensProcessamento,
                                         STATUS_EXTRACAO.AGUARDANDO_EXTRACAO.name,
                                         TIPO_EXTRACAO.EQUIPE.name, itemProcessamentoEdicao["_id"])

    itemProcessamentoEdicao["status"] = STATUS_EXTRACAO.EXTRACAO_PARTIDAS.name

    return (itemProcessamentoEdicao, len(itensProcessamento))
  except Exception as e:
    navegador.quit()
    log.ERRO(f"Erro ao extrair itens processamento da edição da competição {itemProcessamentoEdicao['url']}", e.args)
    return None


def extrairItensProcessamentoPartidas(itemProcessamentoEdicao):
  try:

    itemProcessamentoEdicao["status"] = STATUS_EXTRACAO.PROCESSANDO.name
    item_extracao_core.salvarItemExtracao(itemProcessamentoEdicao)

    listaPartidas = extrator_partida.extrairHtmlPartidasEdicaoCompeticao(itemProcessamentoEdicao["url"])

    if listaPartidas is None:
      itemProcessamentoEdicao["status"] = STATUS_EXTRACAO.ERRO.name
      return (itemProcessamentoEdicao, 0)

    itensProcessamento = listaPartidas["agendadas"] + listaPartidas["finalizadas"]
    resultado = salvarListaItensExtracao(itensProcessamento,
                                         STATUS_EXTRACAO.AGUARDANDO_EXTRACAO.name,
                                         TIPO_EXTRACAO.PARTIDA.name, itemProcessamentoEdicao["_id"])

    itemProcessamentoEdicao["status"] = STATUS_EXTRACAO.AGUARDANDO_EXTRACAO.name

    return (itemProcessamentoEdicao, len(itensProcessamento))
  except Exception as e:
    log.ERRO(f"Não foi possível extrair itens processamento de partidas. [{itemProcessamentoEdicao['url']}]", e.args)
    return None


def atualizarQuantidadeItemsFilhos(itemExtracao, quantidade):
  try:
    itemExtracao["quantidadeFilhos"] = quantidade
    item_extracao_core.salvarItemExtracao(itemExtracao)
  except Exception as e:
    log.ERRO(f"Erro ao atualizar quantidade de itens filhos. [{itemExtracao['url']}]", e.args)


def extrairPaises():
  try:
    listaPaises = extrator_pais.extrairHtmlPaises()
    barraProgresso = Bar('Extraindo lista de países:',
                         max=len(listaPaises),
                         suffix=INDICADOR_PROGRESSO, fill='=')

    dataHoraInicio = datetime.now()

    for item in listaPaises:
      salvarItemExtracao(item["url"],
                         item["sequencial"],
                         TIPO_EXTRACAO.PAIS.name,
                         STATUS_EXTRACAO.EXTRACAO_COMPETICOES.name)
      barraProgresso.next()

    log.OK(
      f"Extração de {len(listaPaises)} países finalizada com sucesso. Início:{dataHoraInicio} - Fim: {datetime.now()}")

  except Exception as e:
    log.ERRO("Não foi possível extrair países.", e.args)


def processarExtracaoCompeticoes():
  try:
    numeroProcessos = cpu_count() - 1
    dataHoraInicio = datetime.now()
    filtros = item_extracao_core.OPCOES_FILTRO.copy()
    filtros["tipo"] = [TIPO_EXTRACAO.PAIS.name]
    filtros["status"] = [STATUS_EXTRACAO.EXTRACAO_COMPETICOES.name]

    listaProcessamento = item_extracao_core.listarItensExtracao(filtros, [("prioridadeExtracao", 1)])

    barraProgresso = Bar('Extraindo competições dos países. [{} processos]:'.format(numeroProcessos),
                         max=len(listaProcessamento),
                         suffix=INDICADOR_PROGRESSO, fill='=')

    with Pool(processes=numeroProcessos) as pool:
      # pool.map(extrairItensProcessamentoCompeticao,listaProcessamento)
      jobs = []
      for item in prepararListaParaProcessamento(listaProcessamento):
        jobs.append(
          pool.apply_async(extrairItensProcessamentoCompeticao, (item,))
        )

      contadorCompeticoes = 0

      for job in jobs:
        itemProcessamentoPais, quantidadeProcessada = job.get()
        contadorCompeticoes += quantidadeProcessada
        atualizarQuantidadeItemsFilhos(itemProcessamentoPais, quantidadeProcessada)
        barraProgresso.next()

    log.OK(
      f"Extração de competições finalizada com sucesso. Total países: "
      f"{len(listaProcessamento)}. Total competições:{contadorCompeticoes}. "
      f"Início:[{dataHoraInicio}] - Fim:[{datetime.now()}]")

  except Exception as e:
    log.ERRO("Não foi possível extrair competições.", e.args)


def processarExtracaoEdicoesCompeticao():
  try:
    numeroProcessos = cpu_count() - 1

    with Pool(processes=numeroProcessos) as pool:
      dataHoraInicio = datetime.now()
      filtros = item_extracao_core.OPCOES_FILTRO.copy()
      filtros["tipo"] = [TIPO_EXTRACAO.COMPETICAO.name]
      filtros["status"] = [STATUS_EXTRACAO.OK.name, STATUS_EXTRACAO.PROCESSANDO.name]

      listaProcessamento = item_extracao_core.listarItensExtracao(filtros, [("prioridadeExtracao", 1)])
      barraProgresso = Bar('Extraindo edições das competições. [{} processos]:'.format(numeroProcessos),
                           max=len(listaProcessamento),
                           suffix=INDICADOR_PROGRESSO, fill='=')

      resultados = [
        pool.apply_async(extrairItensProcessamentoEdicoesCompeticao, (item,))
        for item in listaProcessamento]

      contadorEdicoes = 0

      for resultado in resultados:
        itemProcessamentoPais, quantidadeProcessada = resultado.get()
        contadorEdicoes += quantidadeProcessada
        atualizarQuantidadeItemsFilhos(itemProcessamentoPais, quantidadeProcessada)
        barraProgresso.next()

    log.OK(f"Extração de edições de competição finalizada com sucesso. "
           f"Total competições: {len(listaProcessamento)}. Total edições:{contadorEdicoes}. "
           f"Início:[{dataHoraInicio}] - Fim:[{datetime.now()}]")

  except Exception as e:
    log.ERRO("Não foi possível extrair edições competições.", e.args)


def processarExtracaoEquipes():
  try:
    numeroProcessos = cpu_count() - 1
    dataHoraInicio = datetime.now()
    filtros = item_extracao_core.OPCOES_FILTRO.copy()
    filtros["tipo"] = [TIPO_EXTRACAO.EDICAO_COMPETICAO.name]
    filtros["status"] = [STATUS_EXTRACAO.EXTRACAO_EQUIPES.name]

    listaProcessamento = item_extracao_core.listarItensExtracao(filtros, [("prioridadeExtracao", 1)])

    barraProgresso = Bar('Extraindo equipes das edições das competições. [{} processos]:'.format(numeroProcessos),
                         max=len(listaProcessamento),
                         suffix=INDICADOR_PROGRESSO, fill='=')

    with Pool(processes=numeroProcessos) as pool:
      jobs = []
      for item in prepararListaParaProcessamento(listaProcessamento):
        jobs.append(
          pool.apply_async(extrairItensProcessamentoEquipes, (item,))
        )

      contadorEquipes = 0

      for job in jobs:
        itemProcessamento, quantidadeProcessada = job.get()
        contadorEquipes += quantidadeProcessada
        atualizarQuantidadeItemsFilhos(itemProcessamento, quantidadeProcessada)
        barraProgresso.next()

    log.OK(
      f"Extração de equipes finalizada com sucesso. Total edições de competição: {len(listaProcessamento)}. Total equipes:{contadorEquipes}. Início:[{dataHoraInicio}] - Fim:[{datetime.now()}]")

  except Exception as e:
    log.ERRO("Não foi possível extrair equipes.", e.args)


def processarExtracaoPartidas():
  try:
    numeroProcessos = cpu_count() - 1

    with Pool(processes=numeroProcessos) as pool:
      dataHoraInicio = datetime.now()
      filtros = item_extracao_core.OPCOES_FILTRO.copy()
      filtros["tipo"] = [TIPO_EXTRACAO.EDICAO_COMPETICAO.name]
      filtros["status"] = [STATUS_EXTRACAO.EXTRACAO_PARTIDAS.name, STATUS_EXTRACAO.PROCESSANDO.name,
                           STATUS_EXTRACAO.OK.name]
      filtros["prioridadeExtracao"] = [5]

      listaProcessamento = item_extracao_core.listarItensExtracao(filtros, [("prioridadeExtracao", 1)])

      barraProgresso = Bar('Extraindo partidas das edições das competições. [{} processos]:'.format(numeroProcessos),
                           max=len(listaProcessamento),
                           suffix=INDICADOR_PROGRESSO, fill='=')
      resultados = [
        pool.apply_async(extrairItensProcessamentoPartidas, (item,))
        for item in listaProcessamento]

      contadorPartidas = 0

      for resultado in resultados:
        itemProcessamento, quantidadeProcessada = resultado.get()
        contadorPartidas += quantidadeProcessada
        atualizarQuantidadeItemsFilhos(itemProcessamento, quantidadeProcessada)
        barraProgresso.next()

    log.OK(
      f"Extração de partidas finalizada com sucesso. Total edições de competição: {len(listaProcessamento)}. Total partidas:{contadorPartidas}. Início:[{dataHoraInicio}] - Fim:[{datetime.now()}]")

  except Exception as e:
    log.ERRO("Não foi possível extrair partidas.", e.args)

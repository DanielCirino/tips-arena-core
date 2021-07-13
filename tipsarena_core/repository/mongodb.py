import os

from bson import ObjectId
from pymongo import MongoClient, UpdateOne, ASCENDING, DESCENDING
from pymongo.cursor import CursorType

from tipsarena_core.exceptions import database_errors
from tipsarena_core.services import log_service as log

client = MongoClient(os.getenv("TA_MONGODB_URI"))
database = client.get_database(os.getenv("TA_DATABASE"))


def inserirDocumento(nomeColecao: str, documento: any):
  try:
    doc = obterDocumentoNormalizado(documento)
    return database[nomeColecao].insert_one(doc)
  except Exception as e:
    log.ERRO("Não foi possível inserir documento na coleção '{}' **{}**.".format(nomeColecao, documento),
             e.args)
    raise database_errors.InserirDocumentoError(
      message="Não foi possível inserir documento na coleção '{}' **{}**.".format(nomeColecao, documento))


def atualizarDocumento(nomeColecao: str, documento: dict):
  try:
    doc = obterDocumentoNormalizado(documento)
    queryUpdate = {"_id": doc["_id"]}
    return database[nomeColecao].update_one(queryUpdate, {"$set": doc})

  except Exception as e:
    log.ERRO("Não foi possível atualizar documento na coleção '{}' **{}**.".format(nomeColecao, documento),
             e.args)
    raise database_errors.AtualizarDocumentoError(
      message="Não foi possível atualizar documento na coleção '{}' **{}**.".format(nomeColecao, documento))


def inserirOuAtualizarDocumento(nomeColecao, documento, filtro, valoresPadrao={}):
  try:
    doc = obterDocumentoNormalizado(documento)

    for key in valoresPadrao:
      if key in documento:
        del documento[key]

    return database[nomeColecao].update_one(filtro, {"$set": doc, "$setOnInsert": valoresPadrao}, upsert=True)

  except Exception as e:
    log.ERRO(f"Não foi possível inserir documento na coleção '{nomeColecao}' **{documento}**."
             .format(nomeColecao, documento), e.args)
    raise database_errors.InserirOuAtualizarDocumentoError(
      message="Erro ao inserir ou atualizar documento. [{}]".format(e.args))


def inserirVariosDocumentosCasoNaoExistam(nomeColecao, listaDocumentos, campoFiltro):
  try:
    listaAtualizacao = []
    for documento in listaDocumentos:
      doc = obterDocumentoNormalizado(documento)
      listaAtualizacao.append(UpdateOne({campoFiltro: doc.get(campoFiltro)}, {"$set": doc}, upsert=True))

    return database[nomeColecao].bulk_write(listaAtualizacao, ordered=False)
  except Exception as e:
    log.ERRO(f"Não foi possível inserir {len(listaDocumentos)} documentos na coleção '{nomeColecao}'.", e.args)
    database_errors.InserirOuAtualizarDocumentosEmLoteError(
      message=f"Não foi possível inserir {len(listaDocumentos)} documentos na coleção '{nomeColecao}' [{e.args}].")


def deletarDocumento(nomeColecao: str, id: str):
  try:
    filtro = {"_id": ObjectId(id)}
    return database[nomeColecao].delete_one(filtro)
  except Exception as e:
    log.ERRO("Não foi possível deletar documento com id '{}' da coleção '{}'."
             .format(id, nomeColecao), e.args)

    raise database_errors.DeletarDocumentoError(
      message="Não foi possível deletar documento com id '{}' da coleção '{}'."
        .format(id, nomeColecao))


def listarDocumentos(nomeColecao: str, filtros={}, ordenacao=[], limite=0, offset=0):
  try:
    cursor = database[nomeColecao].find(filtros)

    if ordenacao != []:
      print(ordenacao)
      cursor.sort(ordenacao)

    if limite == 0:
      cursor.limit(limite)

    if offset > 0:
      cursor.skip(offset)

    return list(cursor)
  except Exception as e:
    log.ERRO("Não foi possível listar documentos da coleção '{}'.".format(nomeColecao), e.args)
    raise database_errors.ListarDocumentosError(
      message="Não foi possível listar documentos da coleção '{}'.".format(nomeColecao))


def obterCursor(nomeColecao: str, filtros={}, ordenacao=[], qtdLinhasLote=1000):
  try:
    cursor = database[nomeColecao].find(cursor_type=CursorType.EXHAUST, batch_size=qtdLinhasLote)

    if ordenacao != []:
      print(ordenacao)
      cursor.sort(ordenacao)

    return cursor
  except Exception as e:
    log.ERRO("Não foi possível obter cursor para a coleção '{}'.".format(nomeColecao), e.args)
    raise database_errors.ListarDocumentosError(
      message="Não foi possível obter cursor para coleção '{}'.".format(nomeColecao))


def obterDocumentoPorId(nomeColecao: str, id: str):
  try:
    return database[nomeColecao].find_one({"_id": ObjectId(id)})
  except Exception as e:
    log.ERRO("Não foi possível encontrar o documento com o ID '{}' da coleção '{}'."
             .format(id, nomeColecao), e.args)
    raise database_errors.ObterDocumentoError(
      message="Não foi possível encontrar o documento com o ID '{}' da coleção '{}'."
        .format(id, nomeColecao))


def obterDocumentoPorChave(nomeColecao: str, chave: dict):
  try:
    return database[nomeColecao].find_one(chave)
  except Exception as e:
    log.ERRO("Não foi possível encontrar o documento com a chave '{}' da coleção '{}'."
             .format(chave, nomeColecao), e.args)
    raise database_errors.ObterDocumentoError(
      message="Não foi possível encontrar o documento com a chave '{}' da coleção '{}'."
        .format(chave, nomeColecao))


def obterDocumentoNormalizado(documento):
  if (hasattr(documento, "__dict__")):
    return documento.__dict__
  else:
    return documento


def pesquisarTexto(nomeColecao: str, texto: str, limite=10):
  try:
    cursor = database[nomeColecao].find({"$text": {"$search": texto}}).limit(limite)
    return list(cursor)
  except Exception as e:
    log.ERRO("Erro ao pesquisar texto '{}' na coleção [{}]".format(texto, nomeColecao), e.args)
    raise database_errors.PesquisaTextoError(
      message="Erro ao pesquisar texto '{}' na coleção [{}]".format(texto, nomeColecao))


def obterTotalDocumentos(nomeColecao: str, filtros={}):
  try:
    return database[nomeColecao].estimated_document_count()
  except Exception as e:
    log.ERRO("Não foi possível obter o total de documentos da coleção '{}'. [{}]"
             .format(nomeColecao), e.args)
    raise database_errors.ObterDocumentoError(
      message="Não foi possível obter o total de documentos da coleção '{}'."
        .format(nomeColecao))


def listarColecoes():
  return database.list_collection_names()


def excluirColecao(nomeColecao: str):
  try:
    database[nomeColecao].drop()
  except Exception as e:
    log.ERRO("Erro ao excluir coleção {}.".format(nomeColecao), e.args)


def testarConexao():
  """"
  Realiza um teste de conexão com o servidor de banco de dados
  """
  try:
    info = client.server_info()
    log.INFO("Servidor de banco de dados está em execução. Versao:{}".format(info["version"]))
    return True
  except Exception as e:
    log.ERRO("Teste de conexão falhou :(.", e.args)
    raise database_errors.ConexaoError(message="Teste de conexão falhou :(. Detalhes [{}]".format(e.args))


def fazerAgregacao(nomeColecao: str, pipeline, explain=False):
  try:
    if explain:
      return database.command("aggregate", nomeColecao, pipeline=pipeline, explain=explain, allowDiskUse=True)

    return database[nomeColecao].aggregate(pipeline=pipeline, allowDiskUse=True)

  except Exception as e:
    log.ERRO("Erro ao executar agregação dos dados. {}".format(e.args))
    raise database.AgregarDadosError(
      message="Erro ao executar agregação dos dados na coleção {}. **{}**".format(nomeColecao, e.args))


def listarOperacoesCorrentes():
  with client.admin.aggregate([{"$currentOp": {}}]) as cursor:
    for operation in cursor:
      log.INFO("[{}] [{}]".format(operation["opid"], operation["op"]))


def criarIndice(nomeColecao: str, indice: tuple, eUnico: bool):
  try:
    resultado = database[nomeColecao].create_index([indice], unique=eUnico)
    log.OK("Índice '{}' criado com sucesso na coleção '{}'!".format(resultado, nomeColecao.upper()))
  except Exception as e:
    log.ERRO("Erro ao criar indice [{}] na coleção {}. [{}]".format(
      indice[0],
      nomeColecao), e.args)
    raise database_errors.CriarIndiceError(message="Erro ao criar indice [{}] na coleção {}. [{}]".format(
      indice[0],
      nomeColecao))

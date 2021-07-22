from datetime import datetime

from tipsarena_core import repositorio

NOME_COLECAO = 'usuarios'


def criarIndicesUsuario():
  indicesAplicacao = [
    (("documento", repositorio.ASCENDING), True),
    (("email", repositorio.ASCENDING), True)
  ]

  for indice in indicesAplicacao:
    repositorio.criarIndice(NOME_COLECAO, indice[0], indice[1])


def salvarUsuario(usuario):
  try:
    usuario["dataAtualizacao"] = datetime.utcnow()
    filtro = {"documento": usuario.get("documento")}

    return repositorio.iserirOuAtualizarDocumento(NOME_COLECAO, usuario, filtro, {"dataCadastro": datetime.utcnow()})

  except Exception as e:
    print("Erro ao salvar usuario.[{}]".format(e.args))
    return None


def obterUsuarioPorEmail(email: str):
  try:
    return repositorio.obterDocumentoPorChave(NOME_COLECAO, {"email": email})
  except Exception as e:
    print("Erro ao obter usuario pelo E-mail {}. [{}]".format(
      email, e.args))
    return None


def obterUsuarioPorDocumento(documento: str):
  try:
    return repositorio.obterDocumentoPorChave(NOME_COLECAO, {"documento": documento})
  except Exception as e:
    print("Erro ao obter usuario por documento {}. [{}]".format(
      documento, e.args))
    return None


def listarUsuarios(filtros={}, ordenacao=[], limite=0, offset=0):
  lista = repositorio.listarDocumentos(NOME_COLECAO, filtros, ordenacao, limite, offset)
  return lista


def obterQuantidadeUsuarios():
  return repositorio.obterTotalDocumentos(NOME_COLECAO)


def excluirTodos():
  repositorio.excluirColecao(NOME_COLECAO)

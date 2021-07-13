from datetime import datetime

from tipsarena_core.repository import mongodb

NOME_COLECAO = 'usuarios'


def salvarUsuario(usuario):
  try:
    idUsuario = usuario.get("_id")
    eUsuarioNovo = idUsuario is None or idUsuario == ""

    usuario["dataAtualizacao"] = datetime.utcnow()

    if eUsuarioNovo:
      usuario["dataCadastro"] = datetime.utcnow()
      return mongodb.inserirDocumento(NOME_COLECAO, usuario)
    else:
      return mongodb.atualizarDocumento(NOME_COLECAO, usuario)

  except Exception as e:
    print("Erro ao salvar usuario.[{}]".format(e.args))
    return None

def obterUsuarioPorEmail(email: str):
  try:
    return mongodb.obterDocumentoPorChave(NOME_COLECAO, {"email": email})
  except Exception as e:
    print("Erro ao obter usuario pelo E-mail {}. [{}]".format(
      email, e.args))
    return None

def obterUsuarioPorDocumento(documento: str):
  try:
    return mongodb.obterDocumentoPorChave(NOME_COLECAO, {"documento": documento})
  except Exception as e:
    print("Erro ao obter usuario por documento {}. [{}]".format(
      documento, e.args))
    return None

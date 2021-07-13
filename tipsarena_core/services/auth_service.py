from datetime import datetime, timedelta
from uuid import uuid4, UUID

import bcrypt
import jwt

from tipsarena_core.exceptions.auth_erros import CriptografarSenhaError, GerarTokenSessaoError, TokenSessaoInvalidoError
from tipsarena_core.services import log_service as log

TEMPO_EXPIRACAO_TOKEN = {
  '24_HRS': 86400,
  '12_HRS': 43200,
  '6_HRS': 21600,
  '3_HRS': 10800,
  '90_MIN': 5400,
  '30_MIN': 1800,
  '15_MIN': 900,
  'MINIMO': 1
}


def criptografarSenha(senha: str):
  try:
    senhaCriptografada = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    return senhaCriptografada.decode()
  except Exception as e:
    raise CriptografarSenhaError(message="Erro ao criptograr senha. [{}]".format(e.args))


def compararSenha(senha: str, senhaCriptografada: str):
  return bcrypt.checkpw(senha.encode(), senhaCriptografada.encode())


def gerarTokenSessao(dadosToken: dict,
                     expiraEm: int):
  try:
    log.INFO("{} | {} | {} ".format(datetime.now(), datetime.now() + timedelta(seconds=expiraEm), expiraEm))
    dadosToken['exp'] = datetime.utcnow() + timedelta(seconds=expiraEm)
    return jwt.encode(dadosToken, 's3cr3t', algorithm="HS256")
  except Exception as e:
    log.ERRO("Erro ao gerar token de sessão. [{}]".format(e.args))
    raise GerarTokenSessaoError(message="Erro ao gerar token de sessão. [{}]".format(e.args))


def decodificarToken(token: str):
  try:
    dadosToken = jwt.decode(token, 's3cr3t', algorithms=["HS256"])
    return dadosToken
  except Exception as e:
    raise TokenSessaoInvalidoError(message="Erro ao decodificar token de sessão. [{}]".format(e.args))


def gerarIdentificadorUniversal():
  return str(uuid4()).upper()


def validarIdentificadorUniversal(identificador: str):
  try:
    uuid = UUID(identificador.lower(), version=4)
  except ValueError:
    return False

  return str(uuid) == identificador.lower()

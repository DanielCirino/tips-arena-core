import time

from tipsarena_core.services import auth_service


def test_gerar_token_sessao():
  token = auth_service.gerarTokenSessao(dadosToken={"dados": "teste"},
                                        expiraEm=auth_service.TEMPO_EXPIRACAO_TOKEN['15_MIN'])
  dadosToken = auth_service.decodificarToken(token)
  assert dadosToken["dados"] == "teste"


def test_validar_token_sessao_expirado():
  try:
    token = auth_service.gerarTokenSessao({"dados": "teste"}, auth_service.TEMPO_EXPIRACAO_TOKEN['MINIMO'])
    time.sleep(2)
    dadosToken = auth_service.decodificarToken(token)
    assert False

  except Exception as e:
    print(e.message)
    assert True


def test_criptografar_descriptografar_senha():
  senha = 'T3st3'
  senhaCriptografada = auth_service.criptografarSenha(senha)
  assert auth_service.compararSenha(senha, senhaCriptografada)


def test_senha_invalida():
  senha = 'T3st3'
  senhaCriptografada = auth_service.criptografarSenha(senha)
  assert not auth_service.compararSenha('senha errada', senhaCriptografada)


def test_identificador_unico_valido():
  idValido = auth_service.gerarIdentificadorUniversal()
  assert auth_service.validarIdentificadorUniversal(idValido)


def test_identificador_unico_invalido():
  idValido = auth_service.gerarIdentificadorUniversal() + '-invalido'
  assert not auth_service.validarIdentificadorUniversal(idValido)

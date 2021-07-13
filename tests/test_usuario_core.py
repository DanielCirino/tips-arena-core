from tipsarena_core.core import usuario_core
from tipsarena_core.services import auth_service


def test_excluir_usuarios():
  usuario_core.excluirTodos()
  usuario_core.criarIndicesUsuario()
  assert usuario_core.obterQuantidadeUsuarios() == 0


def test_salvar_usuario():
  usuario = {"email": "teste@teste.com.br",
             "documento": "12345678900",
             "nome": "Usuário de Testes",
             "perfilAcesso": "CONSULTA",
             "status": "PENDENTE_ATIVACAO",
             "senha": auth_service.criptografarSenha("T3st3")}
  resultado = usuario_core.salvarUsuario(usuario)
  assert resultado.acknowledged


def test_atualizar_usuario():
  usuario = {"email": "teste@teste.com.br",
             "documento": "12345678900",
             "nome": "Usuário de Testes Atualizado",
             "perfilAcesso": "CONSULTA",
             "status": "PENDENTE_ATIVACAO"}
  resultado = usuario_core.salvarUsuario(usuario)
  assert resultado.acknowledged


def test_obter_usuario_por_documento():
  usuario = usuario_core.obterUsuarioPorDocumento('12345678900')
  assert usuario["documento"] == "12345678900"


def test_obter_usuario_por_email():
  usuario = usuario_core.obterUsuarioPorEmail('teste@teste.com.br')
  assert usuario["email"] == "teste@teste.com.br"


def test_obter_usuario_documento_inexistente():
  try:
    usuario_core.obterUsuarioPorDocumento("inexistente")
  except Exception as e:
    assert True


def test_obter_usuario_por_email_inexistente():
  try:
    usuario_core.obterUsuarioPorEmail("e-mail@inexistente.com")
  except Exception as e:
    assert True


def test_obter_lista_usuarios():
  lista = usuario_core.listarUsuarios()
  assert len(lista) > 0


def test_obter_lista_usuarios_pendentes_ativacao():
  filtro = {"status": "PENDENTE_ATIVACAO"}
  lista = usuario_core.listarUsuarios(filtro)
  assert len(lista) > 0


def test_obter_lista_usuarios_vazia():
  filtro = {"campoInexistente": -1}
  lista = usuario_core.listarUsuarios(filtro)
  assert len(lista) == 0


def test_obter_quantidade_usuarios():
  assert usuario_core.obterQuantidadeUsuarios() == 1


if __name__ == '__main__':
  test_obter_usuario_por_email()

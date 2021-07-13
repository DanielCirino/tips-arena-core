from tipsarena_core.core import aposta_core
from tipsarena_core.core import partida_core
from tipsarena_core.extratores.flash_score import extrator_partida
from tipsarena_core.models.Aposta import Aposta
from tipsarena_core.models.Partida import Partida

partida: Partida = partida_core.obterPartidaPorId(
  "c1afc46e2f07ad08bbcb68fb")


def test_inclusao_aposta_vitoria_mandante():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.RESULT.name
  aposta.opcaoMercado = "VITORIA_MANDANTE"
  aposta.valorOdd = partida.odds["resultado"]["mandante"]
  aposta.valor = 75.00
  aposta.descricao = "Teste de aposta resultado"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_vitoria_visitante():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.RESULT.name
  aposta.opcaoMercado = "VITORIA_VISITANTE"
  aposta.valorOdd = partida.odds["resultado"]["visitante"]
  aposta.valor = 90.00
  aposta.descricao = "Teste de aposta resultado"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_empate():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.RESULT.name
  aposta.opcaoMercado = "EMPATE"
  aposta.valorOdd = partida.odds["resultado"]["empate"]
  aposta.valor = 100.00
  aposta.descricao = "Teste de aposta resultado"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_contra_visitante():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.DOUBLE_CHANCE.name
  aposta.opcaoMercado = "CONTRA_VISITANTE"
  aposta.valorOdd = partida.odds["duplaChance"]["contraVisitante"]
  aposta.valor = 125.00
  aposta.descricao = "Teste de aposta resultado"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_contra_mandante():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.DOUBLE_CHANCE.name
  aposta.opcaoMercado = "CONTRA_MANDANTE"
  aposta.valorOdd = partida.odds["duplaChance"]["contraMandante"]
  aposta.valor = 205.00
  aposta.descricao = "Teste de aposta resultado"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_contra_empate():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.DOUBLE_CHANCE.name
  aposta.opcaoMercado = "CONTRA_EMPATE"
  aposta.valorOdd = partida.odds["duplaChance"]["contraEmpate"]
  aposta.valor = 120.00
  aposta.descricao = "Teste de aposta resultado"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_dnb_mandante():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.DNB.name
  aposta.opcaoMercado = "DNB_MANDANTE"
  aposta.valorOdd = partida.odds["drawNoBet"]["mandante"]
  aposta.valor = 120.00
  aposta.descricao = "Teste de aposta DNB_MANDANTE"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_dnb_visitante():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.DNB.name
  aposta.opcaoMercado = "DNB_VISITANTE"
  aposta.valorOdd = partida.odds["drawNoBet"]["visitante"]
  aposta.valor = 120.00
  aposta.descricao = "Teste de aposta DNB VISITANTE"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_odd():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.ODD_EVEN.name
  aposta.opcaoMercado = "ODD"
  aposta.valorOdd = partida.odds["oddEven"]["odd"]
  aposta.valor = 80.00
  aposta.descricao = "Teste de aposta resultado PAR"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_even():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.ODD_EVEN.name
  aposta.opcaoMercado = "EVEN"
  aposta.valorOdd = partida.odds["oddEven"]["even"]
  aposta.valor = 45.00
  aposta.descricao = "Teste de aposta resultado IMPAR"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_btts_no():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.BTTS.name
  aposta.opcaoMercado = "BTTS_NO"
  aposta.valorOdd = partida.odds["btts"]["no"]
  aposta.valor = 87.00
  aposta.descricao = "Teste de aposta BTTS_NO"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_btts_yes():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.BTTS.name
  aposta.opcaoMercado = "BTTS_YES"
  aposta.valorOdd = partida.odds["btts"]["yes"]
  aposta.valor = 55.00
  aposta.descricao = "Teste de aposta BTTS_YES"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_under_0_5():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.UNDER_OVER.name
  aposta.opcaoMercado = "UNDER_0_5"
  aposta.valorOdd = partida.odds["underOver"][0]["under"]
  aposta.valor = 187.00
  aposta.descricao = "Teste de aposta UNDER"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_over_0_5():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.UNDER_OVER.name
  aposta.opcaoMercado = "OVER_0_5"
  aposta.valorOdd = partida.odds["underOver"][0]["over"]
  aposta.valor = 93.00
  aposta.descricao = "Teste de aposta OVER"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_placar_1_0():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.CORRECT_SCORE.name
  aposta.opcaoMercado = "PLACAR_1_0"
  aposta.valorOdd = partida.odds["placarExato"][0]["valor"]
  aposta.valor = 115.00
  aposta.descricao = "Teste de aposta PLACAR"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def test_inclusao_aposta_placar_2_0():
  aposta = Aposta()
  aposta.idUsuario = "5c81259b6fa2c7107b7644f7"
  aposta.idPartida = partida._id
  aposta.mercado = Aposta.Mercados.CORRECT_SCORE.name
  aposta.opcaoMercado = "PLACAR_2_0"
  aposta.valorOdd = partida.odds["placarExato"][1]["valor"]
  aposta.valor = 15.00
  aposta.descricao = "Teste de aposta PLACAR"
  aposta.status = Aposta.Status.PENDENTE.name
  aposta.resultado = Aposta.Resultado.PENDENTE.name

  resultado = aposta_core.salvarAposta(aposta)
  assert resultado.inserted_id != ""


def teste_finalizar_apostas_partida(self):
  extrator = extrator_partida()
  partida = partida_core.obterPartidaPorId("c1afc46e2f07ad08bbcb68fb")
  dadosPartida = extrator.obterDadosPartida(partida.url)

  extrator.finalizarNavegadorWeb()

  dadosPartida["_id"] = partida._id
  dadosPartida["idCompeticao"] = partida.idCompeticao
  dadosPartida["dataCadastro"] = partida.dataCadastro
  partidaAtualizada = Partida(dadosPartida)

  resultado = partida_core.salvarPartida(partidaAtualizada)

  if resultado:
    analiseAlteracoes = partida_core.analisarAlteracoesPartida(
      partida, partidaAtualizada)

    partida_core.processarAlteracoesPartida(partidaAtualizada, analiseAlteracoes)

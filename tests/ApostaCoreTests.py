import unittest

from core.ApostaCore import ApostaCore
from core.PartidaCore import PartidaCore
from models.Aposta import Aposta
from models.Partida import Partida
from webscraping.ScraperPartida import ScraperPartida


class ApostaCoreTests(unittest.TestCase):
    def testeInclusaoApostas(self):
        apostaCore = ApostaCore()
        partidaCore = PartidaCore()

        partida: Partida = partidaCore.getPartidaPorId(
            "49f9e33ff140ada0b276f853")


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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

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

        resultado = apostaCore.salvarAposta(aposta)
        self.assertTrue(resultado.inserted_id != "")

    def testeFinalizarApostasPartida(self):
        partidaCore = PartidaCore()
        extrator = ScraperPartida()
        partida = partidaCore.getPartidaPorId("49f9e33ff140ada0b276f853")
        dadosPartida = extrator.getDadosPartida(partida.url)

        extrator.finalizarWebDriver()

        dadosPartida["_id"] = partida._id
        dadosPartida["idCompeticao"] = partida.idCompeticao
        dadosPartida["dataCadastro"] = partida.dataCadastro
        partidaAtualizada = Partida(dadosPartida)

        resultado = partidaCore.salvarPartida(partidaAtualizada)

        if resultado:
            analiseAlteracoes = partidaCore.analisarAlteracoesPartida(
                partida, partidaAtualizada)

            partidaCore.processarAlteracoesPartida(partidaAtualizada, analiseAlteracoes)


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
            "128d1b6e02d36f8a7eb39c2d")


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

    def testeFinalizarApostasPartida(self):
        partidaCore = PartidaCore()
        extrator = ScraperPartida()
        partida = partidaCore.getPartidaPorId("128d1b6e02d36f8a7eb39c2d")
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


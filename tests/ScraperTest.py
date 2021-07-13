
# -*- coding: utf-8 -*-

import time
import unittest
from datetime import datetime

from extratores.MotorExtracao import MotorExtracao
from extratores.MotorFactory import MotorFactory
from repository.Collection import Collection
from tipsarena_core.core import partida_core, item_extracao_core
from tipsarena_core.extratores import extrator_edicao_competicao
from tipsarena_core.extratores import extrator_competicao
from tipsarena_core.extratores import extrator_equipe
from tipsarena_core.extratores import extrator_pais
from tipsarena_core.extratores import extrator_partida
from tipsarena_core.models.Partida import Partida
from tipsarena_core.models.ItemExtracao import ItemExtracao
from utils.DateTimeHandler import DateTimeHandler
from utils.HashString import HashString


class ScraperTest(unittest.TestCase):



    def teste_extrair_dados_partida(self):
        scraper = extrator_partida()
        partida = scraper.obterDadosPartida(
            "/match/UZGaKnC4/")  # 0QqMMPUm ou jNK3xpne
        print(partida)
        scraper.finalizarNavegadorWeb()
        self.assertTrue(partida != None)

    def teste_extrair_lista_partidas_edicao_competicao(self):
        scraper = extrator_partida()
        lista = scraper.obterListaPartidasEdicaoCompeticao(
            "/futebol/africa-do-sul/primeira-liga/")
        print(lista)
        scraper.finalizarNavegadorWeb()
        self.assertTrue(len(lista) > 0)

    def teste_extrair_lista_partidas_dia(self):
        scraper = extrator_partida()
        lista = scraper.obterListaPartidasDia()

        self.assertTrue(len(lista) > 0)

    def teste_extrator_lista_paises(self):
        motor = MotorExtracao(MotorExtracao.Acao.SCRAPING_PAISES, 0, 1, [])
        resultado = motor.scrapListaPaises()
        print(resultado)

    def teste_extrator_lista_competicoes_pais(self):
        objectId = HashString().encode("/futebol/brasil/")
        doc = Collection("scrap_work").obterDocumentoPorId(objectId)
        motor = MotorExtracao(
            MotorExtracao.Acao.SCRAPING_COMPETICOES, 0, 1, [])
        scrapPais = ItemExtracao(doc)
        resultado = motor.scrapListaCompeticoesPais(scrapPais)
        print(resultado)

    def teste_extrator_lista_edicoes_competicoes(self):
        objectId = HashString().encode("/futebol/brasil/campeonato-paulista/")
        doc = Collection("scrap_work").obterDocumentoPorId(objectId)
        motor = MotorExtracao(
            MotorExtracao.Acao.SCRAPING_EDICOES_COMPETICAO, 0, 1, [])
        scrapCompeticao = ItemExtracao(doc)
        resultado = motor.scrapListaEdicoesCompeticoes(scrapCompeticao)
        print(resultado)

    def teste_extrator_edicao_mais_recente_competicao(self):
        extrator = extrator_edicao_competicao()
        edicao = extrator.obterEdicaoMaisRecenteCompeticao(
            "/futebol/brasil/campeonato-paulista/")
        print(edicao)

    def teste_extrator_lista_equipes_edicao_competicao(self):
        objectId = HashString().encode("/futebol/brasil/campeonato-paulista/")
        doc = Collection("scrap_work").obterDocumentoPorId(objectId)
        motor = MotorExtracao(MotorExtracao.Acao.SCRAPING_EQUIPES, 0, 1, [])
        scrapEdicao = ItemExtracao(doc)
        resultado = motor.scrapListaEquipesEdicaoCompeticao(scrapEdicao)
        print(resultado)

    def teste_extrator_lista_partidas_edicao_competicao(self):
        objectId = HashString().encode("/futebol/brasil/campeonato-paulista/")
        doc = Collection("scrap_work").obterDocumentoPorId(objectId)
        motor = MotorExtracao(MotorExtracao.Acao.SCRAPING_PARTIDAS, 0, 1, [])
        scrapEdicao = ItemExtracao(doc)
        resultado = motor.scrapListaPartidasEdicaoCompeticao(scrapEdicao)
        print(resultado)

    def teste_motor_salvar_competicao(self):
        objectId = HashString().encode("/futebol/brasil/serie-a/")
        scrap = item_extracao_core().obterItemExtracaoPorId(objectId)

        motor = MotorExtracao(MotorExtracao.Acao.SALVAR_COMPETICOES, 0, 1, [])

        ret = motor.salvarCompeticao(scrap)

        self.assertTrue(ret)

    def teste_motor_salvar_edicao_competicao(self):
        objectId = HashString().encode("/futebol/africa-do-sul/copa-sul-africana-2016-2017/")
        scrap = item_extracao_core().obterItemExtracaoPorId(objectId)

        motor = MotorExtracao(
            MotorExtracao.Acao.SALVAR_EDICAO_COMPETICAO, 0, 1, [])

        ret = motor.salvarEdicaoCompeticao(scrap)

        self.assertTrue(ret)

    def teste_motor_salvar_equipe(self):
        objectId = HashString().encode("/equipe/botafogo-sp/2yRUzy5N/")
        scrap = item_extracao_core().obterItemExtracaoPorId(objectId)

        motor = MotorExtracao(MotorExtracao.Acao.SALVAR_EQUIPE, 0, 1, [])

        ret = motor.salvarEquipe(scrap)

        self.assertTrue(ret)

    def teste_motor_salvar_partida(self):
        objectId = HashString().encode("/match/UZGaKnC4/")
        scrap = item_extracao_core().obterItemExtracaoPorId(objectId)

        motor = MotorExtracao(MotorExtracao.Acao.SALVAR_EQUIPE, 0, 1, [])

        ret = motor.salvarPartida(scrap)

        self.assertTrue(ret)


    def teste_motor_extracao_factory(self):
        factory = MotorFactory(1, 1, 1)
        factory.getItensProcessamentoMotorExtracao()

        lista = factory.itensProcessamento
        print(len(lista))

        self.assertTrue(lista is not None)

    def teste_conversao_data(self):
        date = datetime.strptime("2019-02-02 12:15", "%Y-%m-%d %H:%M")
        timezone_off_set = DateTimeHandler().calcularTimezoneOffSet(
            time.mktime(date.timetuple()))
        self.assertTrue(timezone_off_set == -3)

    def teste_get_partidas_dia(self):

        data_inicio = datetime.strftime(
            datetime.today(), "%Y-%m-%d") + " 00:00:00"
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d %H:%M:%S")
        data_fim = datetime.now()

        filtrosPartida = partida_core.getOpcoesFiltro()

        filtrosPartida["dataHoraInicio"] = data_inicio
        filtrosPartida["dataHoraFim"] = data_fim
        filtrosPartida["status"].append(Partida.Status.AGENDADO.name)
        filtrosPartida["status"].append(
            Partida.Status.RESULTADO_NAO_DISPONIVEL.name)
        filtrosPartida["status"].append(Partida.Status.EM_ANDAMENTO.name)
        filtrosPartida["status"].append(Partida.Status.PRIMEIRO_TEMPO.name)
        filtrosPartida["status"].append(Partida.Status.INTERVALO.name)
        filtrosPartida["status"].append(Partida.Status.SEGUNDO_TEMPO.name)

        lista = partida_core.listPartidas(filtrosPartida)

        self.assertTrue(lista != None)

    def teste_get_head_to_head(self):
        headToHead = extrator_partida().obterUltimasPartidasEquipes()
        print(headToHead)
        self.assertTrue(headToHead!={})

    def teste_alteracao_id_partidas(self):

        collectionPartidas = Collection("partidas").collection
        collectionApostas = Collection("apostas").collection

        partidas =  Collection("partidas").listarDocumentos(sort=[("dataHora", -1)])
        for partida in partidas:
            try:
                idExterno = partida["url"].split("/")[2]
                novoId = HashString().encode(idExterno)
                idAntigo = partida["_id"]
                partida["_id"] = novoId

                idComparacao=HashString().encode(partida["url"])
                if partida["_id"] == idComparacao:

                    result = collectionPartidas.insert_one(partida)
                    print(result.inserted_id)

                    if result.acknowledged:
                        query_update = {"_id": idAntigo}
                        partidaExcluida = collectionPartidas.delete_one(query_update)
                        print(partidaExcluida.acknowledged)
                        apostasAtualizadas = collectionApostas.update_many({"idPartida":idAntigo},{"$set":{"idPartida":novoId}})
                        print(apostasAtualizadas.raw_result)
                        print("___________________________________________")
            except Exception as e:
                print(e.args[0])

        self.teste_deletar_partidas_duplicadas()
        self.assertTrue(partidas)

    def teste_deletar_partidas_duplicadas(self):

        collectionPartidas = Collection("partidas").collection

        partidas =  Collection("partidas").listarDocumentos(sort=[("dataHora", -1)])
        for partida in partidas:
            try:
                idComparacao = HashString().encode(partida["url"])
                if partida["_id"] == idComparacao:
                    partidaExcluida =  collectionPartidas.delete_one({"_id":idComparacao})
                    print(partidaExcluida.acknowledged)
                    print("___________________________________________")
            except Exception as e:
                print(e.args[0])

        self.assertTrue(partidas)


if __name__ == '__main__':
    unittest.main()

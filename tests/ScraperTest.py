
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
import time
from core.PartidaCore import PartidaCore
from core.ScrapWorkCore import ScrapWorkCore
from extratores.MotorExtracao import MotorExtracao
from extratores.MotorFactory import MotorFactory
from models.Partida import Partida
from models.ScrapWork import ScrapWork
from repository.Collection import Collection
from utils.DateTimeHandler import DateTimeHandler
from utils.HashString import HashString
from webscraping.ScraperCompeticao import ScraperCompeticao
from webscraping.ScraperEdicaoCompeticao import ScraperEdicaoCompeticao
from webscraping.ScraperEquipe import ScraperEquipe
from webscraping.ScraperPais import ScraperPais
from webscraping.ScraperPartida import ScraperPartida


class ScraperTest(unittest.TestCase):

    def teste_hash_string(self):
        h1 = (HashString().encode("/futebol/africa-do-sul/"))
        h1_teste = (HashString().encode("/futebol/africa-do-sul/"))

        self.assertTrue(h1 == h1_teste)

        h3 = (HashString().encode("/futebol/africa-do-sul/primeira-liga/"))
        h3_teste = (HashString().encode(
            "/futebol/africa-do-sul/primeira-liga"))

        self.assertTrue(h3 != h3_teste)

        h2 = (HashString().encode("/futebol/africa-do-sul/primeira-liga/"))
        h2_teste = (HashString().encode(
            "/futebol/africa-do-sul/primeira-liga/"))

        self.assertTrue(h2 == h2_teste)

    def teste_extrair_lista_paises(self):
        scraper = ScraperPais()
        lista = scraper.getListaPaises()
        print(lista)
        self.assertTrue(len(lista) > 0)

    def teste_extrair_lista_competicoes_pais(self):
        scraper = ScraperCompeticao()
        lista = scraper.getListaCompeicoesPais("/futebol/africa-do-sul/")
        print(lista)
        self.assertTrue(len(lista) > 0)

    def teste_extrair_dados_competicao(self):
        scraper = ScraperCompeticao()
        compet = scraper.getDadosCompeticao(
            "/futebol/africa-do-sul/primeira-liga/")
        print(compet)
        self.assertTrue(compet != None)

    def teste_extrair_lista_edicoes_competicao(self):
        scraper = ScraperEdicaoCompeticao()
        lista = scraper.getListaEdicoesCompeticao(
            "/futebol/africa-do-sul/primeira-liga/")
        print(lista)
        self.assertTrue(len(lista) > 0)

    def teste_extrair_dados_edicao_competicao(self):
        scraper = ScraperEdicaoCompeticao()
        edicao = scraper.getDadosEdicaoCompeticao(
            "/futebol/africa-do-sul/primeira-liga-2012-2013/")
        print(edicao)
        self.assertTrue(edicao != None)

    def teste_extrair_lista_equipes_edicao_competicao(self):
        scraper = ScraperEquipe()
        lista = scraper.getListaEquipesEdicaoCompeticao(
            "/futebol/africa-do-sul/primeira-liga/")
        print(lista)
        self.assertTrue(len(lista) > 0)

    def teste_extrair_dados_equipe(self):
        scraper = ScraperEquipe()
        equipe = scraper.getDadosEquipe("/equipe/kaizer/fFZ2CGx0/")
        print(equipe)
        self.assertTrue(equipe != None)

    def teste_extrair_dados_partida(self):
        scraper = ScraperPartida()
        partida = scraper.getDadosPartida(
            "/match/IPMRioQR/")  # 0QqMMPUm ou jNK3xpne
        print(partida)
        scraper.finalizarWebDriver()
        self.assertTrue(partida != None)

    def teste_extrair_lista_partidas_edicao_competicao(self):
        scraper = ScraperPartida()
        lista = scraper.getListaPartidasEdicaoCompeticao(
            "/futebol/africa-do-sul/primeira-liga/")
        print(lista)
        scraper.finalizarWebDriver()
        self.assertTrue(len(lista) > 0)

    def teste_extrair_lista_partidas_dia(self):
        scraper = ScraperPartida()
        lista = scraper.getListaPartidasDia()

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
        scrapPais = ScrapWork(doc)
        resultado = motor.scrapListaCompeticoesPais(scrapPais)
        print(resultado)

    def teste_extrator_lista_edicoes_competicoes(self):
        objectId = HashString().encode("/futebol/brasil/campeonato-paulista/")
        doc = Collection("scrap_work").obterDocumentoPorId(objectId)
        motor = MotorExtracao(
            MotorExtracao.Acao.SCRAPING_EDICOES_COMPETICAO, 0, 1, [])
        scrapCompeticao = ScrapWork(doc)
        resultado = motor.scrapListaEdicoesCompeticoes(scrapCompeticao)
        print(resultado)

    def teste_extrator_edicao_mais_recente_competicao(self):
        extrator = ScraperEdicaoCompeticao()
        edicao = extrator.getEdicaoMaisRecenteCompeticao(
            "/futebol/brasil/campeonato-paulista/")
        print(edicao)

    def teste_extrator_lista_equipes_edicao_competicao(self):
        objectId = HashString().encode("/futebol/brasil/campeonato-paulista/")
        doc = Collection("scrap_work").obterDocumentoPorId(objectId)
        motor = MotorExtracao(MotorExtracao.Acao.SCRAPING_EQUIPES, 0, 1, [])
        scrapEdicao = ScrapWork(doc)
        resultado = motor.scrapListaEquipesEdicaoCompeticao(scrapEdicao)
        print(resultado)

    def teste_extrator_lista_partidas_edicao_competicao(self):
        objectId = HashString().encode("/futebol/brasil/campeonato-paulista/")
        doc = Collection("scrap_work").obterDocumentoPorId(objectId)
        motor = MotorExtracao(MotorExtracao.Acao.SCRAPING_PARTIDAS, 0, 1, [])
        scrapEdicao = ScrapWork(doc)
        resultado = motor.scrapListaPartidasEdicaoCompeticao(scrapEdicao)
        print(resultado)

    def teste_motor_salvar_competicao(self):
        objectId = HashString().encode("/futebol/brasil/serie-a/")
        scrap = ScrapWorkCore().getScrapWorkById(objectId)

        motor = MotorExtracao(MotorExtracao.Acao.SALVAR_COMPETICOES, 0, 1, [])

        ret = motor.salvarCompeticao(scrap)

        self.assertTrue(ret)

    def teste_motor_salvar_edicao_competicao(self):
        objectId = HashString().encode("/futebol/africa-do-sul/copa-sul-africana-2016-2017/")
        scrap = ScrapWorkCore().getScrapWorkById(objectId)

        motor = MotorExtracao(
            MotorExtracao.Acao.SALVAR_EDICAO_COMPETICAO, 0, 1, [])

        ret = motor.salvarEdicaoCompeticao(scrap)

        self.assertTrue(ret)

    def teste_motor_salvar_equipe(self):
        objectId = HashString().encode("/equipe/botafogo-sp/2yRUzy5N/")
        scrap = ScrapWorkCore().getScrapWorkById(objectId)

        motor = MotorExtracao(MotorExtracao.Acao.SALVAR_EQUIPE, 0, 1, [])

        ret = motor.salvarEquipe(scrap)

        self.assertTrue(ret)

    def teste_motor_salvar_partida(self):
        objectId = HashString().encode("/jogo/v5hgQNv3/")
        scrap = ScrapWorkCore().getScrapWorkById(objectId)

        motor = MotorExtracao(MotorExtracao.Acao.SALVAR_EQUIPE, 0, 1, [])

        ret = motor.salvarPartida(scrap)

        self.assertTrue(ret)

    def teste_motor_extracao_factory(self):
        factory = MotorFactory(2, 1, 1)
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
        partidaCore = PartidaCore()
        data_inicio = datetime.strftime(
            datetime.today(), "%Y-%m-%d") + " 00:00:00"
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d %H:%M:%S")
        data_fim = datetime.now()

        filtrosPartida = partidaCore.getOpcoesFiltro()

        filtrosPartida["dataHoraInicio"] = data_inicio
        filtrosPartida["dataHoraFim"] = data_fim
        filtrosPartida["status"].append(Partida.Status.AGENDADO.name)
        filtrosPartida["status"].append(
            Partida.Status.RESULTADO_NAO_DISPONIVEL.name)
        filtrosPartida["status"].append(Partida.Status.EM_ANDAMENTO.name)
        filtrosPartida["status"].append(Partida.Status.PRIMEIRO_TEMPO.name)
        filtrosPartida["status"].append(Partida.Status.INTERVALO.name)
        filtrosPartida["status"].append(Partida.Status.SEGUNDO_TEMPO.name)

        lista = partidaCore.listPartidas(filtrosPartida)

        self.assertTrue(lista != None)

    def teste_get_head_to_head(self):
        headToHead = ScraperPartida().obterUltimasPartidasEquipes()
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

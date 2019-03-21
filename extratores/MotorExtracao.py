
# -*- coding: utf-8 -*-

import threading
from enum import Enum
import time
from datetime import datetime, timedelta

from utils.HashString import HashString

from webscraping.ScraperPais import ScraperPais
from webscraping.ScraperCompeticao import ScraperCompeticao
from webscraping.ScraperEdicaoCompeticao import ScraperEdicaoCompeticao
from webscraping.ScraperEquipe import ScraperEquipe
from webscraping.ScraperPartida import ScraperPartida

from models.ScrapWork import ScrapWork
from models.Competicao import Competicao
from models.EdicaoCompeticao import EdicaoCompeticao
from models.Equipe import Equipe
from models.Partida import Partida

from core.ScrapWorkCore import ScrapWorkCore
from core.CompeticaoCore import CompeticaoCore

from core.EquipeCore import EquipeCore
from core.PartidaCore import PartidaCore


class MotorExtracao(threading.Thread):
    def __init__(self, acao=-1, id_thread=-1, total_threads=-1, lista_processamento=[]):

        self.acao = acao
        self.id_thread = id_thread
        self.total_threads = total_threads

        self.lista_processamento = lista_processamento
        self.total_registros = len(lista_processamento)

        self.range_inicio = id_thread * \
            round(len(self.lista_processamento) / self.total_threads)
        self.range_fim = (
            (id_thread + 1) * round(len(self.lista_processamento) / self.total_threads)) - 1

        if self.range_fim + 1 > len(self.lista_processamento):
            self.range_fim = len(self.lista_processamento) - 1

        if id_thread + 1 == total_threads:
            if self.range_fim + 1 < len(self.lista_processamento):
                self.range_fim = len(self.lista_processamento) - 1

        # print("[{}a{}][{}]".format(self.range_inicio, self.range_fim, self.id_thread))

        self.total_processado = 0
        self.total_erros = 0
        self.hora_inicio = time.strftime("%Y-%m-%d %H:%M:%S")
        self.hora_fim = None
        self.processamento_finalizado = False

        self.extrator = None

        threading.Thread.__init__(self)

    def salvarScrap(self, url, prioridade: int, tipo: str, status: str, idPai=0):
        try:

            scrapWorkCore = ScrapWorkCore()
            objectId = HashString().encode(url)
            scrap = scrapWorkCore.getScrapWorkById(objectId)

            scrap.url = url
            scrap.tipo = tipo
            scrap.idPai = idPai
            scrap.status = status
            scrap.prioridadeExtracao = prioridade

            ret = scrapWorkCore.salvarScrapWork(scrap)
            if ret:
                return True
            else:
                return False
        except Exception as e:
            return False

    def salvarListaScraping(self, listaUrls, status, tipo, idPai):
        try:
            contadorSucesso = 0
            contadorErro = 0

            for item in listaUrls:
                ret = self.salvarScrap(
                    item["url"], item["seq"], tipo, status, idPai)
                if ret:
                    contadorSucesso += 1
                else:
                    contadorErro += 1
            return {"totalSucesso": contadorSucesso, "totalErro": contadorErro}

        except Exception as e:
            print(e.args)
            return None

    def scrapListaPaises(self):
        try:
            horaInicio = datetime.now()
            paises = ScraperPais().getListaPaises()

            ret = self.salvarListaScraping(paises,
                                           ScrapWork.Status.SCRAPING_COMPETICOES.name,
                                           ScrapWork.Tipo.PAIS.name, "")

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acao,
                "totalItens": len(paises),
                "resultado": ret,
                "idThread": self.id_thread,
                "totalThread": self.total_threads
            }
        except Exception as e:
            print(e.args)
            return None

    def scrapListaCompeticoesPais(self, scrapPais: ScrapWork):
        scrapWorkCore = ScrapWorkCore()
        try:

            horaInicio = datetime.now()
            competicoes = ScraperCompeticao().getListaCompeicoesPais(scrapPais.url)

            scrapPais.target = len(competicoes)
            scrapPais.status = ScrapWork.Status.PROCESSANDO.name
            scrapWorkCore.salvarScrapWork(scrapPais)

            ret = self.salvarListaScraping(competicoes,
                                           ScrapWork.Status.SCRAPING_EDICOES_COMPETICAO.name,
                                           ScrapWork.Tipo.COMPETICAO.name, scrapPais._id)

            scrapPais.status = ScrapWork.Status.OK.name
            scrapWorkCore.salvarScrapWork(scrapPais)

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acao,
                "totalItens": len(competicoes),
                "resultado": ret,
                "idThread": self.id_thread,
                "totalThread": self.total_threads
            }

        except Exception as e:
            print(e.args)
            scrapPais.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapPais)

            return None

    def scrapListaEdicoesCompeticoes(self, scrapCompeticao: ScrapWork):
        scrapWorkCore = ScrapWorkCore()
        try:

            horaInicio = datetime.now()
            edicoes = ScraperEdicaoCompeticao().getListaEdicoesCompeticao(scrapCompeticao.url)

            scrapCompeticao.target = len(edicoes)
            scrapCompeticao.status = ScrapWork.Status.PROCESSANDO.name
            scrapWorkCore.salvarScrapWork(scrapCompeticao)

            ret = self.salvarListaScraping(edicoes,
                                           ScrapWork.Status.SCRAPING_EQUIPES.name,
                                           ScrapWork.Tipo.EDICAO_COMPETICAO.name, scrapCompeticao._id)

            scrapCompeticao.status = ScrapWork.Status.AGUARDANDO_SCRAPING.name
            scrapWorkCore.salvarScrapWork(scrapCompeticao)

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acao,
                "totalItens": len(edicoes),
                "resultado": ret,
                "idThread": self.id_thread,
                "totalThread": self.total_threads
            }

        except Exception as e:
            print(e.args)
            scrapCompeticao.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapCompeticao)

            return None

    def scrapListaEquipesEdicaoCompeticao(self, scrapEdicao: ScrapWork):
        scrapWorkCore = ScrapWorkCore()
        try:

            horaInicio = datetime.now()
            equipes = ScraperEquipe().getListaEquipesEdicaoCompeticao(scrapEdicao.url)

            scrapEdicao.target = len(equipes)
            scrapEdicao.status = ScrapWork.Status.PROCESSANDO.name
            scrapWorkCore.salvarScrapWork(scrapEdicao)

            ret = self.salvarListaScraping(equipes,
                                           ScrapWork.Status.AGUARDANDO_SCRAPING.name,
                                           ScrapWork.Tipo.EQUIPE.name, scrapEdicao._id)

            scrapEdicao.status = ScrapWork.Status.SCRAPING_PARTIDAS.name
            scrapWorkCore.salvarScrapWork(scrapEdicao)

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acao,
                "totalItens": len(equipes),
                "resultado": ret,
                "idThread": self.id_thread,
                "totalThread": self.total_threads
            }

        except Exception as e:
            print(e.args)
            scrapEdicao.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapEdicao)

            return None

    def scrapListaPartidasEdicaoCompeticao(self, scrapEdicao):
        scrapWorkCore = ScrapWorkCore()
        try:

            horaInicio = datetime.now()
            partidas = self.extrator.getListaPartidasEdicaoCompeticao(
                scrapEdicao.url)
            totalPartidas = len(partidas["agendadas"]) + \
                len(partidas["finalizadas"])

            scrapEdicao.target = totalPartidas
            scrapEdicao.status = ScrapWork.Status.PROCESSANDO.name
            scrapWorkCore.salvarScrapWork(scrapEdicao)

            ret = self.salvarListaScraping(partidas["agendadas"] + partidas["finalizadas"],
                                           ScrapWork.Status.AGUARDANDO_SCRAPING.name,
                                           ScrapWork.Tipo.PARTIDA.name, scrapEdicao._id)

            scrapEdicao.status = ScrapWork.Status.AGUARDANDO_SCRAPING.name
            scrapWorkCore.salvarScrapWork(scrapEdicao)

            horaFim = datetime.now()

            return {
                "horaInicio": horaInicio,
                "horaFim": horaFim,
                "acaoMotor": self.acao,
                "totalItens": totalPartidas,
                "resultado": ret,
                "idThread": self.id_thread,
                "totalThread": self.total_threads
            }

        except Exception as e:
            print(e.args)
            scrapEdicao.status = ScrapWork.Status.ERRO.name
            scrapWorkCore.salvarScrapWork(scrapEdicao)

            return None

    def salvarCompeticao(self, scrapCompeticao: ScrapWork):
        try:
            competicaoCore = CompeticaoCore()
            dadosCompeticao = ScraperCompeticao().getDadosCompeticao(scrapCompeticao.url)
            objectId = HashString().encode(scrapCompeticao.url)

            competicao = competicaoCore.getCompeticaoPorId(objectId)
            dadosCompeticao["_id"] = competicao._id
            dadosCompeticao["dataCadastro"] = competicao.dataCadastro

            competicao = Competicao(dadosCompeticao)

            ret = competicaoCore.salvarCompeticao(competicao)

            if ret:
                scrapCompeticao.status = ScrapWork.Status.OK.name
            else:
                scrapCompeticao.status = ScrapWork.Status.ERRO.name

            ScrapWorkCore().salvarScrapWork(scrapCompeticao)

            return ret
        except Exception as e:
            print(e.args)
            scrapCompeticao.status = ScrapWork.Status.ERRO.name
            ScrapWorkCore().salvarScrapWork(scrapCompeticao)
            return False

    def salvarEdicaoCompeticao(self, scrapEdicao: ScrapWork):
        try:
            edicaoCore = EdicaoCompeticaoCore()
            dadosEdicao = ScraperEdicaoCompeticao().getDadosEdicaoCompeticao(scrapEdicao.url)
            objectId = HashString().encode(scrapEdicao.url)

            edicao = edicaoCore.getEdicaoCompeticaoPorId(objectId)
            dadosEdicao["_id"] = edicao._id
            dadosEdicao["dataCadastro"] = edicao.dataCadastro

            edicao = EdicaoCompeticao(dadosEdicao)
            edicao.idCompeticao = scrapEdicao.idPai

            ret = edicaoCore.salvarEdicaoCompeticao(edicao)

            if ret:
                scrapEdicao.status = ScrapWork.Status.OK.name
            else:
                scrapEdicao.status = ScrapWork.Status.ERRO.name

            ScrapWorkCore().salvarScrapWork(scrapEdicao)

            return ret
        except Exception as e:
            print(e.args)
            scrapEdicao.status = ScrapWork.Status.ERRO.name
            ScrapWorkCore().salvarScrapWork(scrapEdicao)
            return False

    def salvarEquipe(self, scrapEquipe: ScrapWork):
        try:
            equipeCore = EquipeCore()
            dadosEquipe = ScraperEquipe().getDadosEquipe(scrapEquipe.url)
            objectId = HashString().encode(scrapEquipe.url)

            equipe = equipeCore.getEquipePorId(objectId)
            dadosEquipe["_id"] = equipe._id
            dadosEquipe["dataCadastro"] = equipe.dataCadastro

            equipe = Competicao(dadosEquipe)

            ret = equipeCore.salvarEquipe(equipe)

            if ret:
                scrapEquipe.status = ScrapWork.Status.OK.name
            else:
                scrapEquipe.status = ScrapWork.Status.ERRO.name

            ScrapWorkCore().salvarScrapWork(scrapEquipe)

            return ret
        except Exception as e:
            print(e.args)
            scrapEquipe.status = ScrapWork.Status.ERRO.name
            ScrapWorkCore().salvarScrapWork(scrapEquipe)
            return False

    def salvarPartida(self, scrapPartida: ScrapWork):
        try:

            partidaCore = PartidaCore()
            dadosPartida = self.extrator.getDadosPartida(scrapPartida.url)
            objectId = HashString().encode(scrapPartida.url)

            partida = partidaCore.getPartidaPorId(objectId)
            dadosPartida["_id"] = partida._id
            dadosPartida["edicaoCompeticao"]["url"] = scrapPartida.url

            dadosPartida["dataCadastro"] = partida.dataCadastro

            partida = Partida(dadosPartida)
            partida.idEdicaoCompeticao = scrapPartida.idPai

            ret = partidaCore.salvarPartida(partida)

            if ret:
                scrapPartida.status = ScrapWork.Status.OK.name
            else:
                scrapPartida.status = ScrapWork.Status.ERRO.name

            ScrapWorkCore().salvarScrapWork(scrapPartida)

            return ret
        except Exception as e:
            print(e.args)
            scrapPartida.status = ScrapWork.Status.ERRO.name
            ScrapWorkCore().salvarScrapWork(scrapPartida)
            return False

    def exibirAcoesMotor(self):
        for acao in self.Acao:
            print("{} ==> {}".format(acao.value, acao.name))

    def run(self):
        # obter lista paises do site
        # obter lista competicoes por pais
        # obter lista partidas por competicao
        # obter lista equipes por competicao

        # salvar competicoes por pais
        # salvar partidas da competicao
        # salvar equipes da competicao

        if self.acao == self.Acao.SCRAPING_PAISES:

            for i in range(self.range_inicio, self.range_fim + 1):
                url = self.lista_processamento[i]
                ret = self.salvarScrap(
                    url, ScrapWork.Tipo.PAIS.name, ScrapWork.Status.SCRAPING_COMPETICOES.name)

                if ret:
                    self.total_processado += 1
                else:
                    self.total_erros += 1

        elif self.acao == self.Acao.SCRAPING_COMPETICOES:
            for i in range(self.range_inicio, self.range_fim + 1):
                scrapPais = self.lista_processamento[i]
                ret = self.scrapListaCompeticoesPais(scrapPais)

                if ret is not None:
                    self.total_processado += ret["resultado"]["totalSucesso"]
                else:
                    self.total_erros += ret["resultado"]["totalErro"]

        elif self.acao == self.Acao.SCRAPING_EDICOES_COMPETICAO:
            for i in range(self.range_inicio, self.range_fim + 1):
                scrapCompeticao = self.lista_processamento[i]
                ret = self.scrapListaEdicoesCompeticoes(scrapCompeticao)

                if ret is not None:
                    self.total_processado += ret["resultado"]["totalSucesso"]
                else:
                    self.total_erros += ret["resultado"]["totalErro"]

        elif self.acao == self.Acao.SCRAPING_EQUIPES:
            for i in range(self.range_inicio, self.range_fim + 1):
                scrapEdicao = self.lista_processamento[i]
                ret = self.scrapListaEquipesEdicaoCompeticao(scrapEdicao)

                if ret is not None:
                    self.total_processado += ret["resultado"]["totalSucesso"]
                else:
                    self.total_erros += ret["resultado"]["totalErro"]

        elif self.acao == self.Acao.SCRAPING_PARTIDAS:
            self.extrator = ScraperPartida()

            for i in range(self.range_inicio, self.range_fim + 1):
                scrapEdicao = self.lista_processamento[i]
                ret = self.scrapListaPartidasEdicaoCompeticao(scrapEdicao)

                if ret is not None:
                    self.total_processado += ret["resultado"]["totalSucesso"]
                else:
                    self.total_erros += ret["resultado"]["totalErro"]

            self.extrator.finalizarWebDriver()

        elif self.acao == self.Acao.SALVAR_COMPETICOES:
            for i in range(self.range_inicio, self.range_fim + 1):
                scrapCompeticao = self.lista_processamento[i]
                ret = self.salvarCompeticao(scrapCompeticao)

                if ret:
                    self.total_processado += 1
                else:
                    self.total_erros += 1

        elif self.acao == self.Acao.SALVAR_EDICAO_COMPETICAO:
            for i in range(self.range_inicio, self.range_fim + 1):
                scrap_edicao = self.lista_processamento[i]
                self.salvar_edicao_competicao(scrap_edicao)

        elif self.acao == self.Acao.SALVAR_EQUIPE:
            for i in range(self.range_inicio, self.range_fim + 1):
                scrap_equipe = self.lista_processamento[i]
                self.salvar_equipe(scrap_equipe)

        elif self.acao == self.Acao.SALVAR_PARTIDAS:
            self.extrator = ScraperPartida()
            for i in range(self.range_inicio, self.range_fim + 1):
                scrap_partida = self.lista_processamento[i]
                self.salvarPartida(scrap_partida)

            self.extrator.finalizarWebDriver()

        else:
            print("ACAO INVALIDA")

        self.processamento_finalizado = True
        self.hora_fim = time.strftime("%Y-%m-%d %H:%M:%S")

    class Acao(Enum):
        SCRAPING_PAISES = 1
        SCRAPING_COMPETICOES = 2
        SCRAPING_EDICOES_COMPETICAO = 3
        SCRAPING_EQUIPES = 4
        SCRAPING_PARTIDAS = 5

        SALVAR_COMPETICOES = 6
        SALVAR_EDICAO_COMPETICAO = 7
        SALVAR_EQUIPE = 8
        SALVAR_PARTIDAS = 9


# -*- coding: utf-8 -*-

from datetime import datetime
from repository.Collection import Collection
from models.ScrapWork import ScrapWork
from utils.HashString import HashString


class ScrapWorkCore:
    def __init__(self):
        self.collection = Collection("scrap_work")

    def getOpcoesFiltro(self):
        return {
            "idPai": "",
            "url": "",
            "tipo": [],
            "status": []
        }

    def getOpcoesOrdenacao(self):
        return [{
            "prioridadeExtracao": 1,
        }]

    def getScrapWorkById(self, id):
        doc = self.collection.obterDocumentoPorId(id)

        if doc is not None:
            return ScrapWork(doc)
        else:
            return ScrapWork()

    def getScrapWorksPorTipo(self, tipo, status):
        filtros = self.getOpcoesFiltro()
        filtros["tipo"].append(tipo)
        filtros["status"].append(status)

        ordenacao = self.getOpcoesOrdenacao()

        return self.listScrapWorks(filtros, ordenacao)

    def listScrapWorks(self, filter={}, sort=[], limit=0, skip=0):
        listaScraps = []
        if filter != {}:
            if filter["idPai"] == "":
                del filter["idPai"]

            if filter["url"] == "":
                del filter["url"]

            if filter["tipo"] == "":
                del filter["tipo"]
            else:
                filter["tipo"] = {"$in": filter["tipo"]}

            if filter["status"] == "":
                del filter["status"]
            else:
                filter["status"] = {"$in": filter["status"]}

        docs = self.collection.listarDocumentos(
            filter, [("prioridadeExtracao", 1)], limit, skip)

        for doc in docs:
            listaScraps.append(ScrapWork(doc))

        return listaScraps

    def salvarScrapWork(self, scrapWork: ScrapWork):
        try:
            scrapWork.dataAtualizacao = datetime.utcnow()
            if scrapWork._id == "":
                scrapWork._id = HashString().encode(scrapWork.url)
                scrapWork.dataCadastro = datetime.utcnow()
                return self.collection.inserirDocumento(scrapWork)
            else:
                return self.collection.atualizarDocumento(scrapWork)
        except Exception as e:
            print(e.args)
            return False

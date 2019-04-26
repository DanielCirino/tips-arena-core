
# -*- coding: utf-8 -*-

from datetime import datetime
from repository.Collection import Collection
from models.ProcessamentoBatch import ProcessamentoBatch
from utils.DateTimeHandler import DateTimeHandler


class ProcessamentoBatchCore:
    def __init__(self):
        self.collection = Collection("processamento_batch")

    def getOpcoesFiltro(self):
        return {
            "dataInicio": "",
            "dataFim": "",
            "tipo": [],
            "status": []
        }

    def getOpcoesOrdenacao(self):
        return [{
            "dataInicio": -1,
        }]

    def getProcessamentoBatchById(self, id):
        doc = self.collection.obterDocumentoPorId(id)

        if doc is not None:
            return ProcessamentoBatch(doc)
        else:
            return ProcessamentoBatch()

    def getScrapWorksPorTipo(self, tipo, status):
        filtros = self.getOpcoesFiltro()
        filtros["tipo"].append(tipo)
        filtros["status"].append(status)

        ordenacao = self.getOpcoesOrdenacao()

        return self.listScrapWorks(filtros, ordenacao)

    # def listScrapWorks(self, filter={}, sort=[], limit=0, skip=0):
    #     listaScraps = []
    #     if filter != {}:
    #         if filter["idPai"] == "":
    #             del filter["idPai"]
    #
    #         if filter["url"] == "":
    #             del filter["url"]
    #
    #         if filter["tipo"] == "":
    #             del filter["tipo"]
    #         else:
    #             filter["tipo"] = {"$in": filter["tipo"]}
    #
    #         if filter["status"] == "":
    #             del filter["status"]
    #         else:
    #             filter["status"] = {"$in": filter["status"]}
    #
    #     docs = self.collection.listar_documentos(filter, [("prioridadeExtracao", 1)], limit, skip)
    #
    #     for doc in docs:
    #         listaScraps.append(ScrapWork(doc))
    #
    #     return listaScraps

    def salvarProcessamentoBatch(self, processamento: ProcessamentoBatch):
        try:
            processamento.dataAtualizacao = DateTimeHandler().converterHoraLocalToUtc(datetime.now())
            if processamento._id == "":
                delattr(processamento,"_id")
                return self.collection.inserirDocumento(processamento)
            else:
                return self.collection.atualizarDocumento(processamento)
        except Exception as e:
            print(e.args)
            return None


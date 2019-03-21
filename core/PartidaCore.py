
# -*- coding: utf-8 -*-

from datetime import datetime
from bson import json_util
from utils.HashString import HashString
from repository.Collection import Collection
from models.Partida import Partida
import json

class PartidaCore:
    def __init__(self):
        self.collection = Collection("partidas")

    def getOpcoesFiltro(self):
        return {
            "idEdicaoCompeticao": "",
            "status": [],
            "dataHora": [],
            "dataHoraInicio": "",
            "dataHoraFim": ""

        }

    def getOpcoesOrdenacao(self):
        return [{
            "dataCadastro": -1,
            "dataAtualizacao": -1
        }]

    def salvarPartida(self, partida: Partida):
        try:
            partida.dataAtualizacao = datetime.now()
            if partida._id == "":
                partida._id = HashString().encode(partida.url)
                partida.dataCadastro = datetime.now()
                return self.collection.inserir_documento(partida)
            else:
                return self.collection.atualizar_documento(partida)
        except Exception as e:
            print(e.args)
            return False

    def getPartidaPorId(self, id):
        doc = self.collection.get_documento_por_id(id)
        if doc is not None:
            return Partida(doc)
        else:
            return Partida()

    def listPartidas(self, filter={}, sort=[], limit=0, skip=0):
        try:
            listaPartidas = []
            filtroDataHora = {}

            if filter != {}:
                if filter["idEdicaoCompeticao"] == "":
                    del filter["idEdicaoCompeticao"]

                if filter["dataHoraInicio"] != "":
                    filtroDataHora["$gte"] = filter["dataHoraInicio"]

                del filter["dataHoraInicio"]

                if filter["dataHoraFim"] != "":
                    filtroDataHora["$lte"] = filter["dataHoraFim"]

                del filter["dataHoraFim"]

                if len(filter["status"]) == 0:
                    del filter["status"]
                else:
                    filter["status"] = {"$in": filter["status"]}

                filter["dataHora"] = filtroDataHora
            docs = self.collection.listar_documentos(filter, [("dataHora", -1)], limit, skip)



            for doc in docs:
                # print(json.dumps(doc, indent=2, default=json_util.default),",")
                listaPartidas.append(Partida(doc))

            return listaPartidas
        except Exception as e:
            print(e.args)
            return None

    def analisarAlteracoesPartida(self, partida: Partida, partidaAtualizada: Partida):
        try:
            listaAlteracoes = []
            partida = partida.__dict__
            partidaAtualizada = partidaAtualizada.__dict__

            for key in partida:
                if partida[key] != partidaAtualizada[key]:
                    listaAlteracoes.append(
                        {"campo": key,
                         "valorAnterior": partida[key],
                         "valorNovo": partidaAtualizada[key]})

            return listaAlteracoes
        except Exception as e:
            print(e.args)
            return None




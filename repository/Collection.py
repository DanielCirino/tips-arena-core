#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from repository.MongoClient import MongoClient
from utils.DateTimeHandler import DateTimeHandler


class Collection(object):
    def __init__(self, nome):
        self.client = MongoClient()
        self.collection = self.client.get_collection(nome)

    def inserir_documento(self, documento):
        try:
            doc = documento.__dict__
            doc["timezoneOffset"] = DateTimeHandler().local_time_offset()

            return self.collection.insert_one(doc)
        except Exception as e:
            return None
        finally:
            self.client.desconectar()

    def atualizar_documento(self, documento):
        try:
            doc = documento.__dict__
            query_update = {"_id": documento._id}

            return self.collection.update_one(query_update, {"$set": doc})

        except Exception as e:
            print(e.args)
            return None
        finally:
            self.client.desconectar()

    def deletar_documento(self, id):
        query_delete = {"_id": id}
        try:
            return self.collection.delete_one(query_delete)
        except Exception as e:
            return None
        finally:
            self.client.desconectar()

    def listar_documentos(self, query={}, sort=[], limit=0, skip=0):
        try:
            cursor = self.collection.find(query)

            if sort != []:
                cursor.sort(sort)

            if limit == 0:
                cursor.limit(limit)

            if skip > 0:
                cursor.skip(skip)

            return cursor
        except Exception as e:
            print(e.args)
            return []

        finally:
            self.client.desconectar()

    def get_documento_por_id(self, id):
        try:
            doc = self.collection.find_one({"_id": id})
            return doc
        except Exception as e:
            print(e.args)
            return None

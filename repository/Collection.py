
# -*- coding: utf-8 -*-

from repository.MongoClient import MongoClient
from utils.DateTimeHandler import DateTimeHandler


class Collection(object):
    def __init__(self, nome):
        self.client = MongoClient()
        self.collection = self.client.getCollection(nome)

    def inserirDocumento(self, documento):
        try:

            if(hasattr(documento,"__dict__")):
                doc = documento.__dict__
            else:
                doc = documento

            doc["timezoneOffset"] = DateTimeHandler().calcularTimezoneOffSet()

            return self.collection.insert_one(doc)
        except Exception as e:
            return None
        finally:
            self.client.disconnect()

    def atualizarDocumento(self, documento):
        try:
            if (hasattr(documento, "__dict__")):
                doc = documento.__dict__
            else:
                doc = documento

            query_update = {"_id": documento._id}

            return self.collection.update_one(query_update, {"$set": doc})

        except Exception as e:
            print(e.args)
            return None
        finally:
            self.client.disconnect()

    def deletarDocumento(self, id):
        query_delete = {"_id": id}
        try:
            return self.collection.delete_one(query_delete)
        except Exception as e:
            return None
        finally:
            self.client.disconnect()

    def listarDocumentos(self, query={}, sort=[], limit=0, skip=0):
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
            self.client.disconnect()

    def obterDocumentoPorId(self, id):
        try:
            doc = self.collection.find_one({"_id": id})
            return doc
        except Exception as e:
            print(e.args)
            return None

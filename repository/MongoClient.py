
# -*- coding: utf-8 -*-

import os
import pymongo


class MongoClient(object):
    def __init__(self):
        databaseUri = os.environ.get("TA_MONGO_CONNECTION")

        if databaseUri is None:
            print("Variável de ambiente TA_MONGO_CONNECTION precisa ser criada.")
            exit(0)

        self.mongo_client = pymongo.MongoClient(databaseUri)
        self.database = self.mongo_client["tips_arena"]

    def get_collection(self, name):
        return self.database[name]

    def list_collections(self):
        return self.database.list_collection_names()

    def desconectar(self):
        self.mongo_client.close()

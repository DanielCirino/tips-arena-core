
# -*- coding: utf-8 -*-

import os
import pymongo


class MongoClient(object):
    def __init__(self):
        databaseUri = os.environ.get("TA_MONGO_CONNECTION")

        if databaseUri is None:
            print("Variavel de ambiente TA_MONGO_CONNECTION precisa ser criada.")
            exit(0)

        self.mongo_client = pymongo.MongoClient(databaseUri)
        self.database = self.mongo_client["tips_arena"]

    def getCollection(self, name):
        return self.database[name]

    def listCollections(self):
        return self.database.list_collection_names()

    def disconnect(self):
        self.mongo_client.close()

# -*- coding: utf-8 -*-

import os
import urllib

import pymongo


class MongoClient(object):
    def __init__(self):
        try:
            user = urllib.parse.quote_plus(os.environ.get("TA_MONGO_USER"))
            pwd = urllib.parse.quote_plus(os.environ.get("TA_MONGO_PWD"))
            server = urllib.parse.quote_plus(os.environ.get("TA_MONGO_SERVER"))
            port = urllib.parse.quote_plus(os.environ.get("TA_MONGO_PORT"))
            databaseName = urllib.parse.quote_plus(os.environ.get("TA_DATABASE_NAME"))

            databaseUri = "mongodb://{}:{}@{}:{}/{}".format(user, pwd, server, port, databaseName)

            print(pwd)

            if databaseUri is None:
                print("Variavel de ambiente TA_MONGO_CONNECTION precisa ser criada.")
                exit(0)

            self.mongo_client = pymongo.MongoClient(databaseUri)
            self.database = self.mongo_client[databaseName]
        except Exception as e:
            print(e.args[0])
            # print(databaseUri)

    def getCollection(self, name):
        return self.database[name]

    def listCollections(self):
        return self.database.list_collection_names()

    def disconnect(self):
        self.mongo_client.close()

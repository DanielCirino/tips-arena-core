# -*- coding: utf-8 -*-

import os
import urllib

import pymongo


class MongoClient(object):
    def __init__(self):
        try:
            user = os.environ["TA_MONGO_USER"]
            pwd = os.environ["TA_MONGO_PWD"]
            server = os.environ["TA_MONGO_SERVER"]
            port = os.environ["TA_MONGO_PORT"]
            databaseName = os.environ["TA_DATABASE_NAME"]

            databaseUri = "mongodb://{}:{}@{}:{}/{}".format(user, pwd, server, port, databaseName)
            databaseUri = os.environ["TA_MONGO_CONNECTION"]

            print(databaseUri)

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

#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId


class MongoClient(object):
    def __init__(self):
        self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database = self.mongo_client["tips_arena"]

    def get_collection(self, name):
        return self.database[name]

    def list_collections(self):
        return self.database.list_collection_names()

    def desconectar(self):
        self.mongo_client.close()

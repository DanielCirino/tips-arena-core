# -*- coding: utf-8 -*-
from datetime import datetime


class ItemExtracao(object):

  def __init__(self, documento: dict = {}):
    self.id: str
    self.url: str
    self.urlHash: str
    self.tipo: str
    self.dataHora: datetime

    if documento is not None:
      for key in documento:
        setattr(self, key, documento[key])

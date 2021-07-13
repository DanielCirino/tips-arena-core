# -*- coding: utf-8 -*-

class ItemExtracao(object):
  def __init__(self, documento: dict = {}):
    self._id = ""
    self.idPai = 0
    self.url = ""
    self.tipo = ""
    self.status = ""
    self.target = 0
    self.prioridadeExtracao = 0
    self.dataCadastro = ""
    self.dataAtualizacao = ""

    if documento is not None:
      for key in documento:
        setattr(self, key, documento[key])

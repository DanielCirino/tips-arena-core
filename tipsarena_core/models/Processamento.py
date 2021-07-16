# -*- coding: utf-8 -*-

from datetime import datetime
from enum import Enum


class Processamento(object):
  def __init__(self, documento: dict = {}):
    self._id = ""
    self.tipo = ""
    self.status = ""
    self.totalRegistros = 0
    self.totalSucesso = 0
    self.totalErro = 0
    self.detalhes = 0
    self.dataHoraInicio = datetime.now()
    self.dataHoraFim = None
    self.dataAtualizacao = datetime.now()

    if documento is not None:
      for key in documento:
        setattr(self, key, documento[key])

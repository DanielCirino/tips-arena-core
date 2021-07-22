# -*- coding: utf-8 -*-
from enum import Enum

class STATUS(Enum):
  PENDENTE = 1
  FINALIZADA = 2
  CANCELADA = 3


class MERCADO(Enum):
  RESULTADO = 1
  DNB = 2
  DUPLA_CHANCE = 3
  IMPAR_PAR = 4
  AMBOS_MARCAM = 5
  PLACAR_EXATO = 6
  UNDER_OVER = 7


class RESULTADO(Enum):
  PENDENTE = 1
  LUCRO = 2
  PREJUIZO = 3
  CANCELADA = 4

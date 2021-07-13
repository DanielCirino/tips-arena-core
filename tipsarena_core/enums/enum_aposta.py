from enum import Enum

class STATUS(Enum):
  PENDENTE = 1
  FINALIZADA = 2
  CANCELADA = 3


class MERCADOS(Enum):
  RESULT = 1
  DNB = 2
  DOUBLE_CHANCE = 3
  ODD_EVEN = 4
  BTTS = 5
  CORRECT_SCORE = 6
  UNDER_OVER = 7


class RESULTADO(Enum):
  PENDENTE = 1
  LUCRO = 2
  PREJUIZO = 3
  CANCELADA = 4

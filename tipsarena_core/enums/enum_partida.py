from enum import Enum


class STATUS(Enum):
  AGENDADO = 1
  ADIADO = 2
  SUSPENSO = 3
  CANCELADO = 4
  PRIMEIRO_TEMPO = 5
  INTERVALO = 6
  SEGUNDO_TEMPO = 7
  FINALIZADO = 8
  EM_ANDAMENTO = 9
  ABANDONADO = 10
  RESULTADO_NAO_DISPONIVEL = 11
  W_O = 12


class CALCULO_PROBABILIDADE(Enum):
  PENDENTE = 1
  CALCULADO = 2
  ERRO = 3


class ANALISE_PROBABILIDADE(Enum):
  PENDENTE = 1
  ANALISADO = 2
  ERRO = 3

class TIPO_MERCADO(Enum):
  RESULTADO = "1x2-odds"""
  DNB = "home-away"
  UNDER_OVER = "acima-abaixo"
  PLACAR = "correct-score"
  BTTS = "ambos-marcam"
  ODD_EVEN = "odd-even"
  DUPLA_CHANCE = "double-chance"

class MERCADO(Enum):
  RESULTADO = 1
  UNDER = 2
  OVER = 3
  DNB = 4
  PLACAR = 5
  BTTS_YES = 6
  BTTS_NO = 7
  ODD = 8
  EVEN = 9
  CONTRA_MANDANTE = 10
  CONTRA_EMPATE = 11
  CONTRA_VISITANTE = 12
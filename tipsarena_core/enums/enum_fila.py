from enum import Enum


class Fila(Enum):
  FILA_PROCESSAMENTO_HTML_PAISES = "ta-processamento-html-paises"
  FILA_EXTRACAO_COMPETICOES_PAIS = "ta-extracao-competicoes-pais"

  FILA_EXTRACAO_EDICOES_COMPETICAO = "ta-extracao-edicoes-competicao"
  FILA_PROCESSAMENTO_EDICAO_COMPETICAO = "ta-processamento-edicao-competicao"

  FILA_EXTRACAO_PARTIDAS_EDICAO_COMPETICAO = "ta-extracao-partidas-edicao-competicao"
  FILA_PROCESSAMENTO_PARTIDA_EDICAO_COMPETICAO = "ta-processamento-partida-edicao-competicao"

  FILA_EXTRACAO_EQUIPES_EDICAO_COMPETICAO = "ta-extracao-equipes-edicao-competicao"
  FILA_PROCESSAMENTO_EQUIPE = "ta-processamento-equipe"

# -*- coding: utf-8 -*-
import os

from tipsarena_core import gerenciador_filas
from tipsarena_core.enums.enum_fila import Fila as FILA
from tipsarena_core.extratores.flash_score import extrator_pais, extrator_competicao, extrator_edicao_competicao, \
  extrator_equipe, extrator_partida
from tipsarena_core.parsers_html.flash_score import parser_pais, parser_competicao, parser_edicao_competicao, \
  parser_partida, parser_equipe, parser_partida_timeline,parser_partida_estatisticas,parser_partida_odds,parser_partida_head_to_head


def extrairHtmlPaises():
  dadosExtracao = extrator_pais.extrairHtmlPaises()

  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}{dadosExtracao.id.lower()}.html"
  with open(caminhoArquivo, mode="w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_LISTA_PAISES.value,
                                     dadosExtracao.__dict__)


def processarHtmlPaises(caminhoParaArquivo):
  with open(caminhoParaArquivo, "r") as arquivo:
    listaPaises = parser_pais.processarHtmlListaPaises(arquivo)

    for itemProcessamento in listaPaises:
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_COMPETICOES_PAIS.value, itemProcessamento.__dict__)


def extrairHtmlCompeticoesPais(urlPais: str):
  dadosExtracao = extrator_competicao.extrairHtmlCompeticoesPais(urlPais)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}{dadosExtracao.id.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_COMPETICOES_PAIS.value,
                                     dadosExtracao.__dict__)


def processarHtmlCompeticoesPais(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    listaCompeticoes = parser_competicao.processarHtmlCompeticoesPais(html)

    for competicao in listaCompeticoes:
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_EDICOES_COMPETICAO.value, competicao.__dict__)


def extrairHtmlEdicoesCompeticao(urlCompeticao: str):
  dadosExtracao = extrator_competicao.extrairHtmlEdicoesCompeticao(urlCompeticao)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}{dadosExtracao.id.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_EDICOES_COMPETICAO.value,
                                     dadosExtracao.__dict__)


def processarHtmlEdicoesCompeticao(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    listaEdicoes = parser_competicao.processarHtmlEdicoesCompeticao(html)

    for edicao in listaEdicoes:
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_EDICAO_COMPETEICAO.value, edicao)
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDAS_EDICAO_COMPETICAO.value, edicao)
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_EQUIPES_EDICAO_COMPETICAO.value, edicao)


def extrairHtmlEdicaoCompeticao(urlEdicao: str):
  dadosExtracao = extrator_edicao_competicao.extrairHtmlEdicaoCompeticao(urlEdicao)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}edicao_competicao/{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_EDICAO_COMPETICAO.value,
                                     dadosExtracao.__dict__)


def processarHtmlEdicaoCompeticao(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    edicaoCompeticao = parser_edicao_competicao.processarHtmlEdicaoCompeticao(html)
    pass


def extrairHtmlPartidasEdicaoCompeticao(urlEdicao: str):
  htmlPartidasFinalizadas = extrator_edicao_competicao.extrairHtmlPartidasFinalizadasEdicaoCompeticao(urlEdicao)
  caminhoArquivoPartidasFinalizadas = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/{htmlPartidasFinalizadas.urlHash.lower()}.html"

  with open(caminhoArquivoPartidasFinalizadas, "w") as arquivo:
    arquivo.write(htmlPartidasFinalizadas.html)

  htmlPartidasAgendadas = extrator_edicao_competicao.extrairHtmlPartidasAgendadasEdicaoCompeticao(urlEdicao)
  caminhoArquivoPartidasAgendadas = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/{htmlPartidasAgendadas.urlHash.lower()}.html"

  with open(caminhoArquivoPartidasAgendadas, "w") as arquivo:
    arquivo.write(htmlPartidasAgendadas.html)


def processarHtmlPartidasEdicaoCompeticao(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    partidas = parser_partida.processarHtmlListaPartidas(html)
    for partida in partidas:
      pass


def extrairHtmlEquipesEdicaoCompeticao(urlEdicao: str):
  dadosExtracao = extrator_equipe.extrairHtmlEquipesEdicaoCompeticao(urlEdicao)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}equipe/{dadosExtracao.id.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_EQUIPES_EDICAO_COMPETICAO.value,
                                     dadosExtracao.__dict__)


def processarHtmlEquipesEdicaoCompeticao(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    equipes = parser_equipe.processarHtmlEquipesCompeticao(html)
    for equipe in equipes:
      pass


def extrairHtmlPartida(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlPartida(urlPartida)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def processarHtmlPartida(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    partida = parser_partida.processarHtmlPartida(html)
    pass


def processarHtmlTimelinePartida(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    timeline = parser_partida_timeline.processarHtmlTimeline(html)
    for evento in timeline:
      pass


def extrairHtmlEstatisticasPartida(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlEstatisticasPartida(urlPartida)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/estatisticas/{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def processarHtmlEstatisticasPartida(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    estatisticas = parser_partida_estatisticas.processarHtmlEstatisticas(html)
    for estatistica in estatisticas:
      pass

def extrairHtmlCotacoesResultado(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlOddsPartida(urlPartida)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/odd/{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def processarHtmlCotacoesResultado(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    cotacoes = parser_partida_odds.processarHtmlOddsResultado(html)
    for cotacao in cotacoes:
      pass


if __name__ == "__main__":
  # extrairHtmlPaises()
  # processarHtmlPaises('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/f3a928ab-510a-44f6-8be1-1916a712ef54.html')
  # extrairHtmlCompeticoesPais("http://www.flashscore.com.br/futebol/inglaterra/")
  # processarHtmlCompeticoesPais(
  #   "/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/83fece40-18b7-48a3-b390-02ce6679e6ca.html")
  # extrairHtmlEdicoesCompeticao("https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles/")
  # processarHtmlEdicoesCompeticao(
  #   '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/ed8b349f-b819-4fee-b164-3de2f8f678c1.html')
  # extrairHtmlEdicaoCompeticao("https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles-2019-2020/")
  # processarHtmlEdicaoCompeticao(
  #   '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/edicao_competicao/520e812bf705531d64c8ea8e.html')
  # extrairHtmlPartidasEdicaoCompeticao("https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles-2019-2020/")
  # processarHtmlPartidasEdicaoCompeticao(
  #   '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/6260cdd1-40b8-4a2a-a754-e66df5d85ca1.html')
  # extrairHtmlEquipesEdicaoCompeticao("https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles-2019-2020/")
  # processarHtmlEquipesEdicaoCompeticao('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/equipe/6105e77d-7c00-4b66-a6c2-b864d78ba510.html')
  # extrairHtmlPartida("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  # processarHtmlPartida('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/09ae7cbc7754c616ff4da36f.html')
  # processarHtmlTimelinePartida(
  #   '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/09ae7cbc7754c616ff4da36f.html')
  # extrairHtmlEstatisticasPartida("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  # processarHtmlEstatisticasPartida('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/estatisticas/09ae7cbc7754c616ff4da36f.html')
  # extrairHtmlCotacoesResultado("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  processarHtmlCotacoesResultado('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/odd/09ae7cbc7754c616ff4da36f.html')
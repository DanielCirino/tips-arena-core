# -*- coding: utf-8 -*-
import os

from tipsarena_core import gerenciador_filas
from tipsarena_core.enums.enum_fila import Fila as FILA
from tipsarena_core.extratores.flash_score import extrator_pais, extrator_competicao
from tipsarena_core.parsers_html.flash_score import parser_pais, parser_competicao, parser_edicao_competicao


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



def extrairHtmlEdicaoCompeticao(urlEdicao:str):
  pass

def processarHtmlEdicaoCompeticao(caminhoArquivo:str):
  pass

def extrairHtmlPartidasEdicaoCompeticao(urlEdicao:str):
  pass

def processarHtmlPartidasEdicaoCompeticao(caminhoArquivo):
  pass

def extrairHtmlEquipesEdicaoCompeticao(urlEdicao:str):
  pass

def processarHtmlEquipesEdicaoCompeticao(urlEdicao:str):
  pass

def extrairHtmlPartida(urlPartida:str):
  pass

def processarHtmlPartida(caminhoArquivo:str):
  pass

def extrairHtmlEstatisticasPartida(urlPartida:str):
  pass

if __name__ == "__main__":
  # extrairHtmlPaises()
  # processarHtmlPaises('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/f3a928ab-510a-44f6-8be1-1916a712ef54.html')
  # extrairHtmlCompeticoesPais("http://www.flashscore.com.br/futebol/inglaterra/")
  # processarHtmlCompeticoesPais(
  #   "/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/83fece40-18b7-48a3-b390-02ce6679e6ca.html")
  # extrairHtmlEdicoesCompeticao("https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles/")
  processarHtmlEdicoesCompeticao(
    '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/ed8b349f-b819-4fee-b164-3de2f8f678c1.html')

# -*- coding: utf-8 -*-
import os

from tipsarena_core import gerenciador_filas
from tipsarena_core.enums.enum_fila import FILA
from tipsarena_core.enums.enum_aposta import MERCADO
from tipsarena_core.extratores.flash_score import extrator_pais, extrator_competicao, extrator_edicao_competicao, \
  extrator_equipe, extrator_partida


def extrairHtmlPaises():
  dadosExtracao = extrator_pais.extrairHtmlPaises()

  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}pais/paises-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, mode="w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_LISTA_PAISES.value,
                                     dadosExtracao.__dict__)


def extrairHtmlCompeticoesPais(urlPais: str):
  dadosExtracao = extrator_competicao.extrairHtmlCompeticoesPais(urlPais)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}competicao/cmp-ps-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_COMPETICOES_PAIS.value,
                                     dadosExtracao.__dict__)


def extrairHtmlEdicoesCompeticao(urlCompeticao: str):
  dadosExtracao = extrator_competicao.extrairHtmlEdicoesCompeticao(urlCompeticao)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}edicao_competicao/edc-cmp-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_EDICOES_COMPETICAO.value,
                                     dadosExtracao.__dict__)


def extrairHtmlEdicaoCompeticao(urlEdicao: str):
  dadosExtracao = extrator_edicao_competicao.extrairHtmlEdicaoCompeticao(urlEdicao)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}edicao_competicao/edc-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_EDICAO_COMPETICAO.value,
                                     dadosExtracao.__dict__)


def extrairHtmlPartidasEdicaoCompeticao(urlEdicao: str):
  htmlPartidasFinalizadas = extrator_edicao_competicao.extrairHtmlPartidasFinalizadasEdicaoCompeticao(urlEdicao)
  caminhoArquivoPartidasFinalizadas = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/ptd-edc-{htmlPartidasFinalizadas.urlHash.lower()}.html"

  with open(caminhoArquivoPartidasFinalizadas, "w") as arquivo:
    arquivo.write(htmlPartidasFinalizadas.html)

  htmlPartidasAgendadas = extrator_edicao_competicao.extrairHtmlPartidasAgendadasEdicaoCompeticao(urlEdicao)
  caminhoArquivoPartidasAgendadas = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/ptd-edc-{htmlPartidasAgendadas.urlHash.lower()}.html"

  with open(caminhoArquivoPartidasAgendadas, "w") as arquivo:
    arquivo.write(htmlPartidasAgendadas.html)


def extrairHtmlEquipesEdicaoCompeticao(urlEdicao: str):
  dadosExtracao = extrator_equipe.extrairHtmlEquipesEdicaoCompeticao(urlEdicao)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}equipe/eqp-edc{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_PROC_HTML_EQUIPES_EDICAO_COMPETICAO.value,
                                     dadosExtracao.__dict__)


def extrairHtmlPartida(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlPartida(urlPartida)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/ptd-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def extrairHtmlEstatisticasPartida(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlEstatisticasPartida(urlPartida)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/estatisticas/ptd-stat-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)

def extrairHtmlConfrontosEquipes(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlUltimasPartidasEquipes(urlPartida)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/confrontos/ptd-h2h-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def extrairHtmlCotacoesResultado(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlOddsPartida(urlPartida, MERCADO.RESULTADO)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/odd/ptd-odd-rst-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def extrairHtmlCotacoesDNB(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlOddsPartida(urlPartida, MERCADO.DNB)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/odd/ptd-odd-dnb-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def extrairHtmlCotacoesDuplaChance(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlOddsPartida(urlPartida, MERCADO.DUPLA_CHANCE)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/odd/ptd-odd-dc{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def extrairHtmlCotacoesImparPar(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlOddsPartida(urlPartida, MERCADO.IMPAR_PAR)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/odd/ptd-odd-ip-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def extrairHtmlCotacoesAmbosMarcam(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlOddsPartida(urlPartida, MERCADO.AMBOS_MARCAM)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/odd/ptd-odd-btts{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def extrairHtmlCotacoesPlacarExato(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlOddsPartida(urlPartida, MERCADO.PLACAR_EXATO)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/odd/ptd-odd-plc-{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


def extrairHtmlCotacoesUnderOver(urlPartida: str):
  dadosExtracao = extrator_partida.extrairHtmlOddsPartida(urlPartida, MERCADO.UNDER_OVER)
  caminhoArquivo = f"{os.getenv('TA_DIR_ARQUIVOS_PARA_PROCESSAR')}partida/odd/ptd-odd-uo{dadosExtracao.urlHash.lower()}.html"
  with open(caminhoArquivo, "w") as arquivo:
    arquivo.write(dadosExtracao.html)

  dadosExtracao.html = None

  gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,
                                     dadosExtracao.__dict__)


if __name__ == "__main__":
  extrairHtmlPaises()
  extrairHtmlCompeticoesPais("http://www.flashscore.com.br/futebol/inglaterra/")
  extrairHtmlEdicoesCompeticao("https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles/")

  extrairHtmlPartidasEdicaoCompeticao("https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles-2019-2020/")
  extrairHtmlEquipesEdicaoCompeticao("https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles-2019-2020/")
  extrairHtmlPartida("https://www.flashscore.com.br/jogo/AwCj20Vo/")

  extrairHtmlEstatisticasPartida("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  extrairHtmlConfrontosEquipes("https://www.flashscore.com.br/jogo/AwCj20Vo/")

  extrairHtmlCotacoesResultado("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  extrairHtmlCotacoesDNB("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  extrairHtmlCotacoesDuplaChance("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  extrairHtmlCotacoesImparPar("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  extrairHtmlCotacoesAmbosMarcam("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  extrairHtmlCotacoesPlacarExato("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  extrairHtmlCotacoesUnderOver("https://www.flashscore.com.br/jogo/AwCj20Vo/")
  pass

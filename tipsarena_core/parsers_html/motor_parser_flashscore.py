# -*- coding: utf-8 -*-

from tipsarena_core import gerenciador_filas
from tipsarena_core.enums.enum_fila import FILA as FILA
from tipsarena_core.parsers_html.flash_score import parser_pais, parser_competicao, parser_edicao_competicao, \
  parser_partida, parser_equipe, parser_partida_timeline, parser_partida_estatisticas, parser_partida_odds


def processarHtmlPaises(caminhoParaArquivo):
  with open(caminhoParaArquivo, "r") as arquivo:
    listaPaises = parser_pais.processarHtmlListaPaises(arquivo)

    for itemProcessamento in listaPaises:
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_COMPETICOES_PAIS.value, itemProcessamento.__dict__)


def processarHtmlCompeticoesPais(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    listaCompeticoes = parser_competicao.processarHtmlCompeticoesPais(html)

    for competicao in listaCompeticoes:
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_EDICOES_COMPETICAO.value, competicao.__dict__)


def processarHtmlEdicoesCompeticao(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    listaEdicoes = parser_competicao.processarHtmlEdicoesCompeticao(html)

    for edicao in listaEdicoes:
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_EDICAO_COMPETEICAO.value, edicao)
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDAS_EDICAO_COMPETICAO.value, edicao)
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_EQUIPES_EDICAO_COMPETICAO.value, edicao)


def processarHtmlEdicaoCompeticao(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    edicaoCompeticao = parser_edicao_competicao.processarHtmlEdicaoCompeticao(html)
    pass


def processarHtmlPartidasEdicaoCompeticao(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    partidas = parser_partida.processarHtmlListaPartidas(html)
    for partida in partidas:
      gerenciador_filas.produzirMensagem(FILA.FL_EXT_HTML_PARTIDA.value,partida)



def processarHtmlEquipesEdicaoCompeticao(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    equipes = parser_equipe.processarHtmlEquipesCompeticao(html)
    for equipe in equipes:
      pass


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


def processarHtmlEstatisticasPartida(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    estatisticas = parser_partida_estatisticas.processarHtmlEstatisticas(html)
    for estatistica in estatisticas:
      pass


def processarHtmlCotacoesResultado(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    cotacoes = parser_partida_odds.processarHtmlOddsResultado(html)
    for cotacao in cotacoes:
      pass


def processarHtmlCotacoesDNB(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    cotacoes = parser_partida_odds.processarHtmlOddsDrawNoBet(html)
    pass


def processarHtmlCotacoesDuplaChance(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    cotacoes = parser_partida_odds.processarHtmlOddsDuplaChance(html)
    pass


def processarHtmlCotacoesImparPar(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    cotacoes = parser_partida_odds.processarHtmlOddsImparPar(html)
    pass


def processarHtmlCotacoesAmbosMarcam(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    cotacoes = parser_partida_odds.processarHtmlOddsBtts(html)
    pass


def processarHtmlCotacoesPlacarExato(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    cotacoes = parser_partida_odds.processarHtmlOddsPlacarExato(html)
    for cotacao in cotacoes:
      pass


def processarHtmlCotacoesUnderOver(caminhoParaArquivo: str):
  with open(caminhoParaArquivo, "r") as arquivo:
    html = arquivo.read()
    cotacoes = parser_partida_odds.processarHtmlOddsUnderOver(html)
    for cotacao in cotacoes:
      pass


if __name__ == "__main__":
  processarHtmlPaises('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/paises-b3a8ebf43551bf390ad6733f.html')
  # processarHtmlCompeticoesPais(
  #   "/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/83fece40-18b7-48a3-b390-02ce6679e6ca.html")
  # processarHtmlEdicoesCompeticao(
  #   '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/ed8b349f-b819-4fee-b164-3de2f8f678c1.html')
  # extrairHtmlEdicaoCompeticao("https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles-2019-2020/")
  # processarHtmlEdicaoCompeticao(
  #   '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/edicao_competicao/520e812bf705531d64c8ea8e.html')

  # processarHtmlPartidasEdicaoCompeticao(
  #   '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/6260cdd1-40b8-4a2a-a754-e66df5d85ca1.html')
  # extrairHtmlEquipesEdicaoCompeticao("https://www.flashscore.com.br/futebol/inglaterra/campeonato-ingles-2019-2020/")

  # processarHtmlEquipesEdicaoCompeticao('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/equipe/6105e77d-7c00-4b66-a6c2-b864d78ba510.html')
  # processarHtmlPartida('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/09ae7cbc7754c616ff4da36f.html')
  # processarHtmlEstatisticasPartida('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/estatisticas/09ae7cbc7754c616ff4da36f.html')
  # processarHtmlTimelinePartida(
  #   '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/09ae7cbc7754c616ff4da36f.html')
  # processarHtmlCotacoesResultado(
  #   '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/odd/09ae7cbc7754c616ff4da36f.html')
  # processarHtmlCotacoesDNB('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/odd/ab3567ca270bbefbd60dcf1e.html')
  # processarHtmlCotacoesDuplaChance('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/odd/30b2c165536df3d3335fb4f3.html')
  # processarHtmlCotacoesImparPar('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/odd/b6460593435c695a7302a892.html')
  # processarHtmlCotacoesAmbosMarcam('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/odd/4edbd6bc5682ecd5ae1725c1.html')
  # processarHtmlCotacoesPlacarExato('/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/odd/78c09da5c2fbe222a8ae6bde.html')
  # processarHtmlCotacoesUnderOver(
  #   '/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partida/odd/4aa57f80a1e0a68e08f3f154.html')

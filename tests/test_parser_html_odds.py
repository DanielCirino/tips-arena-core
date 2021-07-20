# -*- coding: utf-8 -*-
import pathlib
from tipsarena_core.parsers_html.flash_score import parser_partida_odds


def teste_parser_html_mercados_disponiveis():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_odds_partida.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    mercadosDisponiveis = parser_partida_odds.processarHtmlMercadosApostaDisponiveis(html)
    assert len(mercadosDisponiveis) > 10


def teste_parser_html_processar_odds_resultado():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_odds_1_x_2.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    oddsResultado = parser_partida_odds.processarHtmlOddsResultado(html)
    assert len(oddsResultado) == 4


def teste_parser_html_processar_under_over():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_odds_under_over.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    oddsDnb = parser_partida_odds.processarHtmlOddsUnderOver(html)
    assert len(oddsDnb) == 13


def teste_parser_html_processar_odds_dnb():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_odds_dnb.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    oddsDnb = parser_partida_odds.processarHtmlOddsDrawNoBet(html)
    assert len(oddsDnb) == 3


def teste_parser_html_processar_placar_exato():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_odds_placar_exato.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    oddsDnb = parser_partida_odds.processarHtmlOddsPlacarExato(html)
    assert len(oddsDnb) == 78


def teste_parser_html_processar_odds_dupla_chance():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_odds_dupla_chance.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    oddsDnb = parser_partida_odds.processarHtmlOddsDuplaChance(html)
    assert len(oddsDnb) == 4


def teste_parser_html_processar_odds_impar_par():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_odds_impar_par.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    oddsDnb = parser_partida_odds.processarHtmlOddsImparPar(html)
    assert len(oddsDnb) == 3


def teste_parser_html_processar_odds_dupla_chance():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_odds_dupla_chance.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    oddsDnb = parser_partida_odds.processarHtmlOddsDuplaChance(html)
    assert len(oddsDnb) == 4


if __name__ == "__main__":
  teste_parser_html_processar_odds_dupla_chance()

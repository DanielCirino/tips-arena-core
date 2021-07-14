import pathlib
from tipsarena_core.parsers_html.flash_score import parser_partida


def teste_parser_html_lista_partidas():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_lista_partidas.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaPartidas = parser_partida.processarHtmlListaPartidas(html)
    assert len(listaPartidas) >= 105


def teste_parser_html_lista_partidas_do_dia():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_lista_partidas_hoje.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaPartidas = parser_partida.processarHtmlListaPartidas(html)
    assert len(listaPartidas) >= 200


def teste_parser_html_lista_partidas_ontem():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_lista_partidas_ontem.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaPartidas = parser_partida.processarHtmlListaPartidas(html)
    assert len(listaPartidas) >= 73


def teste_parser_html_lista_partidas_anteontem():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_lista_partidas_anteontem.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaPartidas = parser_partida.processarHtmlListaPartidas(html)
    assert len(listaPartidas) >= 105


def teste_parser_html_lista_partidas_amanha():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_lista_partidas_amanha.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaPartidas = parser_partida.processarHtmlListaPartidas(html)
    assert len(listaPartidas) >= 105


def teste_parser_html_lista_partidas_depois_de_amanha():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_lista_partidas_depois_de_amanha.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaPartidas = parser_partida.processarHtmlListaPartidas(html)
    assert len(listaPartidas) >= 105



if __name__ == "__main__":
  teste_parser_html_lista_partidas_do_dia()

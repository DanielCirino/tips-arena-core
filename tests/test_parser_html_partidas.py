import pathlib
from tipsarena_core.parsers_html.flash_score import parser_partida


def teste_parser_html_lista_partidas():
  caminhoArquivo = "/Volumes/HD/Documents/tips_arena/tests/arquivos/para_processar/partidas/partidas_edicao/ptd-edc-b7b0d43b51e5c8b475c55ee1.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaPartidas = parser_partida.processarHtmlListaPartidas(html)
    for partida in listaPartidas:
      print(partida)


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


def teste_parser_html_partida():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_partida.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    partida = parser_partida.processarHtmlPartida(html)
    assert len(partida) == 12


if __name__ == "__main__":
  teste_parser_html_lista_partidas()

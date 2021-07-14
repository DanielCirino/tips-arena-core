import pathlib
from tipsarena_core.parsers_html.flash_score import parser_partida_estatisticas


def teste_parser_html_estatisticas_partida():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_estatisticas_partida.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    estatisticas = parser_partida_estatisticas.processarHtmlEstatisticas(html)
    assert len(estatisticas) == 14


if __name__ == "__main__":
  teste_parser_html_estatisticas_partida()

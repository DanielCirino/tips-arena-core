import pathlib
from tipsarena_core.parsers_html.flash_score import parser_partida_timeline


def teste_parser_html_timeline_partida():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_timeline_partida.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    timeline = parser_partida_timeline.processarHtmlTimeline(html)
    assert len(timeline) == 26


if __name__ == "__main__":
  teste_parser_html_timeline_partida()

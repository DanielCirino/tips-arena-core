import pathlib
from tipsarena_core.parsers_html.flash_score import parser_pais


def teste_parser_html_paises():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_paises.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaPaises = parser_pais.processarHtmlListaPaises(html)
    assert len(listaPaises) >= 150


if __name__ == "__main__":
  teste_parser_html_paises()

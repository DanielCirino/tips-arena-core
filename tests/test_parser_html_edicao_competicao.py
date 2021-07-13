import pathlib
from tipsarena_core.parsers_html.flash_score import parser_competicao


def teste_parser_html_edicao_competicao():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_edicao_competicao.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    dadosCompeticao = parser_competicao.processarHtmlCompeticao(html)
    assert dadosCompeticao["anoEdicao"] == '2019'




if __name__ == "__main__":
  teste_parser_html_edicao_competicao()

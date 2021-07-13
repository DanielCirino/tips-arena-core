import pathlib
from tipsarena_core.parsers_html.flash_score import parser_equipe


def teste_parser_html_equipes_edicao_competicao():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_equipes_edicao.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    listaEquipes = parser_equipe.processarHtmlEquipesCompeticao(html)
    assert len(listaEquipes) >= 16

def teste_parser_html_equipe():
  caminhoArquivo = f"{pathlib.Path(__file__).parent.resolve()}/exemplos_html/exemplo_equipe.html"
  with open(caminhoArquivo) as arquivo:
    html = arquivo.read()
    equipe = parser_equipe.processarHtmlEquipe(html)
    assert equipe["nome"]=="RB Brasil"

if __name__ == "__main__":
  teste_parser_html_equipe()

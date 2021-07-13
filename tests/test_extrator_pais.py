from tipsarena_core.extratores.flash_score import extrator_pais


def teste_extracao_lista_paises():
  listaPaises = extrator_pais.obterListaPaises()
  assert len(listaPaises) > 150


if __name__ == '__main__':
  extrator_pais.obterListaPaises()
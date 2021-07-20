# -*- coding: utf-8 -*-
from tipsarena_core.utils import html_utils, string_utils
from tipsarena_core.enums.enum_partida import TIPO_MERCADO
from tipsarena_core.services import log_service as log

CASAS_DECIMAIS = 3
CSS_LISTA_ODDS = "div[class^=tableWrapper]"
CSS_LINHAS_ODDS = "div[class^=row_]"
CSS_INFO_CASA_APOSTA = "div[class^=bookmakerPart] div a"


def processarHtmlMercadosApostaDisponiveis(elemento: str):
  try:
    CSS_MERCADOS = "#detail > div > div.tabs a"

    htmlOdds = html_utils.converterStringParaHtml(elemento)
    htmlMercadosDisponiveis = htmlOdds.select(CSS_MERCADOS)

    listaMercadosDisponiveis = []

    for elemento in htmlMercadosDisponiveis:
      linkMercado = elemento.attrs["href"]
      nomeMercado = elemento.attrs["title"]
      codigoMercado = string_utils.limparString(elemento.text.upper())  # 1X2,CASA/FORA ,O/U, DC, EXATO, I/P, AM

      mercado = {"link": linkMercado,
                 "tipo": "",
                 "nome": nomeMercado,
                 "codigo": codigoMercado}

      if codigoMercado == "1X2":
        mercado["tipo"] = TIPO_MERCADO.RESULTADO
      elif codigoMercado == 'O/U':
        mercado["tipo"] = TIPO_MERCADO.UNDER_OVER
      elif codigoMercado == 'CASA/FORA':
        mercado["tipo"] = TIPO_MERCADO.DNB
      # elif codigoMercado == 'bookmark-asian-handicap':
      #     print('')
      # elif codigoMercado == 'bookmark-european-handicap':
      #     print('')
      elif codigoMercado == 'AM':
        mercado["tipo"] = TIPO_MERCADO.DUPLA_CHANCE
      # elif codigoMercado == 'bookmark-ht-ft':
      #     print('')
      elif codigoMercado == 'EXATO':
        mercado["tipo"] = TIPO_MERCADO.PLACAR
      elif codigoMercado == 'I/P':
        mercado["tipo"] = TIPO_MERCADO.ODD_EVEN
      elif codigoMercado == 'AM':
        mercado["tipo"] = TIPO_MERCADO.BTTS
      else:
        pass

      listaMercadosDisponiveis.append(mercado)

    return listaMercadosDisponiveis

  except Exception as e:
    log.ERRO("Não foi possível obter mercados disponíveis para aposta.", e.args)
    return []


def processarHtmlOddsPartida(html: str):
  try:

    oddsPartida = {
      "resultado": {},
      "duplaChance": {},
      "drawNoBet": {},
      "oddEven": {},
      "btts": {},
      "underOver": [],
      "placarExato": []
    }
    mercadosDisponiveis = processarHtmlMercadosApostaDisponiveis(html)

    for mercado in mercadosDisponiveis:
      odds = extrairOddsPorMercado(mercado, html)

      if mercado["tipo"] == TIPO_MERCADO.RESULTADO:
        oddsPartida["resultado"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.DUPLA_CHANCE:
        oddsPartida["duplaChance"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.DNB:
        oddsPartida["drawNoBet"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.ODD_EVEN:
        oddsPartida["oddEven"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.BTTS:
        oddsPartida["btts"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.UNDER_OVER:
        oddsPartida["underOver"] = odds

      elif mercado["tipo"] == TIPO_MERCADO.PLACAR:
        oddsPartida["placarExato"] = odds

    return oddsPartida

  except Exception as e:
    log.ERRO("Erro ao obter odds da partida [{}]", e.args)
    return oddsPartida


def extrairOddsPorMercado(mercado, html: str):
  try:
    htmlOdds = html_utils.converterStringParaHtml(html)
    tabelaOdds = htmlOdds.select_one(CSS_LISTA_ODDS)

    if mercado["tipo"] == TIPO_MERCADO.RESULTADO: return processarHtmlOddsResultado(str(tabelaOdds))

    if mercado["tipo"] == TIPO_MERCADO.UNDER_OVER:
      listaOdds = []
      tabelasUnderOver = tabelaOdds.select("[class^=table_]")
      for tabela in tabelasUnderOver:
        odds = processarHtmlOddsUnderOver(str(tabela))
        if odds != {}:
          listaOdds.append(odds)
      return listaOdds

    if mercado["tipo"] == TIPO_MERCADO.DNB: return processarHtmlOddsDrawNoBet(str(tabelaOdds))

    if mercado["tipo"] == TIPO_MERCADO.BTTS: return processarHtmlOddsBtts(str(tabelaOdds))

    if mercado["tipo"] == TIPO_MERCADO.PLACAR:
      listaOdds = []
      tabelasPlacarExato = tabelaOdds.select("[class^=table_]")
      for tabela in tabelasPlacarExato:
        odds = processarHtmlOddsPlacarExato(str(tabela))
        if odds != {}:
          listaOdds.append(odds)

      return listaOdds

    if mercado["tipo"] == TIPO_MERCADO.ODD_EVEN: return processarHtmlOddsImparPar(str(tabelaOdds))

    if mercado["tipo"] == TIPO_MERCADO.DUPLA_CHANCE: return processarHtmlOddsDuplaChance(str(tabelaOdds))

  except Exception as e:
    log.ERRO(f"Não foi possível obter ODDS para o mercado {mercado}.", e.args)
    return []


def processarHtmlOddsResultado(html: str):
  redutorQuantidadeMandante = 0
  redutorQuantidadeEmpate = 0
  redutorQuantidadeVisitante = 0

  valorOddsMandante = 0
  valorOddsEmpate = 0
  valorOddsVisitante = 0

  listaOdds = []

  try:
    htmlOdds = html_utils.converterStringParaHtml(html)
    htmlListaOdds = htmlOdds.select(CSS_LINHAS_ODDS)
    quantidadeOdds = len(htmlListaOdds)

    for elemento in htmlListaOdds:
      infoCasaAposta = elemento.select_one(CSS_INFO_CASA_APOSTA).attrs["title"]
      opcoes = elemento.select("a[class^=odd_]")

      oddMandante = opcoes[0].text.replace("-", "0")
      oddEmpate = opcoes[1].text.replace("-", "0")
      oddVisitante = opcoes[2].text.replace("-", "0")

      listaOdds.append(
        {"casaAposta": infoCasaAposta,
         "oddMandante": float(oddMandante),
         "oddEmpate": float(oddEmpate),
         "oddVisitante": float(oddVisitante)
         }
      )

      if oddMandante == "0": redutorQuantidadeMandante += 1
      if oddEmpate == "0": redutorQuantidadeEmpate += 1
      if oddVisitante == "0": redutorQuantidadeVisitante += 1

      valorOddsMandante += float(oddMandante)
      valorOddsEmpate += float(oddEmpate)
      valorOddsVisitante += float(oddVisitante)

    return {
      "mandante": round(valorOddsMandante / (quantidadeOdds - redutorQuantidadeMandante),
                        CASAS_DECIMAIS),
      "empate": round(valorOddsEmpate / (quantidadeOdds - redutorQuantidadeEmpate), CASAS_DECIMAIS),
      "visitante": round(valorOddsVisitante / (quantidadeOdds - redutorQuantidadeVisitante),
                         CASAS_DECIMAIS),
      "listaOdds": listaOdds
    }

  except Exception as e:
    log.ERRO("Não foi possível processar ODDs de resultado.", e.args)
    return {}


def processarHtmlOddsDrawNoBet(html: str):
  redutorQuantidadeMandante = 0
  redutorQuantidadeVisitante = 0

  valorOddsMandante = 0
  valorOddsVisitante = 0
  listaOdds = []

  try:
    htmlOdds = html_utils.converterStringParaHtml(html)
    htmlListaOdds = htmlOdds.select(CSS_LINHAS_ODDS)
    quantidadeOdds = len(htmlListaOdds)

    for elemento in htmlListaOdds:
      infoCasaAposta = elemento.select_one(CSS_INFO_CASA_APOSTA).attrs["title"]
      opcoes = elemento.select("a[class^=odd_]")

      oddMandante = opcoes[0].text.replace("-", "0")
      oddVisitante = opcoes[1].text.replace("-", "0")

      listaOdds.append(
        {"casaAposta": infoCasaAposta,
         "oddMandante": float(oddMandante),
         "oddVisitante": float(oddVisitante)
         }
      )

      if oddMandante == "0": redutorQuantidadeMandante += 1
      if oddVisitante == "0": redutorQuantidadeVisitante += 1

      valorOddsMandante += float(oddMandante)
      valorOddsVisitante += float(oddVisitante)

    return {
      "mandante": round(valorOddsMandante / (quantidadeOdds - redutorQuantidadeMandante),
                        CASAS_DECIMAIS),
      "visitante": round(valorOddsVisitante / (quantidadeOdds - redutorQuantidadeVisitante),
                         CASAS_DECIMAIS),
      "listaOdds": listaOdds
    }

  except Exception as e:
    log.ERRO(f"Não foi possível obter odds DNB.", e.args)
    return {}


def processarHtmlOddsUnderOver(html: str):
  try:
    listaOddsUnderOver = []
    htmlOdds = html_utils.converterStringParaHtml(html)
    tabelasUnderOver = htmlOdds.select("[class^=table_]")

    for tabela in tabelasUnderOver:
      redutorQuantidadeUnder = 0
      redutorQuantidadeOver = 0

      valorOddsOver = 0
      valorOddsUnder = 0
      listaOdds = []

      htmlListaOdds = tabela.select(CSS_LINHAS_ODDS)
      quantidadeOdds = len(htmlListaOdds)


      for elemento in htmlListaOdds:
        quantidadeGols = elemento.select_one("[class^=noOddsCell_]").text
        infoCasaAposta = elemento.select_one(CSS_INFO_CASA_APOSTA).attrs["title"]
        opcoes = elemento.select("a[class^=odd_]")

        oddOver = opcoes[0].text.replace("-", "0")
        oddUnder = opcoes[1].text.replace("-", "0")

        listaOdds.append(
          {"casaAposta": infoCasaAposta,
           "gols": quantidadeGols,
           "oddOver": float(oddOver),
           "oddUnder": float(oddUnder)
           }
        )

        if oddOver == "0": redutorQuantidadeOver += 1
        if oddUnder == "0": redutorQuantidadeUnder += 1

        valorOddsOver += float(oddOver)
        valorOddsUnder += float(oddUnder)

      listaOddsUnderOver.append({
        "totalGols": float(quantidadeGols),
        "under": round(valorOddsUnder / (quantidadeOdds - redutorQuantidadeUnder), CASAS_DECIMAIS),
        "over": round(valorOddsOver / (quantidadeOdds - redutorQuantidadeOver), CASAS_DECIMAIS),
        "listaOdds": listaOdds
      })

    return listaOddsUnderOver


  except Exception as e:
    log.ERRO("Não foi possível processar odds under/over.", e.args)
    return {}


def processarHtmlOddsPlacarExato(html: str):
  try:
    listaOddsPlacarExato = []
    htmlOdds = html_utils.converterStringParaHtml(html)
    tabelasPlacarExato = htmlOdds.select("[class^=table_]")

    for tabela in tabelasPlacarExato:
      redutorQuantidadeOdds = 0
      valorOddsPlacar = 0
      listaOdds = []

      htmlListaOdds = tabela.select(CSS_LINHAS_ODDS)
      quantidadeOdds = len(htmlListaOdds)
      placar = htmlListaOdds[0].select_one("[class^=noOddsCell_]").text

      for elemento in htmlListaOdds:
        infoCasaAposta = elemento.select_one(CSS_INFO_CASA_APOSTA).attrs["title"]
        opcoes = elemento.select("a[class^=odd_]")

        oddPlacar = opcoes[0].text.replace("-", "0")
        listaOdds.append(
          {"casaAposta": infoCasaAposta,
           "placar": placar,
           "odd": float(oddPlacar)
           }
        )

        if oddPlacar == "0": redutorQuantidadeOdds += 1
        valorOddsPlacar += float(oddPlacar)

      quantidadesGol = placar.split(":")

      listaOddsPlacarExato.append({
        "placarMandante": quantidadesGol[0],
        "placarVisitante": quantidadesGol[1],
        "valor": round(valorOddsPlacar / (quantidadeOdds - redutorQuantidadeOdds), CASAS_DECIMAIS),
        "listaOdds": listaOdds
      })

    return listaOddsPlacarExato
  except Exception as e:
    log.ERRO("Não foi possível processar ODDs de placar exato.", e.args)
    return {}


def processarHtmlOddsBtts(html:str):
  redutorQuantidadeBtts = 0
  redutorQuantidadeNoBtts = 0

  valorOddsBtts = 0
  valorOddsNoBtts = 0
  listaOdds = []
  try:
    htmlOdds = html_utils.converterStringParaHtml(html)
    htmlListaOdds = htmlOdds.select(CSS_LINHAS_ODDS)
    quantidadeOdds = len(htmlListaOdds)

    for elemento in htmlListaOdds:
      infoCasaAposta = elemento.select_one(CSS_INFO_CASA_APOSTA).attrs["title"]
      opcoes = elemento.select("a[class^=odd_]")

      oddBtts = opcoes[0].text.replace("-", "0")
      oddNoBtts = opcoes[1].text.replace("-", "0")

      listaOdds.append({"casaAposta": infoCasaAposta,
                        "yes": float(oddBtts),
                        "no": float(oddNoBtts)})

      if oddBtts == "0": redutorQuantidadeBtts += 1
      if oddNoBtts == "0": redutorQuantidadeNoBtts += 1

      valorOddsBtts += float(oddBtts)
      valorOddsNoBtts += float(oddNoBtts)

    return {
      "yes": round(valorOddsBtts / (quantidadeOdds - redutorQuantidadeBtts), CASAS_DECIMAIS),
      "no": round(valorOddsNoBtts / (quantidadeOdds - redutorQuantidadeNoBtts), CASAS_DECIMAIS),
      "listaOdds": listaOdds
    }

  except Exception as e:
    log.ERRO("Não foi possível processar ODDs BTTS.", e.args)
    return {}


def processarHtmlOddsImparPar(html: str):
  redutorQuantidadeImpar = 0
  redutorQuantidadePar = 0

  valorOddImpar = 0
  valorOddPar = 0
  listaOdds = []

  try:
    htmlOdds = html_utils.converterStringParaHtml(html)
    htmlListaOdds = htmlOdds.select(CSS_LINHAS_ODDS)
    quantidadeOdds = len(htmlListaOdds)

    for elemento in htmlListaOdds:
      infoCasaAposta = elemento.select_one(CSS_INFO_CASA_APOSTA).attrs["title"]
      opcoes = elemento.select("a[class^=odd_]")

      oddImpar = opcoes[0].text.replace("-", "0")
      oddPar = opcoes[1].text.replace("-", "0")

      listaOdds.append({"casaAposta": infoCasaAposta,
                        "odd": float(oddImpar),
                        "even": float(oddPar)})

      if oddImpar == "0": redutorQuantidadeImpar += 1
      if oddPar == "0": redutorQuantidadePar += 1

      valorOddImpar += float(oddImpar)
      valorOddPar += float(oddPar)

    return {
      "odd": round(valorOddImpar / (quantidadeOdds - redutorQuantidadeImpar), CASAS_DECIMAIS),
      "even": round(valorOddPar / (quantidadeOdds - redutorQuantidadePar), CASAS_DECIMAIS),
      "listaOdds": listaOdds
    }

  except Exception as e:
    log.ERRO("Não foi possível processar ODDs IMPAR/PAR.", e.args)
    return {}


def processarHtmlOddsDuplaChance(html: str):
  redutorQuantidadeContraMandante = 0
  redutorQuantidadeContraEmpate = 0
  redutorQuantidadeContraVisitante = 0

  valorOddContraMandante = 0
  valorOddContraEmpate = 0
  valorOddContraVisitante = 0
  listaOdds = []

  try:
    htmlOdds = html_utils.converterStringParaHtml(html)
    htmlListaOdds = htmlOdds.select(CSS_LINHAS_ODDS)
    quantidadeOdds = len(htmlListaOdds)

    for elemento in htmlListaOdds:
      infoCasaAposta = elemento.select_one(CSS_INFO_CASA_APOSTA).attrs["title"]
      opcoes = elemento.select("a[class^=odd_]")

      oddContraVisitante = opcoes[0].text.replace("-", "0")
      oddContraEmpate = opcoes[1].text.replace("-", "0")
      oddContraMandante = opcoes[2].text.replace("-", "0")

      listaOdds.append({"casaAposta": infoCasaAposta,
                        "contraVisitante": float(oddContraMandante),
                        "contraMandante": float(oddContraEmpate),
                        "contraEmpate": float(oddContraVisitante)})

      if oddContraMandante == "0": redutorQuantidadeContraMandante += 1
      if oddContraEmpate == "0": redutorQuantidadeContraEmpate += 1
      if oddContraVisitante == "0": redutorQuantidadeContraVisitante += 1

      valorOddContraMandante += float(oddContraMandante)
      valorOddContraEmpate += float(oddContraEmpate)
      valorOddContraVisitante += float(oddContraVisitante)

    return {
      "contraVisitante": round(valorOddContraVisitante / (quantidadeOdds - redutorQuantidadeContraVisitante),
                               CASAS_DECIMAIS),
      "contraMandante": round(valorOddContraMandante / (quantidadeOdds - redutorQuantidadeContraEmpate),
                              CASAS_DECIMAIS),
      "contraEmpate": round(valorOddContraEmpate / (quantidadeOdds - redutorQuantidadeContraEmpate),
                            CASAS_DECIMAIS),
      "listaOdds": listaOdds
    }

  except Exception as e:
    log.ERRO("Não foi possível processar ODDs dupla chance.", e.args)
    return {}

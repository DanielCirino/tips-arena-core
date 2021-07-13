# -*- coding: utf-8 -*-
from datetime import datetime

import pytz


def converterHoraLocalToUtc(dataHoraLocal: datetime):
  try:
    fusoHorario = pytz.timezone("America/Sao_Paulo")
    return fusoHorario.localize(dataHoraLocal)

  except Exception as e:
    return None


def obterNumeroMes(nomeMes: str):
  codigoMes = "00"
  nomeMes = nomeMes.lower()

  if nomeMes == "janeiro": codigoMes = "01"
  if nomeMes == "fevereiro": codigoMes = "02"
  if nomeMes == "março" or codigoMes == "marco":  codigoMes = "03"
  if nomeMes == "abril": codigoMes = "04"
  if nomeMes == "maio": codigoMes = "05"
  if nomeMes == "junho": codigoMes = "06"
  if nomeMes == "julho": codigoMes = "07"
  if nomeMes == "agosto": codigoMes = "08"
  if nomeMes == "setembro": codigoMes = "09"
  if nomeMes == "outubro": codigoMes = "10"
  if nomeMes == "novembro": codigoMes = "11"
  if nomeMes == "dezembro": codigoMes = "12"

  return codigoMes

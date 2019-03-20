#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from math import factorial, pow, e


class UtilBll:

    def limparString(self, texto: str):
        texto = texto.strip()
        texto = texto.replace("'", "''")
        texto = texto.replace("  ", "")
        texto = bytes(texto, 'utf-8').decode('utf-8', 'ignore')
        return texto

    def getNumeroMes(self, nomeMes: str):
        codigoMes = "00";
        nomeMes = nomeMes.lower();

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

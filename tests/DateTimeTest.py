# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import unittest

from pytz import timezone

from core.ScrapWorkCore import ScrapWorkCore
from utils.DateTimeHandler import DateTimeHandler
from repository.Collection import Collection


class DateTimeTest(unittest.TestCase):

    def teste_conversao_data(self):
        timezoneOffset = datetime.now() - datetime.utcnow()
        timezoneBrasil = timezone("America/Sao_Paulo")
        timezonUtc = timezone("GMT")

        data_inicio = datetime.strftime(datetime.now(), "%Y-%m-%d 00:00:00")
        data_inicio = DateTimeHandler().converterHoraLocalToUtc(datetime.strptime(data_inicio, "%Y-%m-%d %H:%M:%S"))
        data_fim = datetime.utcnow()

        date_utc = datetime.utcnow().isoformat()
        date_now = datetime.now().astimezone(timezone).isoformat()
        str_data = "16.02.2019 11:00"
        data_from_string = datetime.strptime(str_data, "%d.%m.%Y %H:%M")
        data_with_timezone = data_from_string.astimezone(timezone)
        date_iso_format = data_from_string.isoformat()
        date_utc_convert = timezonUtc.localize(data_with_timezone)

        print(data_from_string.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

        self.assertTrue(data_from_string != None)

    def teste_salvar_data_mongodb(self):
        str_data = "29.05.2019 23:30"
        data_from_string = datetime.strptime(str_data, "%d.%m.%Y %H:%M")

        datas = {"dataLocal": data_from_string,
                 "dataUtc": DateTimeHandler().converterHoraLocalToUtc(data_from_string)

                 }
        ret = Collection("testeDataHora").inserirDocumento(datas)

        datasSalvas = Collection("testeDataHora").listarDocumentos()
        for doc in datasSalvas:
            print(doc)



        self.assertTrue(datasSalvas != None)


if __name__ == "__main__":
    unittest.main()

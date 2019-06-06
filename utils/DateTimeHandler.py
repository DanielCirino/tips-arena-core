
# -*- coding: utf-8 -*-

import time
import pytz
from datetime import datetime,timedelta


class DateTimeHandler:

    def converterHoraLocalToUtc(self,dataHoraLocal:datetime):
        try:
            fusoHorario = pytz.timezone("America/Sao_Paulo")
            dataComFusoHorario = fusoHorario.localize(dataHoraLocal)

            return dataComFusoHorario
        except Exception as e:
            return None


    def calcularTimezoneOffSet(self, t=None):
        offset = 0

        if t is None:
            t = time.time()

        if time.localtime(t).tm_isdst and time.daylight:
            offset = time.altzone
        else:
            offset = time.timezone

        return int(offset / 60 / 60)


    def converterHoraLocalToUtc(self,dataHoraLocal:datetime):
        try:
            fusoHorario = pytz.timezone("UTC")
            dataHoraUtc = dataHoraLocal + timedelta(hours=self.calcularTimezoneOffSet())

            return  fusoHorario.localize(dataHoraUtc)
        except Exception as e:
            return None
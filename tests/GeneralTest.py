from datetime import datetime
import unittest

import pytz

from core.ScrapWorkCore import ScrapWorkCore
class GeneralTest(unittest.TestCase):

    def teste_conversao_data(self):
        timezone = pytz.timezone("America/Sao_Paulo")
        date_utc = datetime.utcnow().isoformat()
        date_now  = datetime.now().astimezone(timezone).isoformat()
        str_data = "16.02.2019 11:00"
        data_from_string = datetime.strptime(str_data, "%d.%m.%Y %H:%M")
        data_with_timezone = data_from_string.astimezone(timezone).isoformat()
        date_iso_format = data_from_string.isoformat()

        print(data_from_string.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

        self.assertTrue(data_from_string != None)


if __name__ == "__main__":
    unittest.main()


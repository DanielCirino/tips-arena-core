
# -*- coding: utf-8 -*-

import time


class DateTimeHandler:

    def local_time_offset(self, t=None):
        offset = 0

        if t is None:
            t = time.time()

        if time.localtime(t).tm_isdst and time.daylight:
            offset = time.altzone
        else:
            offset = time.timezone

        return int(offset / 60 / 60)

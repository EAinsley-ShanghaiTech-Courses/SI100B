# ============================================================================ #
#                               Python Project                                 #
#        SI 100B: Introduction to Information Science and Technology           #
#                        Fall 2020, ShanghaiTech University                    #
#                      Author: Diao Zihao <hi@ericdiao.com>                    #
#                          Last motified: 07/07/2020                           #
# ============================================================================ #

from typing import Tuple
import re
import time
import requests as rq
# from typing import List, Dict, Any


class FlightAwareCrawler:
    def __init__(self,
                 loc: Tuple[float, float] = (0.0, 0.0),
                 rng: [float, float] = (0.0, 0.0)):
        self.latitude_center, self.longitude_center = loc
        self.latitude_nw, self.longitude_nw = rng
        self.latitude_se, self.longitude_se = (x * 2 - y
                                               for x, y in zip(loc, rng))

    def get_data_once(self):
        # !无法跨越180经线求和，如果跨越180度经线，需要分成两部分求解
        # !在输入数据完全合法的情况下，只需考虑两种情况：右下角经度大于180，
        # !右下角纬度小于-90
        tokenregx = '\"VICINITY_TOKEN\":\"([A-Za-z0-9]*)\"'
        kDataURL = "https://flightaware.com/ajax/vicinity_aircraft.rvt"
        kHtmlURL = "https://flightaware.com/live/"
        token = re.search(tokenregx, kHtmlURL.text)
        print(token.group(1))

        testparam = {
            "minLon": 10,
            "minLat": -8.59954833984375,
            "maxLon": -10,
            "maxLat": 27.0703125,
            "token": token.group(1)
        }

        testquery = rq.get(kDataURL, params=testparam)

        print(testquery)
        t = testquery.json()
        print(len(t['features']))
        t['features'][0]

    def spin(self, interval=1):
        self.get_data_once()
        time.sleep(interval)


a = FlightAwareCrawler((1.1, 1.1), (0.0, 0.0))

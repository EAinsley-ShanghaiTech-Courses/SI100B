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
        print(self.latitude_se, self.longitude_se)

    def get_data_once(self):
        # !无法跨越180经线求和，如果跨越180度经线，需要分成两部分求解
        # !在输入数据完全合法的情况下，只需考虑两种特殊情况：右下角经度大于180，
        # !右下角纬度小于-90（这个无法处理）
        tokenregx = '\"VICINITY_TOKEN\":\"([A-Za-z0-9]*)\"'
        kDataURL = "https://flightaware.com/ajax/vicinity_aircraft.rvt"
        kHtmlURL = "https://flightaware.com/live/"
        html = rq.get(kHtmlURL)
        token = re.search(tokenregx, html.text)
        print(token.group(1))

        params = {
            "minLon": self.longitude_nw,
            "minLat": max(-90, self.latitude_se),
            "maxLon": min(180, self.longitude_se),
            "maxLat": self.latitude_nw,
            "token": token.group(1)
        }
        query_data_raw = rq.get(kDataURL, params=params).json()
        print(query_data_raw.keys())
        query_data = query_data_raw["features"]

        # 经线跨国180度
        if self.longitude_se > 180:
            params["minLat"] = -180
            params["maxLat"] = self.longitude_se - 360
            query_data_raw = rq.get(kDataURL, params=params).json()
            query_data.extend(query_data_raw["features"])

        # TODO：筛选数据

        print(query_data)

    def spin(self, interval=1):
        start_time = time.time()
        self.get_data_once()
        time.sleep(interval - time.time() + start_time)


a = FlightAwareCrawler((31.17940, 121.59043), (51.0, 100.0))
# 31.17940N, 121.59043E

a.get_data_once()

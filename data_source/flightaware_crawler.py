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
import json
import os
import platform

# from typing import List, Dict, Any
if platform.system() == 'Windows':
    kDefaultPath = r"d:\pyton-crawler\data.json"
else:
    kDefaultPath = "/tmp/wif_crawler/data.json"


class FlightAwareCrawler:
    def __init__(self,
                 loc: Tuple[float, float] = (0.0, 0.0),
                 rng: [float, float] = (0.0, 0.0)):
        self.latitude_center, self.longitude_center = loc
        self.latitude_nw, self.longitude_nw = rng
        self.latitude_se, self.longitude_se = (x * 2 - y
                                               for x, y in zip(loc, rng))
        self.baddata = 0
        self.saved_data = {}

    def get_data_once(self):
        def ExtractData(x):
            data_dict = {}
            # 如果没有关键的飞机信息，就丢弃数据
            try:
                data_dict['longitude'], data_dict['latitude'] = x['geometry'][
                    'coordinates']
                data_dict['departure_IATA'] = x['properties']['origin']['iata']
                data_dict['arrival_IATA'] = x['properties']['destination'][
                    'iata']
            except KeyError:
                self.baddata += 1
                return None

            kMapping = {
                'direction': 'heading',
                'altitude': 'altitude',
                'groundspeed': 'groundspeed',
                'ident': 'filghtnumber'
            }
            # 如果是不重要的数据丢失，就把数据设成None
            for v, k in kMapping.items():
                try:
                    data_dict[k] = x['properties'][v]
                except KeyError:
                    data_dict[k] = None
            return data_dict

        # !无法跨越180经线和南北极点求和，如果跨越180度经线，需要分成两部分求解
        # !在输入数据完全合法的情况下，只需考虑两种特殊情况：右下角经度大于180，
        # !右下角纬度小于-90（这个无法处理）
        tokenregx = '\"VICINITY_TOKEN\":\"([A-Za-z0-9]*)\"'
        kDataURL = "https://flightaware.com/ajax/vicinity_aircraft.rvt"
        kHtmlURL = "https://flightaware.com/live/"
        html = rq.get(kHtmlURL, timeout=5)
        token = re.search(tokenregx, html.text)

        params = {
            "minLon": self.longitude_nw,
            "minLat": max(-90, self.latitude_se),
            "maxLon": min(180, self.longitude_se),
            "maxLat": self.latitude_nw,
            "token": token.group(1)
        }
        query_data_raw = rq.get(kDataURL, params=params, timeout=5).json()
        query_data = query_data_raw['features']

        # 经线跨国180度
        if self.longitude_se > 180:
            params["minLat"] = -180
            params["maxLat"] = self.longitude_se - 360
            query_data_raw = rq.get(kDataURL, params=params, timeout=5).json()
            query_data.extend(query_data_raw['features'])
        extract_data = {}

        for i in query_data:
            key = i['properties']['flight_id']
            if key in extract_data:
                continue
            extract_datum = ExtractData(i)
            if extract_datum is None:
                continue
            extract_data[key] = extract_datum

        return extract_data

    def display_data(self, num):
        os.system("clear")
        for i, (k, v) in enumerate(self.saved_data.items()):
            if i == num:
                return
            print(i + 1, ":")
            for field_name, field_value in v.items():
                print("  ", field_name, ":", field_value)

    def spin(self,
             interval=1,
             max_loop=100,
             filename=kDefaultPath,
             save=True,
             display=False,
             display_num=5):
        loop_count = 0
        retry_time = 0
        while max_loop is None or loop_count < max_loop:
            start_time = time.time()
            try:
                self.saved_data = self.get_data_once()
            except rq.exceptions.Timeout:
                if retry_time > 2:
                    exit("Connection Failed")
                print("timeout...retrying")
                retry_time += 1
            except rq.exceptions.ConnectionError:
                if retry_time > 2:
                    exit("Connection Failed")
                print("unable to connect...retrying")
                retry_time += 1
            else:
                retry_time = 0
                if max_loop:
                    loop_count += 1
                if save:
                    with open(filename, "w") as f:
                        json.dump(self.saved_data, f, indent=2)
                if display:
                    self.display_data(display_num)
                print("bad data:", self.baddata)
                print("airplane numbers:", len(self.saved_data))
                self.baddata = 0
                time.sleep(max(interval - time.time() + start_time, 0))

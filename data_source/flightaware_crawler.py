"""A Web Crawler of flight Aware

Dpendencies:
    requests

"""

from typing import Tuple, Dict, Union
import re
import time
import requests as rq
import json
import os
import platform

if platform.system() == 'Windows':
    kDefaultPath = r"d:\python-crawler\data.json"
else:
    kDefaultPath = "/tmp/data.json"


class FlightAwareCrawler:
    """The web crawler of Flight Aware.

    Give a center point and the north-west corner of the square. Give the
    information of the flight in this square based on the data crawled from
    <flightaware.com>.

    Example:
        >>> from data_source import flightaware_crawler as crl
        >>> crawler = crl.FlightAwareCrawler((31, 121), (20, 111))
        >>> crawler.spin(interval=1, max_loop=3, save=False, display=False)
        ------
        bad data: 0
        airplane numbers: 966
        bad data: 0
        airplane numbers: 965
        bad data: 0
        airplane numbers: 966
        ------
        Note: The output may look different from the example.
    Args:
        loc(Tuple[float, float]): The location of the centerpoint. The first
            float is latitude, the second is longitude.
        rng(Tuple[float, float]): The loaction of the north-west point of the
            square. The first float is latitude, the second is longitude.
    """
    def __init__(self,
                 loc: Tuple[float, float] = (0.0, 0.0),
                 rng: Tuple[float, float] = (0.0, 0.0)):
        self.__latitude_center, self.__longitude_center = loc
        self.__latitude_nw, self.__longitude_nw = rng
        self.__latitude_se, self.__longitude_se = (x * 2 - y
                                                   for x, y in zip(loc, rng))
        self.baddata = 0
        self.__token = None
        self.__update_token()
        self.__saved_data = {}
        self.__plane_num = None

    @property
    def location(self):
        return [self.__latitude_center, self.__longitude_center]

    @property
    def plane_number(self):
        return self.__plane_num

    @location.setter
    def location(self, loc: Tuple[float, float]):
        move_lat = loc[0] - self.__latitude_center
        move_lon = loc[1] - self.__longitude_center
        self.__latitude_center, self.__longitude_center = loc
        self.__latitude_nw += move_lat
        self.__latitude_se += move_lat
        self.__longitude_nw += move_lon
        self.__longitude_se += move_lon

    def __update_token(self):
        tokenregx = '\"VICINITY_TOKEN\":\"([A-Za-z0-9]*)\"'
        kHtmlURL = "https://flightaware.com/live/"
        html = rq.get(kHtmlURL, timeout=5)
        token = re.search(tokenregx, html.text)
        self.__token = token.group(1)

    def __data_extract(self, x: Dict) -> Dict:
        # Extact needed data.
        data_dict = {}
        # Dismiss the datum, if it doesn't contain the essential information of
        # the airplane
        try:
            data_dict['longitude'], data_dict['latitude'] = x['geometry'][
                'coordinates']
            data_dict['departure_IATA'] = x['properties']['origin']['iata']
            data_dict['arrival_IATA'] = x['properties']['destination']['iata']
        except KeyError:
            self.baddata += 1
            return None

        kMapping = {
            'direction': 'heading',
            'altitude': 'altitude',
            'groundspeed': 'groundspeed',
            'ident': 'flightnumber'
        }
        # Set the value to None, if the trivial information is lost
        for v, k in kMapping.items():
            try:
                data_dict[k] = x['properties'][v]
            except KeyError:
                data_dict[k] = None
        return data_dict

    def __get_response(self, url, params={}) -> Dict:
        response = rq.get(url, params=params, timeout=5)
        if response.status_code == 500:
            self.__update_token()
            params['token'] = self.__token
            return self.__get_response(url, params)
        return response.json()

    def get_data_once(self) -> Dict:
        """Crawl the data from the website once.

        Returns:
            A dictionary contains all needed data of the airline.
        """
        kDataURL = "https://flightaware.com/ajax/vicinity_aircraft.rvt"

        params = {
            "minLon": self.__longitude_nw,
            "minLat": max(-90, self.__latitude_se),
            "maxLon": min(180, self.__longitude_se),
            "maxLat": self.__latitude_nw,
            "token": self.__token
        }
        response = self.__get_response(kDataURL, params)
        query_data = response['features']

        # Cross the 180 longitude
        if self.__longitude_se > 180:
            params["minLat"] = -180
            params["maxLat"] = self.__longitude_se - 360
            response = self.__get_response(kDataURL, params)
            query_data.extend(response['features'])

        extract_data = {}
        for i in query_data:
            key = i['properties']['flight_id']
            if key in extract_data:
                continue
            extract_datum = self.__data_extract(i)
            if extract_datum is None:
                continue
            extract_data[key] = extract_datum

        self.__plane_num = len(extract_data)

        return extract_data

    # TODO: Need improvement, remove self.__daved_data
    def __display_data(self, num):
        # Display <nums> pieces of the data
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        for i, (k, v) in enumerate(self.__saved_data.items()):
            if i == num:
                return
            print(i + 1, ":")
            for field_name, field_value in v.items():
                print("  ", field_name, ":", field_value)

    def spin(self,
             interval: float = 1.0,
             max_loop: Union[int, None] = 100,
             filename: str = kDefaultPath,
             save: bool = True,
             display: bool = False,
             display_num: int = 5):
        """Contiuely crawl the data.

        Carwl the data according to arguments.
        Args:
            interval(float): The interval between each data obtainment.
            max_loop(int): The max number of the times of the looping. If it's
                set to None, then the program won't stop until being halted by
                the user.
            filename(str): The file to save the data.
            save(bool): Save the data if it's True.
            display(bool): Display the data on the screen if it's True.
            display_num(int): The number of the data to display.
        """
        loop_count = 0
        retry_time = 0
        while max_loop is None or loop_count < max_loop:
            start_time = time.time()
            # Handle connections
            try:
                self.__saved_data = self.get_data_once()
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
                        json.dump(self.__saved_data, f, indent=2)
                if display:
                    self.__display_data(display_num)
                print("bad data:", self.baddata)
                print("airplane numbers:", self.__plane_num)
                print("Now time:", time.asctime(time.localtime()))
                self.baddata = 0
                time.sleep(max(interval - time.time() + start_time, 0))

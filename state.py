#!/usr/bin/env python3
from data_source.flightaware_crawler import FlightAwareCrawler
from light_controller.controller import BaseController
import time
import json


class State:
    def __init__(self, filename='/tmp/data.json'):
        self.__file = filename
        self.__controller = BaseController()

    def spin(self, interval=2, max_loop=None):
        start_time = time.time()
        loop_count = 0
        while max_loop is None or loop_count < max_loop:
            print("Loading data...")
            with open(self.__file) as f:
                data = json.load(f)
            num = len(data)
            self.__controller.work_once(num)
            time.sleep(max(interval - time.time() + start_time, 0))
            loop_count += 1


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        kLatitude = float(sys.argv[1])
        kLongitude = float(sys.argv[2])
    else:
        kLatitude = 31.17940
        kLongitude = 121.59043
    crl = FlightAwareCrawler((kLatitude, kLongitude),
                             (kLatitude + 0.35, kLongitude - 0.35))
    state = State()
    for i in range(5):
        crl.spin(max_loop=1)
        state.spin(max_loop=1)

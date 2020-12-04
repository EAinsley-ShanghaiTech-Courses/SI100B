# ============================================================================ #
#                               Python Project                                 #
#        SI 100B: Introduction to Information Science and Technology           #
#                        Fall 2020, ShanghaiTech University                    #
#                      Author: Diao Zihao <hi@ericdiao.com>                    #
#                          Last motified: 07/07/2020                           #
# ============================================================================ #
# from typing import Tuple
# from data_source.fr24_crawler import Fr24Crawler
# from light_controller.controller import *


class State:
    def __init__(self):
        raise NotImplementedError

    def spin(self):
        raise NotImplementedError

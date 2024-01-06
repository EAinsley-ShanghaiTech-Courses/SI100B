# ============================================================================ #
#                               Python Project                                 #
#        SI 100B: Introduction to Information Science and Technology           #
#                        Fall 2020, ShanghaiTech University                    #
#                      Author: Diao Zihao <hi@ericdiao.com>                    #
#                          Last motified: 07/07/2020                           #
# ============================================================================ #

from typing import Tuple
# from typing import List, Dict, Any


class Fr24Crawler:
    def __init__(self, loc: Tuple[float, float], rng: float):
        raise NotImplementedError

    def get_data_once(self):
        raise NotImplementedError

    def spin(self, interval=1):
        raise NotImplementedError

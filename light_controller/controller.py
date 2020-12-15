# ============================================================================ #
#                               Python Project                                 #
#        SI 100B: Introduction to Information Science and Technology           #
#                        Fall 2020, ShanghaiTech University                    #
#                      Author: Diao Zihao <hi@ericdiao.com>                    #
#                          Last motified: 07/07/2020                           #
# ============================================================================ #
from gpiozero import PWMLED


class BaseController:
    def __init__(self):
        self.digit[4] = [
            PWMLED(i, initial_value=0, frequency=120) for i in range(14, 18)
        ]

    def work_once(self, num):
        print("NUM:", num)
        num = max(num, 16)
        for i in range(4):
            self.digit[i].value = num % 2
            num //= 2

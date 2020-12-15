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
        kStich = [26, 19,12, 5]
        self.digit = [
            PWMLED(i, initial_value=0, frequency=120) for i in kStich
        ]

    def work_once(self, num):
        print("NUM:", num)
        num = min(num, 15)
        for i in range(4):
            print(num)
            self.digit[i].value = num % 2
            print(i, ":", self.digit[i].value)
            num //= 2

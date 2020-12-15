# ============================================================================ #
#                               Python Project                                 #
#        SI 100B: Introduction to Information Science and Technology           #
#                        Fall 2020, ShanghaiTech University                    #
#                      Author: Diao Zihao <hi@ericdiao.com>                    #
#                          Last motified: 07/07/2020                           #
# ============================================================================ #
from gpiozero import PWMLED
from time import sleep


class BaseController:
    def __init__(self):
        kStich = [26, 19, 12, 5]
        self.__digit = [
            PWMLED(i, initial_value=0, frequency=120) for i in kStich
        ]

    def work_once(self, num):
        print("NUM:", num)
        num = min(num, 15)
        if num == 0:
            for i in range(3):
                self.__digit[0].value = self.__digit[1].value = 1
                sleep(0.2)
                self.__digit[0].value = self.__digit[1].value = 0
                sleep(0.2)
        elif num > 15:
            for i in range(3):
                self.__digit[2].value = self.__digit[3].value = 1
                sleep(0.2)
                self.__digit[2].value = self.__digit[3].value = 0
                sleep(0.2)
        else:
            for i in range(4):
                print(num)
                self.__digit[i].value = num % 2
                print(i, ":", self.__digit[i].value)
                num //= 2

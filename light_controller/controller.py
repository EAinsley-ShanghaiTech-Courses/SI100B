# ============================================================================ #
#                               Python Project                                 #
#        SI 100B: Introduction to Information Science and Technology           #
#                        Fall 2020, ShanghaiTech University                    #
#                      Author: Diao Zihao <hi@ericdiao.com>                    #
#                          Last motified: 07/07/2020                           #
# ============================================================================ #


class BaseController:
    def __init__(self):
        raise NotImplementedError

    def work_once(self):
        raise NotImplementedError

    def on(self):
        raise NotImplementedError

    def off(self):
        raise NotImplementedError

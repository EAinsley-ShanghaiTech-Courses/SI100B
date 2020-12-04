# ============================================================================ #
#                               Python Project                                 #
#        SI 100B: Introduction to Information Science and Technology           #
#                        Fall 2020, ShanghaiTech University                    #
#                      Author: Diao Zihao <hi@ericdiao.com>                    #
#                          Last motified: 07/07/2020                           #
# ============================================================================ #
from flask import Flask
# form flask import request, render_template

web_server = Flask(__name__)
web_server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@web_server.route('/')
def home():
    raise NotImplementedError


@web_server.route('/config', methods=['GET', 'POST'])
def config():
    raise NotImplementedError


@web_server.route('/vis', methods=['GET'])
def vis():
    raise NotImplementedError


if __name__ == "__main__":
    web_server.run(host="127.0.0.1", port=5000)

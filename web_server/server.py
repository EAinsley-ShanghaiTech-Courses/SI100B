# ============================================================================ #
#                               Python Project                                 #
#        SI 100B: Introduction to Information Science and Technology           #
#                        Fall 2020, ShanghaiTech University                    #
#                      Author: Diao Zihao <hi@ericdiao.com>                    #
#                          Last motified: 07/07/2020                           #
# ============================================================================ #
from flask import Flask
from flask import render_template
from flask import request
web_server = Flask(__name__)
web_server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@web_server.route('/')
def home():
    return render_template("home.html")


@web_server.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        return vis()
    return render_template("config.html")


@web_server.route('/vis', methods=['GET'])
def vis():
    return render_template("vis.html")


if __name__ == "__main__":
    web_server.run(host="127.0.0.1", port=5000)

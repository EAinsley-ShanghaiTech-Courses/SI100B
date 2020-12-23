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
import json

web_server = Flask(__name__)
web_server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def dump_config(data):
    kKeys = {
        'center_lat': 31.1790,
        'center_lon': 121.59043,
        'corner_lat': 32.67940,
        'corner_lon': 120.09043,
        'interval': 10
    }
    config = {}
    for k, v in data.items():
        if not v:
            config[k] = kKeys[k]
        elif k + '_sign' in data:
            if data[k + '_sign'] == 'W' or 'S':
                config[k] = -int(v)
        else:
            config[k] = v
    with open('/tmp/config.json', 'w') as f:
        json.dump(config, f)


@web_server.route('/')
def home():
    return render_template("home.html")


@web_server.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        dump_config(request.form)
        return vis()
    return render_template("config.html")


@web_server.route('/vis', methods=['GET'])
def vis():
    with open('/tmp/config.json') as f:
        info = json.load(f)
    return render_template("vis.html", info=info)


if __name__ == "__main__":
    web_server.run(host="127.0.0.1", port=5000)

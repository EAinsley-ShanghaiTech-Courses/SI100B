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
# from ..light_controller import controller
web_server = Flask(__name__)
web_server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# state = controller.State()


def dump_config(data):
    kEmpt = {
        'center_lat': 31.1790,
        'center_lon': 121.59043,
        'corner_lat': 32.67940,
        'corner_lon': 120.09043,
        'interval': 10,
        'value': 100
    }
    config = {}
    for k, v in kEmpt.items():
        if not data[k]:
            config[k] = v
        else:
            config[k] = int(data[k])
    for k, v in data.items():
        if not v:
            config[k] = kEmpt[k]
        else:
            if k in ['center_lon', 'corner_lon']:
                config[k] = min(max(int(v), 0), 180)
                if data[k + '_sign'] == 'W':
                    config[k] = -config[k]
            elif k in ['center_lat', 'corner_lat']:
                config[k] = min(max(int(v), 0), 90)
                if data[k + '_sign'] == 'S':
                    config[k] = -config[k]
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

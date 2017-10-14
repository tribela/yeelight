import os
import time

import webcolors

from flask import Flask, jsonify, render_template, request
from flask_bower import Bower
from flask_sse import sse

from yeelight import Yeelight

app = Flask(__name__)
Bower(app)
app.config['REDIS_URL'] = os.getenv('REDIS_URL')
app.register_blueprint(sse, url_prefix='/stream')

YEELIGHT_ADDRESS = os.environ['YEELIGHT_ADDRESS']

@app.before_first_request
def connect_yeelight():
    global yeelight
    yeelight = Yeelight(YEELIGHT_ADDRESS)


def get_status():
    return {
        'switch': yeelight.switch,
        'mode': yeelight.mode,
        'brightness': yeelight.brightness,
        'rgb': yeelight.rgb,
        'temp': yeelight.temp,
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/status')
def status():
    return jsonify(get_status())



@app.route('/switch', methods=['GET', 'POST', 'PUT', 'DELETE'])
def switch():
    if request.method == 'GET':
        return '1' if yeelight.switch == 1 else '0'

    if request.method == 'POST':
        data = request.json or request.form
        switch = data.get('switch')
    elif request.method in ('PUT', 'DELETE'):
        if request.method == 'PUT':
            switch = 'on'
        else:
            switch = 'off'

    command = {
        'on': yeelight.poweron,
        'off': yeelight.poweroff,
        '1': yeelight.poweron,
        '0': yeelight.poweroff,
    }
    if switch in command:
        command[switch]()
        print('Turn {} the light'.format(switch))
        sse.publish(get_status(), type='update')
        return 'OK'

    return 'Fail'


@app.route('/light', methods=['POST'])
def light():
    data = request.json or request.form

    brightness = data.get('brightness')
    rgb = data.get('rgb')
    color = data.get('color')
    temp = data.get('temp')

    if brightness:
        print('Set brightness: {}'.format(brightness))
        yeelight.set_brightness(int(brightness))

    if rgb:
        print('Set rgb: {}'.format(rgb))
        yeelight.set_rgb(rgb)
    elif color:
        color = color.replace(' ', '')
        print('Set color {}'.format(color))
        try:
            rgb = webcolors.name_to_hex(color)[1:]
        except ValueError as e:
            return str(e)
        else:
            yeelight.set_rgb(rgb)
    elif temp:
        temp = int(temp)
        print('Set temp: {}'.format(temp))
        yeelight.set_temp(temp)

    sse.publish(get_status(), type='update')

    return 'OK' if any((brightness, rgb, temp)) else 'FAIL'


@app.route('/sleep', methods=['POST'])
def sleep():
    data = request.json or request.form
    minutes = int(data.get('minutes'))
    yeelight.set_sleep(minutes)
    print('Set sleep: {}'.format(minutes))
    sse.publish(get_status(), type='update')
    return 'OK'

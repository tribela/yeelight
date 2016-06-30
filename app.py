import time

from flask import Flask, render_template, request

from yeelight import Yeelight

app = Flask(__name__, template_folder='.')
YEELIGHT_ADDRESS = os.environ('YEELIGHT_ADDRESS')
yeelight = Yeelight(YEELIGHT_ADDRESS)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/switch', methods=['POST'])
def switch():
    switch = request.form.get('switch')
    command = {
        'on': yeelight.poweron,
        'off': yeelight.poweroff,
    }
    if switch in command:
        command[switch]()
        return 'OK'

    return 'Fail'


@app.route('/light', methods=['POST'])
def light():
    brightness = request.form.get('brightness')
    rgb = request.form.get('rgb')
    warm = request.form.get('warm')


    if brightness:
        print('Set brightness: {}'.format(brightness))
        yeelight.setbrightness(int(brightness))

    if rgb:
        print('Set rgb: {}'.format(rgb))
        yeelight.setrgb(rgb)
    elif warm:
        print('Set warm: {}'.format(warm))
        yeelight.setwarm(float(warm))


    return 'OK' if any((brightness, rgb, warm)) else 'FAIL'

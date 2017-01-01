# Yeelight control panel

Control [Yeelight Bedside Lamp](http://xiaomi-mi.com/mi-lighting/xiaomi-yeelight-bedside-lamp/) using bluetooth LE.

I reverse engineered some protocol of it.

## TODO

- Read name of devices.
- Wakeup light.
- Scene mode.


## Install and run

```sh
$ sudo apt install python-dev libglib2.0-dev  # Install library for bluepy
$ pip install -r requirements.txt honcho
$ npm install -g bower
$ bower install

# Setting envs.
$ echo 'YEELIGHT_ADDRESS=c0:ff:ee:c0:ff:ee' > .env
$ echo 'REDIS_URL=redis://localhost/1' >> .env

$ honcho start
```

Or you can use it as library. Just import `yeelight.py`.

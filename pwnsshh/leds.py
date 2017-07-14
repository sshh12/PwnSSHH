
import time
import os

class LED(object):

    def __init__(self, name):

        self.name = name

    @property
    def on(self):
        return int(os.popen('cat /sys/devices/platform/leds-gpio/leds/tp-link:green:{}/brightness'.format(self.name)).read()) > 0

    @on.setter
    def on(self, value):

        if value:
            brightness = 255
        else:
            brightness = 0

        os.system('echo {} > /sys/devices/platform/leds-gpio/leds/tp-link:green:{}/brightness'.format(brightness, self.name))

        return value

    def toggle(self):

        self.on = not self.on

def all_on():

    for led in leds: led.on = True

def all_off():

    for led in leds: led.on = False

def cycle(delay=0.3):

    all_off()

    for led in leds:

        led.on = True

        time.sleep(delay)

        led.on = False

LED_3G = LED('3g')
LED_WLAN = LED('wlan')
LED_LAN = LED('lan')

leds = [LED_3G, LED_WLAN, LED_LAN]

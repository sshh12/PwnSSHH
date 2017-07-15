
import time
import os

class LED(object):
    """LED object for interfacing with the 3 leds."""
    def __init__(self, name):

        self.name = name

    @property
    def on(self):
        """Reads the state of the led as bool."""
        return int(os.popen('cat /sys/devices/platform/leds-gpio/leds/tp-link:green:{}/brightness'.format(self.name)).read()) > 0

    @on.setter
    def on(self, value):
        """Sets led to on or off."""
        if value:
            brightness = 255
        else:
            brightness = 0

        os.system('echo {} > /sys/devices/platform/leds-gpio/leds/tp-link:green:{}/brightness'.format(brightness, self.name))

        return value

    def toggle(self):
        """Toggles the state of an led."""
        self.on = not self.on

def all_on():
    """Turn all 3 leds on."""
    for led in leds: led.on = True

def all_off():
    """Turn all 3 leds off."""
    for led in leds: led.on = False

def cycle(delay=0.5):
    """
    Cycles through leds.

    Parameters
    ----------
    delay : int
        The time in seconds between lighting each led
    """
    all_off()

    for led in leds:

        led.on = True

        time.sleep(delay)

        led.on = False

LED_3G = LED('3g')
LED_WLAN = LED('wlan')
LED_LAN = LED('lan')

leds = [LED_3G, LED_WLAN, LED_LAN] # Available Leds

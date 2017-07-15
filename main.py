
from pwnsshh.leds import *
from pwnsshh.configs import *
from pwnsshh.switch import *

import json

def main():

    cycle()
    cycle()

    settings = json.load(open('/root/PwnSSHH/settings.json', 'r'))

    switch = get_switch_id()

    if switch == 0:

        CFG_CLIENT_AP.set_SSID(settings['modes']['client-ap']['ssid'])
        CFG_CLIENT_AP.set_passwd(settings['modes']['client-ap']['passwd'])
        CFG_CLIENT_AP.run()

    elif switch == 1:

        CFG_AP.set_SSID(settings['modes']['ap']['ssid'])
        CFG_AP.set_passwd(settings['modes']['ap']['passwd'])
        CFG_AP.run()


if __name__ == '__main__':
    main()

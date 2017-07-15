
import os

switches = ['3G', 'WISP', 'AP'] # Switch Names

def _get_state(device):

    return "hi" in os.popen("grep -i {} /sys/kernel/debug/gpio".format(device)).read()

def get_switch_id():
    """Returns the current index of the switch on the side of the router. {0, 1, 2}"""
    sw1 = _get_state('sw1')
    sw2 = _get_state('sw2')

    if not sw1 and sw2:
        return 0

    elif sw1 and not sw2:
        return 1

    elif sw1 and sw2:
        return 2

def get_switch_name():
    """Returns the name of the current switch position."""
    return switches[get_switch_id()]

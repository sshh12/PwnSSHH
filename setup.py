
import sys
import os

print('Setting up PwnSSHH...')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if not os.path.isfile('/root/PwnSSHH/main.py'):

    print('(Error) Program in wrong directory.')
    sys.exit(1)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

print('Setting banner...')

banner = """

  _____  _  _  _ __   _ _______ _______ _     _ _     _
 |_____] |  |  | | \  | |______ |______ |_____| |_____|
 |       |__|__| |  \_| ______| ______| |     | |     |

 ------------------------------------------------------
 PwnSSHH (SSHH.IO)
 ------------------------------------------------------


"""

with open('/etc/banner', 'w') as banner_file:

    banner_file.write(banner)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

print('Adding startup script...')

startup = """
#!/bin/sh /etc/rc.common
# PwnSSHH Startup

START=60
STOP=60

start() {
        echo Started!
        (python /root/PwnSSHH/main.py)&
}

stop() {
        echo Stopped!
}
"""

with open('/etc/init.d/pwnsshh', 'w') as init_file:

    init_file.write(startup)

os.system('/etc/init.d/pwnsshh enable')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if 'y' in raw_input('Setup client ap networking? (y/n) > ').lower():

    from pwnsshh.configs import CFG_CLIENT_AP

    CFG_CLIENT_AP.set_SSID(raw_input('Your wifi name > '))
    CFG_CLIENT_AP.set_passwd(raw_input('Your wifi password > '))

    CFG_CLIENT_AP.run()

    print('Configured!')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

print('Checking internet...')

ping_resp = os.system("ping -c 1 -w2 8.8.8.8 > /dev/null 2>&1")

if ping_resp != 0:

    print('(Error) Unable to connect to internet.')
    sys.exit(1)

print('Connected!')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if 'y' in raw_input('Download packages? (y/n) > ').lower():

    os.system('opkg update')
    os.system('opkg install python-pip')


import json
import sys
import os

print('Setting up PwnSSHH...')

def confirm(prompt):
    return 'y' in raw_input("[?]" + prompt + " (y/n) > ").lower()

def error(msg):
    print("[!] (Error) " + msg)
    sys.exit(1)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if not os.path.isfile("/root/PwnSSHH/main.py"):

    error("Program in wrong directory.")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

settings_template = """
{
  "modes":{
    "client-ap":{
      "ssid":"WIFI-SSID",
      "passwd":"WIFI-PASS"
    },
    "ap":{
      "ssid":"WIFI-SSID",
      "passwd":"WIFI-PASS"
    }
  }
}
"""

if confirm("Create/Override settings.json")

    with open("/root/root/PwnSSHH/settings.json", 'w') as settings_file:
        settings_file.write(settings_template)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

print("Setting banner...")

banner = """

  _____  _  _  _ __   _ _______ _______ _     _ _     _
 |_____] |  |  | | \  | |______ |______ |_____| |_____|
 |       |__|__| |  \_| ______| ______| |     | |     |

 ------------------------------------------------------
 PwnSSHH (SSHH.IO)
 ------------------------------------------------------


"""

with open("/etc/banner", 'w') as banner_file:

    banner_file.write(banner)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

print("[#] Adding startup script...")

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

with open("/etc/init.d/pwnsshh", 'w') as init_file:

    init_file.write(startup)

os.system("/etc/init.d/pwnsshh enable")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if confirm("Setup client ap networking"):

    from pwnsshh.configs import CFG_CLIENT_AP

    ssid = raw_input("Your wifi name > ")
    passwd = raw_input("Your wifi password > ")

    CFG_CLIENT_AP.set_SSID(ssid)
    CFG_CLIENT_AP.set_passwd(passwd)

    settings = json.load(open("/root/PwnSSHH/settings.json", 'r'))

    settings['modes']['client-ap']['ssid'] = ssid
    settings['modes']['client-ap']['passwd'] = passwd

    json.dump(settings, open("/root/PwnSSHH/settings.json", 'w'))

    CFG_CLIENT_AP.run()

    print("[+] Configured!")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

print('[#] Checking internet...')

ping_resp = os.system("ping -c 1 -w2 8.8.8.8 > /dev/null 2>&1")

if ping_resp != 0:

    error('Unable to connect to internet.')

print('[+] Connected!')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if confirm('Download packages'):

    os.system('opkg update')
    os.system('opkg install python-pip')

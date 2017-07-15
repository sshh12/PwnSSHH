
from pwnsshh.configs import *

import os

class Config(object):
    """System Configuration Files object."""
    def __init__(self, name):

        self.name = name
        self.network = ""
        self.wireless = ""
        self.firewall = ""
        self.dhcp = ""

    def _replace_all(self, target, new_text):

        self.network = self.network.replace(target, new_text)
        self.wireless = self.wireless.replace(target, new_text)
        self.firewall = self.firewall.replace(target, new_text)
        self.dhcp = self.dhcp.replace(target, new_text)

    def load(self, cfg, fn):
        """
        Loads a config file.

        Takes a file from the config/ dir and loads it into the object as a str.

        Parameters
        ----------
        cfg : str
            The type of config file {network, wireless, firewall, dhcp}
        fn : str
            The filename of the config file

        Note
        ----
        All filenames are relative to the config/ dir in /root/PwnSSHH/
        """
        with open('/root/PwnSSHH/configs/' + fn, 'r') as config_file:

            if cfg == 'network':
                self.network = config_file.read()

            elif cfg == 'wireless':
                self.wireless = config_file.read()

            elif cfg == 'firewall':
                self.firewall = config_file.read()

            elif cfg == 'dhcp':
                self.dhcp = config_file.read()

    def set_SSID(self, ssid):
        """Sets global value for SSID/Wifi Name."""
        self._replace_all("WIFI-SSID", ssid)

    def set_passwd(self, passwd):
        """Sets global value for Wifi password."""
        self._replace_all("WIFI-PASS", passwd)

    def run(self):
        """
        Activates Configuration.

        This will override active config files with the configuration
        created within this object and will restart network services.

        Note
        ----
        If a config file is not loaded for one of the types it will be overriden
        with a blank configuration so its best to always load a file for every
        config type.
        """
        with open('/etc/config/network', 'w') as config_file:
            config_file.write(self.network)

        with open('/etc/config/wireless', 'w') as config_file:
            config_file.write(self.wireless)

        with open('/etc/config/firewall', 'w') as config_file:
            config_file.write(self.firewall)

        with open('/etc/config/dhcp', 'w') as config_file:
            config_file.write(self.dhcp)

        os.popen('ifup wan')
        os.popen('wifi reload')
        os.popen('/etc/init.d/firewall restart')
        os.popen('/etc/init.d/network restart')
        os.popen('/etc/init.d/dnsmasq restart')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

CFG_CLIENT_AP = Config('ClientAP')

CFG_CLIENT_AP.load('firewall', 'firewall')
CFG_CLIENT_AP.load('wireless', 'wireless-client')
CFG_CLIENT_AP.load('network', 'network-client')
CFG_CLIENT_AP.load('dhcp', 'dhcp')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

CFG_AP = Config('AP')

CFG_AP.load('firewall', 'firewall')
CFG_AP.load('wireless', 'wireless-ap')
CFG_AP.load('network', 'network-ap')
CFG_AP.load('dhcp', 'dhcp-ap')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

configs = [CFG_CLIENT_AP, CFG_AP]

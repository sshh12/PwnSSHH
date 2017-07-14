
# PwnSSHH

A Python wrapper for the MR3040.

## Usage

#### Setting Up Device
Instructions heavily based on the [minipwner](http://www.minipwner.com/index.php/build-one).
1. Have a [TP-Link MR3040](https://www.amazon.com/gp/product/B0088PPFP4/), [USB flash drive](https://www.amazon.com/gp/product/B005FYNSZA/), Wi-Fi internet connection, and an Ethernet cable.
2. Partition the USB flash drive with a tool like [Partition Wizard](https://www.partitionwizard.com/) or [gparted](http://gparted.org/)
to have about 96% ext4 and the rest as Linux swap.
3. Download the [OpenWrt image builder](https://downloads.openwrt.org/chaos_calmer/15.05.1/ar71xx/generic/OpenWrt-ImageBuilder-15.05.1-ar71xx-generic.Linux-x86_64.tar.bz2)
and uncompress (```tar xvzf {filename}```).
4. ```make image PROFILE=TLMR3040 PACKAGES="blkid block-mount kmod-fs-ext4 kmod-usb2 kmod-usb-uhci kmod-usb-ohci kmod-usb-storage"```
5. Rename the created image file ```bin/ar71xx/...-v2-squashfs-factory.bin``` to ```openwrt.bin```
6. Put the switch on 3G/4G, connect it to your computer with an Ethernet cord, and power on the device.
5. Navigate to the TP-Link control panel at ```http://192.168.0.1```, then go to System tools -> Firmware Upgrade and upload the openwrt image file.
6. ```telnet 192.168.1.1 23``` and set the password ```passwd``` to enable ssh (no longer need telnet).
7. ```ssh root@192.168.1.1```
8. Edit the fstab config ```vi /etc/config/fstab``` where partitions can be ```sda1``` or ```sda2```
```
config 'global'
        option  anon_swap       '0'
        option  anon_mount      '0'
        option  auto_swap       '1'
        option  auto_mount      '1'
        option  delay_root      '0'
        option  check_fs        '0'

config 'swap'
        option device '/dev/{swap partition}'
        option enabled '1'

config 'mount'
        option target '/overlay'
        option device '/dev/{ext4 partition}'
        option fstype 'ext4'
        option options 'rw,sync'
        option enabled '1'
        option enabled_fsck '0'
```
9. Pivot the root onto the USB drive with the following commands...
```
mkdir -p /tmp/cproot
mount -o bind / /tmp/cproot
mkdir /mnt/{ext4 partition}
mount /dev/{ext4 partition} /mnt/{ext4 partition}
tar -C /tmp/cproot -cvf - . | tar -C /mnt/{ext4 partition} -xf -
umount /tmp/cproot
```
10. Change the mount target in ```/etc/config/fstab``` from ```'/overlay'``` to ```'/'```
11. ```reboot```

#### Setting Up PwnSSHH
1. On main computer, ```git clone https://github.com/sshh12/PwnSSHH.git```
2. Copy files to device ```scp -r /path/to/PwnSSHH root@192.168.1.1:/root/PwnSSHH```
3. ```python /root/PwnSSHH/setup.py``` (This will override config files, banners, etc...)
4. ```reboot```

#### Using
1. PwnSSHH with automatically start on boot and will cycle the leds to indicate startup. 
2. The program can be started manually with ```python /root/PwnSSHH/main.py```.

#### API
If you want to write your own code, the ```pwnsshh``` module will allow one to interface
(read switch state, control leds, init configs, etc...) with the router.

For example
```python
from pwnsshh.leds import all_off, leds

import time

while True:

    all_off() # Turn all leds off

    for led in leds: # Cycle though

        led.on = True

        time.sleep(.5)

        led.on = False
```
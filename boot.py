# boot.py -- run on boot-up
import esp32wlan
import senko
import machine

esp32wlan.wifi.do_connect()

OTA = senko.Senko(user="klaus-trausner", repo="training",  branch ="main", working_dir="", files=["testdatei.txt","testdatei2.txt"])
print("OTA Update: ", OTA.update())

if OTA.update():
    print("Updated to the latest version! Rebooting...")
    machine.reset()
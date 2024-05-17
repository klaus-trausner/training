# boot.py -- run on boot-up
import esp32wlan
import senko
import machine

esp32wlan.wifi.do_connect()

OTA = senko.Senko(user="klaus-trausner", repo="training", url="https://github.com/klaus-trausner/training", branch ="main", working_dir="", files=["testdatei.txt"])
print("OTA Update: ", OTA.update())

if OTA.update():
    print("Updated to the latest version! Rebooting...")
    machine.reset()
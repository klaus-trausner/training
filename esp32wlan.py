import time
import network
import secret
import ntptime


class WiFi:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.timezone = 3600

    def do_connect(self):
        start = time.ticks_ms()
    
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print('connecting to network...')
        self.wlan.connect(secret.wlanSSID, secret.wlanPassword)
        point="."
        while not self.wlan.isconnected() and start + 10000 > time.ticks_ms():
            print(point)
            point+="."
            time.sleep(0.5)

        print("Is connected: ", self.isconnected())    
        print("SSID: ",self.get_ssid())
        print("IP: ", self.get_ip())
        return self.wlan.isconnected()
    

    def isconnected(self):
        return self.wlan.isconnected()
        
    def get_wlan(self):
        return self.wlan
    
    def get_ip(self):
        conf = self.wlan.ifconfig() # (ip, subnet, gateway, dns)
        return conf[0]
    
    def get_ssid(self):
        return self.wlan.config('essid')

    ###### Zeit und Datum #######
    
    # Zeitverschiebung in Sekunden
    def set_timezone(self, zone):
        self.timezone = zone    

    # Sekunden seit 2000-01-01 00:00:00 UTC
    def get_seconds(self):
        try:
            ntptime.settime()
        except:
            pass
        return time.mktime(time.localtime())

    def get_local_seconds(self):
        try:
            ntptime.settime()
        except:
            pass
        return time.mktime(time.localtime()) + self.timezone


    # YYYY, MM, DD, HH, MM, SS, day of week (0=Montag), day of year
    def get_time_values(self, seconds):
        return time.localtime(seconds)
    
    # tt.mm.yyyy
    def date_text(self, seconds):
        zeit = time.localtime(seconds)
        return "{:02d}.{:02d}.{:04d}".format(zeit[2],zeit[1],zeit[0])
    
    # hh:mm:ss
    def time_text(self, seconds):
        zeit = time.localtime(seconds)
        return "{:02d}:{:02d}:{:02d}".format(zeit[3],zeit[4],zeit[5])
    
    # tt.mm.yyyy hh:mm:ss
    def date_time_text(self, seconds):
        return self.date_text(seconds) + " " + self.time_text(seconds)

wifi = WiFi()




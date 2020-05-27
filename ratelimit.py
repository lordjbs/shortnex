# shortnex v2.0
# made by jbs (https://github.com/lordjbs/)
# Copyright (C) 2018-2020 jbs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from utils import set_interval
import json
import threading

with open('config.json') as _config:
    data = json.load(_config)
config = {"timeUntilClear": data["ratelimit"]["timeUntilClear"], "maxRequests": data["ratelimit"]["maxRequests"], "enabled": data["ratelimit"]["enabled"], "maxMultiplier": data["ratelimit"]["maxMultiplier"]}

class Ratelimit:
    def __init__(self):
        self.currentIPs = {}
    
    def loop(self):
        self.set_interval(config["timeUntilClear"])

    def check(self, ip):
        if not config["enabled"]:
            return True

        if ip in self.currentIPs:
            self.addOneRequestToIp(ip)
            if self.currentIPs[ip] > config["maxRequests"]:
                return False
            else:
                return True
        else:
            self.addIpToCurrentIps(ip)
            return True
        

    def addIp(self, ip):
        if ip in self.currentIPs:
            try:
                self.addOneRequestToIp(ip)
            except KeyError:
                self.addIpToCurrentIps(ip)
        else:
            self.addIpToCurrentIps(ip)

    
    def addIpToCurrentIps(self, ip):
        self.currentIPs[ip] = 1
    
    def addOneRequestToIp(self, ip):
        self.currentIPs[ip] += 1
    
    # TODO: add that if the number of requests exceed a given number above the maxrequests value to add the ip to the array again
    def clearIps(self):
        self.currentIPs = self.checkForAbuse()

    def checkForAbuse(self):
        temp = self.currentIPs
        output = {}
        maxReq = config["maxRequests"] * config["maxMultiplier"]
        if temp:
            try:
                for cip, nmbr in temp:
                    if nmbr > maxReq:
                        output[cip] = config["maxRequests"]
            #properly handle this, debug i guess
            except Exception:
                self.a = ""
        return output
        
            
    
    # https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval/14035296#14035296
    def set_interval(self, sec):
        a = sec
        def func_wrapper():
            self.set_interval(a)
            self.clearIps()
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t
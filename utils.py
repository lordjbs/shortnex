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

import random
import re
import string
import threading

regex = re.compile(
    r'^(?:http|ftp)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ip
    r'(?::\d+)?'  # port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def checkIfProperURL(url):
    return re.match(regex, returnProperURL(url))


def returnProperURL(url):
    out = url
    if not re.match(r'^https://', url) or not out.startswith("https://"):
        if not re.match(r'^http://', url) or not out.startswith("http://"):
            out = "https://" + url
    return out


def createID():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(6)])

def createRandomString(nmbr):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(nmbr)]) 

# https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval/14035296#14035296
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

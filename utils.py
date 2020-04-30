
# shortnex v2.0
# made by jbs (https://github.com/lordjbs/)

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import string, random, re

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def checkIfProperURL(url):
    return re.match(regex, returnProperURL(url))


def returnProperURL(url):
    out = url
    print(out)

    if not re.match(r'^https://', url) or not out.startswith("https://"):
        if not re.match(r'^http://', url) or not out.startswith("http://"):
            out = "https://" + url
    print(out)
    return out

def createID():
    ran = ''.join([random.choice(string.ascii_letters
                                    + string.digits) for n in range(6)])
    return ran

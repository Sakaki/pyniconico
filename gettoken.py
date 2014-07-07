# -*- coding:utf-8 -*-

import pycurl
from cStringIO import StringIO
import re

def getToken(cookie):
    buf = StringIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, "http://www.nicovideo.jp/my/mylist")
    curl.setopt(pycurl.COOKIEFILE, 'cookie')
    curl.setopt(curl.WRITEFUNCTION, buf.write)
    curl.perform()

    res = buf.getvalue()
    buf.close()

    line = re.search('NicoAPI\.token = "(.*)";', res)
    token = line.group(1)

    return token


if __name__ == '__main__':
    cookie = 'cookie'
    token = getToken(cookie)
    print token

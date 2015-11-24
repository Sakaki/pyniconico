# -*- conding:utf-8 -*-

import sys
from xml.etree.ElementTree import *
from nicoreq import getres

apiurl = "http://ext.nicovideo.jp/api/getthumbinfo/{0}"
attrs = ["title", "user_nickname", "watch_url", "size_high", "size_low", "movie_type"]

def getInfo(vid):
    url = apiurl.format(vid)
    apires = getres(url)
    elem = fromstring(apires).find("thumb")

    result = {}
    for attr in attrs:
        text = elem.findtext(attr)
        if type(text) == unicode:
            text = text.encode("utf-8")
        result[attr] = text
    return result

if __name__ == "__main__":
    print getInfo(sys.argv[1])

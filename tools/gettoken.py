# -*- coding:utf-8 -*-

import re
import nicoreq

def getToken(cookie):
    url = 'http://www.nicovideo.jp/my/mylist'
    res = nicoreq.getres(url, cookie_in=cookie)

    line = re.search('NicoAPI\.token = "(.*)";', res)
    token = line.group(1)

    return token


if __name__ == '__main__':
    cookie = 'cookie'
    token = getToken(cookie)
    print token

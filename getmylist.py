# -*- coding:utf-8 -*-

import nicoreq

def getmllst(cookie):
    url = 'http://www.nicovideo.jp/api/mylistgroup/list'
    text = nicoreq.getres(url, cookie_in=cookie)

    text = text.split('"')
    mlnames = []

    index = 0
    while(index < len(text)):
        if text[index] == 'id':
            item = {}
            item['id'] = text[index+2]
            name = text[index+10]
            if name.startswith('\\'):
                name = _convunichrs(name)
            item['name'] = name
            mlnames.append(item)
        index += 1

    return mlnames

def _convunichrs(unistr):
    chars = unistr.split('\\u')
    chars = map(lambda char: unichr(int(char, 16)).encode('utf-8'), chars[1:])

    return ''.join(chars)

if __name__ == '__main__':
    cookie = 'cookie'
    lst = getmllst(cookie)

    for item in lst:
        print item['name'], item['id']

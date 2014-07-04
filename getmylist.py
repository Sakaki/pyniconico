import pycurl
import cStringIO

def getmllst(cookie):
    buf = cStringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, 'http://www.nicovideo.jp/api/mylistgroup/list')
    c.setopt(pycurl.COOKIEFILE, cookie)
    c.setopt(c.WRITEFUNCTION, buf.write)

    c.perform()

    text = buf.getvalue()
    buf.close()

    text = text.split('"')
    mlnames = []

    index = 0
    while(index < len(text)):
        if text[index] == 'name':
            mlnames.append(text[index+2])
        index += 1

    for i, name in enumerate(mlnames):
        if name.startswith('\\'):
            result = ''
            chars = name.split('\\')
            chars = map(lambda char: char.replace('u', ''), chars)
            chars = map(lambda char: unichr(int(char, 16)).encode('utf-8'), chars[1:])
            for c in chars:
                result += c
            mlnames[i] = result

    return mlnames


if __name__ == '__main__':
    cookie = 'cookie'
    lst = getmllst(cookie)

    for name in lst:
        print name

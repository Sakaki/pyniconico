# -*- coding:utf-8 -*-
from sys import argv

import nicoreq, gettoken, getmylist

def getMylistSongs(mylistname, cookie):
    token = gettoken.getToken(cookie)
    for item in getmylist.getmllst(cookie):
        if item['name'] == mylistname:
            gid = item['id']

    params = {'group_id': gid,
            'token': token}

    """buf = cStringIO.StringIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, 'http://www.nicovideo.jp/api/mylist/list')
    curl.setopt(pycurl.COOKIEFILE, cookie)
    curl.setopt(curl.WRITEFUNCTION, buf.write)
    curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(opts))
    curl.setopt(pycurl.POST, 1)

    curl.perform()

    res = buf.getvalue()
    buf.close()"""

    url = 'http://www.nicovideo.jp/api/mylist/list'
    res = nicoreq.getres(url,
                         cookie_in=cookie,
                         post_params=params)
    res = res.split('"');

    ids = []
    index = 0
    while(len(res) > index):
        if res[index] == 'video_id':
            ids.append(res[index+2])
        index += 1;

    return ids


if __name__ == '__main__':
    cookie = 'cookie'
    mllst = getmylist.getmllst(cookie)

    for mldict in mllst:
        mlname = mldict['name']
        print mlname+':'
        ids = getMylistSongs(mlname, cookie)
        for vid in ids:
            print '  '+vid

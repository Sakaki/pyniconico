# -*- coding:utf-8 -*-

import urllib, re, sys, os
import nicoreq, convunichrs

def _getsonginfo(regexp, page):
    temp = re.search(regexp, page)
    return temp.group(1)

def download(vid, cookie, loc='./', overwrite=True):
    url = 'http://www.nicovideo.jp/watch/'+vid
    vpage = nicoreq.getres(url,
                           cookie_in=cookie,
                           cookie_out=cookie)

    title = _getsonginfo('<span class="videoHeaderTitle" style="font-size:24px">(.*?)<\/span>', vpage)
    author = _getsonginfo('nickname&quot;:&quot;(.*?) \\\u3055\\\u3093&quot', vpage)
    author = convunichrs.convert(author)

    print title, author

    url = 'http://flapi.nicovideo.jp/api/getflv?v='+vid
    res = nicoreq.getres(url,
                         cookie_in=cookie)

    videourl = res.split('&')[2].replace('url=', '')
    videourl = urllib.unquote(videourl)

    videofile = loc+title+'.flv'
    if not overwrite and os.path.exists(videofile):
        return None

    with open(videofile, 'wb') as f:
        print 'Downloading...'
        res = nicoreq.getres(videourl,
                             cookie_in=cookie)
        print 'finished. Writing to file...'
        f.write(res)

    return {'title': title,
            'author': author}


if __name__ == '__main__':
    vid = sys.argv[1]
    cookie = 'cookie'

    download(vid, cookie)

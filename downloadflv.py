#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib, re, sys, os
from tools import nicoreq, convunichrs, mp3, nicoinfo
from tools.command import Command

class DownloadFlv(Command):
    cmdname = 'download niconico flv'

    def __init__(self, args):
        super(DownloadFlv, self).__init__()
        self.parser.add_argument('vid',
                                 metavar='VID',
                                 help='video id')
        self.parser.add_argument('-l', '--location',
                                 dest='location',
                                 default='./video/',
                                 help='video output folder')
        self.parser.add_argument('-f', '--force',
                                 dest='overwrite',
                                 action='store_true',
                                 help='allow overwrite')
        self.parser.add_argument('--mp3',
                                 dest='mp3conv',
                                 action='store_true',
                                 help='convert to mp3')
        self.parser.add_argument('-b', '--bitrate',
                                 dest='bitrate',
                                 default=192,
                                 help='mp3 bitrate')
        self.setParser(args)

    def _getsonginfo(self, regexp, page):
        temp = re.search(regexp, page)
        return temp.group(1)

    def invoke(self):
        vinfo = nicoinfo.getInfo(self.args.vid)
        nicoreq.getres(vinfo["watch_url"],
                       cookie_in=self.cookie,
                       cookie_out=self.cookie)

        url = 'http://www.nicovideo.jp/watch/'+self.args.vid
        vpage = nicoreq.getres(url,
                               cookie_in=self.cookie,
                               cookie_out=self.cookie)

#        title = self._getsonginfo('<span class="videoHeaderTitle" style="font-size:..px">(.*?)<\/span>', vpage)
#        author = self._getsonginfo('nickname&quot;:&quot;(.*?) \\\u3055\\\u3093&quot', vpage)
#        author = convunichrs.convert(author)

        print vinfo["title"], vinfo["user_nickname"]

        url = 'http://flapi.nicovideo.jp/api/getflv?v='+self.args.vid
        res = nicoreq.getres(url,
                             cookie_in=self.cookie)

        videourl = res.split('&')[2].replace('url=', '')
        videourl = urllib.unquote(videourl)
        is_premium = "is_premium=1" in res

        if not self.args.location.endswith('/'):
            self.args.location += '/'
        vfile = "{0}{1}.{2}".format(self.args.location, vinfo["title"], vinfo["movie_type"])
        if not self.args.overwrite and os.path.exists(vfile):
            print "File exists. Skipping..."
            return

        with open(vfile, 'wb') as f:
            size_h = int(vinfo["size_high"])
            size_l = int(vinfo["size_low"])
            if is_premium or size_l == 0:
                size = size_h
            else:
                size = size_l
            progressbar_info = {
                "show_progress": True,
                "size": size
            }
            res = nicoreq.getres(videourl,
                                 cookie_in=self.cookie,
								 progressbar_info=progressbar_info)
            print 'finished. Saving to "{0}"'.format(vfile)
            f.write(res)

        if self.args.mp3conv:
            mp3.convert(vfile, self.args.bitrate, vinfo["title"], vinfo["user_nickname"])


if __name__ == '__main__':
    DownloadFlv(None).invoke()


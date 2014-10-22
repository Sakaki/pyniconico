# -*- coding:utf-8 -*-

import urllib, re, sys, os
from tools import nicoreq, convunichrs, mp3
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
        url = 'http://www.nicovideo.jp/watch/'+self.args.vid
        vpage = nicoreq.getres(url,
                               cookie_in=self.cookie,
                               cookie_out=self.cookie)

        title = self._getsonginfo('<span class="videoHeaderTitle" style="font-size:24px">(.*?)<\/span>', vpage)
        author = self._getsonginfo('nickname&quot;:&quot;(.*?) \\\u3055\\\u3093&quot', vpage)
        author = convunichrs.convert(author)

        print title, author

        url = 'http://flapi.nicovideo.jp/api/getflv?v='+self.args.vid
        res = nicoreq.getres(url,
                             cookie_in=self.cookie)

        videourl = res.split('&')[2].replace('url=', '')
        videourl = urllib.unquote(videourl)

        if not self.args.location.endswith('/'):
            self.args.location += '/'
        videofile = self.args.location+title+'.flv'
        if not self.args.overwrite and os.path.exists(videofile):
            return None

        with open(videofile, 'wb') as f:
            print 'Downloading...'
            res = nicoreq.getres(videourl,
                                 cookie_in=self.cookie)
            print 'finished. Writing to "{0}"'.format(videofile)
            f.write(res)

        if self.args.mp3conv:
            mp3.convert(videofile, self.args.bitrate, author, title)


if __name__ == '__main__':
    DownloadFlv(None).invoke()

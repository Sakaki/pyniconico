#!/usr/bin/env python
# -*- coding:utf-8 -*-

import getmylist
from tools import nicoreq, gettoken
from tools.command import Command

class GetMLSongs(Command):
    cmdname = 'get songs in mylist'
    mldata = []

    def __init__(self, args):
        super(GetMLSongs, self).__init__()
        self.parser.add_argument('--raw',
                                 dest='raw',
                                 action='store_true',
                                 help='raw output')
        self.parser.add_argument('-n', '--name',
                                 dest='mlname',
                                 default=None,
                                 help='mylist name')
        self.setParser(args)
        self.mldata = getmylist.MyList(self.args).invoke()

    def invoke(self):
        mlnames = []
        if self.args.mlname:
            mlnames = [self.args.mlname]
        else:
            for mldic in self.mldata:
                mlnames.append(mldic['name'])

        for mlname in mlnames:
            spacer = ''
            if not self.args.raw:
                print mlname+':'
                spacer = '  '

            ids = self.getMLSongs(mlname)
            for vid in ids:
                print spacer+vid

    def getMLSongs(self, mylistname):
        token = gettoken.getToken(self.cookie)
        for item in self.mldata:
            if item['name'] == mylistname:
                gid = item['id']

        params = {'token': token}
        if gid != '':
            params['group_id'] = gid
            url = 'http://www.nicovideo.jp/api/mylist/list'
        else:
            url = 'http://www.nicovideo.jp/api/deflist/list'

        res = nicoreq.getres(url,
                             cookie_in=self.cookie,
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
    GetMLSongs(None).invoke()

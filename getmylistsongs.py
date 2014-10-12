# -*- coding:utf-8 -*-

import getmylist
from tools import nicoreq, gettoken
from tools.command import Command

class GetMLSongs(Command):
    cmdname = 'get songs in mylist'
    mldata = []

    def __init__(self, args):
        super(GetMLSongs, self).__init__()
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
            print mlname+':'
            ids = self.getMLSongs(mlname)
            for vid in ids:
                print '  '+vid

    def getMLSongs(self, mylistname):
        token = gettoken.getToken(self.cookie)
        for item in self.mldata:
            if item['name'] == mylistname:
                gid = item['id']

        params = {'group_id': gid,
                  'token': token}

        url = 'http://www.nicovideo.jp/api/mylist/list'
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

    """cookie = 'cookie'
    mllst = getmylist.getmllst(cookie)

    for mldict in mllst:
        mlname = mldict['name']
        print mlname+':'
        ids = getMylistSongs(mlname, cookie)
        for vid in ids:
            print '  '+vid"""

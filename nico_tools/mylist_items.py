#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from nico_tools.mylist import MyList
from nico_tools.nicowalker import NicoWalker
import re


class GetMyListItems(NicoWalker):
    command_name = 'get songs in mylist'

    def __init__(self, args):
        super(GetMyListItems, self).__init__()
        self.parser.add_argument('--raw',
                                 dest='raw',
                                 action='store_true',
                                 help='raw output')
        self.parser.add_argument('-n', '--name',
                                 dest='mlname',
                                 default=None,
                                 help='mylist name')
        self.set_parser(args)
        self.mylist_array = MyList.get_mylist_names(self.session)

    def invoke(self):
        mylist_names = []
        if self.args.mlname:
            mylist_names = [self.args.mlname]
        else:
            for mylist in self.mylist_array:
                mylist_names.append(mylist['name'])

        for mylist_name in mylist_names:
            spacer = ''
            if not self.args.raw:
                print(mylist_name + ':')
                spacer = '  '

            mylist_items = self.get_mylist_items(mylist_name, self.session, self.mylist_array)
            for mylist_item in mylist_items:
                print(spacer + mylist_item["item_data"]["watch_id"])

    @staticmethod
    def get_mylist_items(mylist_name, session, mylist_array):
        url = 'http://www.nicovideo.jp/my/mylist'
        res = session.get(url).text
        line = re.search('NicoAPI\.token = "(.*)";', res)
        token = line.group(1)
        params = {'token': token}

        mylist_id = ""
        for mylist in mylist_array:
            if mylist['name'] == mylist_name:
                mylist_id = mylist['id']
        if mylist_id != '':
            params['group_id'] = mylist_id
            url = 'http://www.nicovideo.jp/api/mylist/list'
        else:
            url = 'http://www.nicovideo.jp/api/deflist/list'

        res_json = session.post(url, data=params).json()
        if res_json["status"] != "ok":
            print("Error loading mylist(Status is {0})".format(res_json["status"]))
            return []
        else:
            return res_json["mylistitem"]


if __name__ == '__main__':
    GetMyListItems(None).invoke()

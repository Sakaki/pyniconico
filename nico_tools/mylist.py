#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from nico_tools import convunichrs
from nico_tools.nicowalker import NicoWalker


class MyList(NicoWalker):
    command_name = 'getmylist'

    def __init__(self, args):
        super(MyList, self).__init__()
        self.set_parser(args)

    def invoke(self):
        for item in self.get_mylist_names(self.session):
            print(item['name'], item['id'])

    @staticmethod
    def get_mylist_names(session):
        url = 'http://www.nicovideo.jp/api/mylistgroup/list'
        text = session.get(url).text
        text = text.split('"')

        mylist_items = []
        index = 0
        while index < len(text):
            if text[index] == 'id':
                mylist_name = text[index+10]
                if mylist_name.startswith('\\'):
                    mylist_name = convunichrs.convert_unichars(mylist_name)
                mylist_item = {
                    "name": mylist_name,
                    "id": text[index + 2]
                }
                mylist_items.append(mylist_item)
            index += 1
        mylist_items.append({'name': 'とりあえずマイリスト', 'id': ''})

        return mylist_items


if __name__ == '__main__':
    MyList(None).invoke()

# -*- coding:utf-8 -*-

from tools import nicoreq, convunichrs
from tools.command import Command

class MyList(Command):
    cmdname = 'getmylist'

    def __init__(self, args):
        super(MyList, self).__init__()
        self.setParser(args)

    def invoke(self):
        url = 'http://www.nicovideo.jp/api/mylistgroup/list'
        text = nicoreq.getres(url, cookie_in=self.cookie)

        text = text.split('"')
        mlnames = []

        index = 0
        while(index < len(text)):
            if text[index] == 'id':
                item = {}
                item['id'] = text[index+2]
                name = text[index+10]
                if name.startswith('\\'):
                    name = convunichrs.convert(name)
                item['name'] = name
                mlnames.append(item)
            index += 1

        mlnames.append({'name': 'とりあえずマイリスト', 'id': ''})

        return mlnames


if __name__ == '__main__':
    cookie = 'cookie'
    lst = MyList(None).invoke()

    for item in lst:
        print item['name'], item['id']

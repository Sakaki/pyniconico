# -*- coding:utf-8 -*-

import argparse
import getcookie

class Command(object):
    cookie = '__cookie__'

    def __init__(self):
        self.parser = argparse.ArgumentParser(description=self.cmdname)
        self.parser.add_argument('-u', '--username',
                                 dest='mail',
                                 default=None,
                                 help='username')
        self.parser.add_argument('-p', '--password',
                                 dest='passwd',
                                 default=None,
                                 help='password')

    def setParser(self, args=None):
        if not args:
            args = self.parser.parse_args()
        mail = args.mail
        passwd = args.passwd

        if not mail or not passwd:
            mail, passwd = getcookie.getLoginInfo()

        self.mail = mail
        self.passwd = passwd
        assert self.login(), 'ログインに失敗しました'

        self.args = args

    def login(self):
        return getcookie.getCookie(self.mail, self.passwd, self.cookie)

    def checkLogin(self):
        return getcookie.checkLogin(self.cookie)

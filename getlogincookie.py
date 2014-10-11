# -*- coding:utf-8 -*-

import nicoreq, re, netrc

def getLoginCookie(mail, passwd, cookie):
    url = "https://secure.nicovideo.jp/secure/login"
    params = {
	    'mail': mail,
	    'password': passwd,
	    'next_url': '',
	    'site': "niconico"}

    nicoreq.getres(url,
		   cookie_out=cookie,
		   post_params=params,
		   require_ssl=True)

def checkLogin(cookie):
    url = 'http://www.nicovideo.jp/my/mylist'
    res = nicoreq.getres(url,
                   cookie_in=cookie,
                   require_ssl = True)

    if res != '':
        return True
    else:
        return False

def getLoginInfo():
    auth = netrc.netrc()
    mail, a, passwd = auth.authenticators("nicovideo")
    return mail, passwd

if __name__ == '__main__':
    cookie = 'cookie'
    mail, passwd = getLoginInfo()
    getLoginCookie(mail, passwd, cookie)

    if checkLogin(cookie):
        print 'ログイン成功'
    else:
        print 'ログイン失敗'

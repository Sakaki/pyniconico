# -*- coding:utf-8 -*-

import nicoreq

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


if __name__ == '__main__':
    cookie = 'cookie'
    with open('auth', 'r') as f:
        lines = f.read().split(',')
        mail = lines[0]
        passwd = lines[1]

    getLoginCookie(mail, passwd, cookie)

    with open(cookie, 'r') as f:
        print f.read()

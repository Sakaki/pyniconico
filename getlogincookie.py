# -*- coding:utf-8 -*-

import pycurl, urllib

def getLoginCookie(mail, passwd, cookie):
	params = {
		'mail': mail,
		'password': passwd,
		'next_url': '',
		'site': "niconico"}

	params_encoded = urllib.urlencode(params)

	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, "https://secure.nicovideo.jp/secure/login")
	curl.setopt(pycurl.POSTFIELDS, params_encoded)
	curl.setopt(pycurl.POST, 1)

	curl.setopt(pycurl.SSLVERSION, 3)
	curl.setopt(pycurl.COOKIEJAR, cookie)

	curl.perform()


if __name__ == '__main__':
    cookie = 'cookie'
    with open('auth', 'r') as f:
        lines = f.read().split(',')
        mail = lines[0]
        passwd = lines[1]

    getLoginCookie(mail, passwd, cookie)

    with open(cookie, 'r') as f:
        print f.read()

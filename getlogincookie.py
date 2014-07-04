import pycurl, urllib


def getLoginCookie(mail, password, cookiename):
    opt = {'mail': mail,
           'password': password}

    c = pycurl.Curl()

    c.setopt(c.URL, 'https://secure.nicovideo.jp/secure/login?site=niconico')
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, urllib.urlencode(opt))
    c.setopt(pycurl.SSLVERSION, pycurl.SSLVERSION_SSLv3)
    c.setopt(pycurl.COOKIEJAR, cookiename)

    c.perform()


if __name__ == "__main__":
    cookiefile = "cookie"
    with open("auth", "r") as f:
        lines = f.readlines()
        mail = lines[0]
        passwd = lines[1]

    getLoginCookie(mail, passwd, cookiefile)

    with open(cookiefile, "r") as f:
        print f.read()

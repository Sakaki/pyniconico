# -*- coding:utf-8 -*-

import urllib, urllib2, urllib2_ssl, os
from cookielib import LWPCookieJar
from progressbar import ProgressBar, Percentage, Bar, ETA

def getres(url, cookie_in=None, cookie_out=None, post_params=None, require_ssl=False, progressbar_info={"show_progress": False}):
    """
    HTTPリクエスト
    :url: リクエストを送信するURL
    :cookie_in: 読み込むクッキーファイル
    :cookie_out: 書き込むクッキーファイル
    :post_params: POSTする辞書リスト
    :require_ssl: 接続にSSL(v3)を使用するか
    :progressbar_info: プログレスバーの情報
    """

    if require_ssl:
        #handler = urllib2_ssl.HTTPSHandler(ca_certs=os.path.dirname(__file__)+'/cert/cacert.pem')
        handler = urllib2_ssl.TLS1Handler()
    else:
        handler = urllib2.HTTPHandler()

    if cookie_in != None or cookie_out != None:
        cookiejar = LWPCookieJar(cookie_in or cookie_out)
        if cookie_in != None:
            cookiejar.load()
        cProcessor = urllib2.HTTPCookieProcessor(cookiejar)
        opener = urllib2.build_opener(cProcessor, handler)
    else:
        opener = urllib2.build_opener(handler)

    if post_params != None:
        res = opener.open(url, urllib.urlencode(post_params))
    else:
        res = opener.open(url)

    result = ""
    if progressbar_info["show_progress"]:
        size = progressbar_info["size"]
        divsize = int(size/100)
        downloaded = 0

        widgets = ["Downloading: ", Percentage(), Bar(), ETA()]
        pbar = ProgressBar(maxval=100, widgets=widgets).start()
        while True:
            fragment = res.read(divsize)
            downloaded += len(fragment)
            if not fragment:
                break
            result += fragment
            pbar.update(int(downloaded/divsize))
        pbar.finish()
    else:
        result = res.read()

    if cookie_out != None:
        cookiejar.save()

    return result

# -*- coding:utf-8 -*-

import pycurl, urllib
from cStringIO import StringIO

def getres(url, cookie_in=None, cookie_out=None, post_params=None, require_ssl=False):
    """
    HTTPリクエスト
    :url: リクエストを送信するURL
    :cookie_in: 読み込むクッキーファイル
    :cookie_out: 書き込むクッキーファイル
    :post_params: POSTする辞書リスト
    :require_ssl: 接続にSSL(v3)を使用するか
    """
    buf = StringIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    if post_params:
        curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(post_params))
        curl.setopt(pycurl.POST, 1)
    if require_ssl:
        curl.setopt(pycurl.SSLVERSION, 3)
    if cookie_in:
        curl.setopt(pycurl.COOKIEFILE, cookie_in)
    if cookie_out:
        curl.setopt(pycurl.COOKIEJAR, cookie_out)
    curl.setopt(curl.WRITEFUNCTION, buf.write)

    curl.perform()
    res = buf.getvalue()
    buf.close()

    return res

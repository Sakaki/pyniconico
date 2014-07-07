# -*- coding:utf-8 -*-
import pycurl, urllib
import cStringIO

buf = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(pycurl.URL, 'http://www.nicovideo.jp/api/deflist/list')
c.setopt(pycurl.COOKIEFILE, 'cookie')
c.setopt(c.WRITEFUNCTION, buf.write)
#c.setopt(pycurl.POSTFIELDS, params_encoded)
#c.setopt(pycurl.POST, 1)

c.perform()

res = buf.getvalue()
buf.close()

print res

'''with open('mlsongstest', 'r') as f:
    res = f.read()

print res
'''

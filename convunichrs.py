# -*- coding:utf-8 -*-

import re

def convert(unistr):
    unichrlst = re.findall(r'\\u.{4}', unistr)
    for uchar in unichrlst:
        code = int(uchar.replace('\\u', ''), 16)
        schar = unichr(code).encode('utf-8')
        unistr = unistr.replace(uchar, schar)

    return unistr

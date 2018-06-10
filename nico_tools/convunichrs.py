# -*- coding:utf-8 -*-

import re


def convert_unichars(unistr):
    unichrlst = re.findall(r'\\u.{4}', unistr)
    for uchar in unichrlst:
        code = int(uchar.replace('\\u', ''), 16)
        schar = chr(code)
        unistr = unistr.replace(uchar, schar)

    return unistr

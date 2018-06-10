# -*- conding:utf-8 -*-

import sys
from xml.etree.ElementTree import fromstring

apiurl = "http://ext.nicovideo.jp/api/getthumbinfo/{0}"
attrs = ["title", "user_nickname", "watch_url", "size_high", "size_low", "movie_type", "thumbnail_url"]


def parse_video_info(api_response_text):
    elem = fromstring(api_response_text).find("thumb")
    result = {}
    for attr in attrs:
        text = elem.findtext(attr)
        if type(text) == bytes:
            text = text.decode("utf-8")
        result[attr] = text
    return result

if __name__ == "__main__":
    print(parse_video_info(sys.argv[1]))

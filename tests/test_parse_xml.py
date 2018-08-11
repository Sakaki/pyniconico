from unittest import TestCase
from nico_tools.nico_xml_parser import parse_video_info
import requests

api_url = "http://ext.nicovideo.jp/api/getthumbinfo/sm32093759"


class TestParse(TestCase):

    def test_parse_xml(self):
        # 動画情報のキーが存在すればOK
        api_response_text = requests.get(api_url).content
        video_info = parse_video_info(api_response_text)
        print(video_info)
        for key in ["title", "user_nickname", "watch_url", "thumbnail_url"]:
            self.assertTrue(key in video_info)

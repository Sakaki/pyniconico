from unittest import TestCase
from nico_tools import mp3_tag
import requests
import os
from mutagen.id3 import ID3

test_mp3 = {
    "url": "https://drive.google.com/uc?export=download&id=1TZj85GYJIeWSuQ8a11oHd6-Y_pXRmhpg",
    "cover_art_url": "http://tn.smilevideo.jp/smile?i=20242331",
    "file_name": "test.mp3"
}
test_tags = {
    "title": "test_title",
    "artist": "test_artist",
    "album": "test_album"
}


class TestMP3Tag(TestCase):

    def setUp(self):
        # テスト対象のmp3をダウンロード
        response = requests.get(test_mp3.get("url"))
        with open(test_mp3.get("file_name"), "wb") as f:
            f.write(response.content)

    def tearDown(self):
        os.remove(test_mp3.get("file_name"))

    def test_add_tag(self):
        mp3_tag.add_tag(test_mp3.get("file_name"), test_mp3["cover_art_url"], test_tags.get("title"),
                        test_tags.get("artist"), test_tags.get("album"))
        tags = ID3(test_mp3.get("file_name"))
        self.assertEqual(tags.get("TIT2"), test_tags.get("title"))
        self.assertEqual(tags.get("TPE1"), test_tags.get("artist"))
        self.assertEqual(tags.get("TALB"), test_tags.get("album"))

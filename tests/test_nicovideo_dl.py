from unittest import TestCase
import netrc
from niconico import NicoVideoArgs
from nico_tools.nicovideo_dl import DownloadVideo
import os
import tests

video_id = "sm20242331"
video_file_name = "CB.mp4.mp4"
mp3_file_name = "CB.mp4.mp3"


class TestDownloadVideo(TestCase):

    def setUp(self):
        # ログイン情報はnetrcから取る
        auth = netrc.netrc()
        self.username, _, self.password = auth.authenticators("nicovideo")

    def test_download_video(self):
        # テスト動画をDLして、サイズが0バイト以上だったらOK
        arguments_dict = {
            "mail": self.username,
            "password": self.password,
            "web_driver": tests.test_driver
        }
        arguments = NicoVideoArgs(arguments_dict)
        download_obj = DownloadVideo(arguments)
        download_obj.download(download_obj.session, video_id, "./", overwrite=True)
        self.assertTrue(os.path.exists(video_file_name))
        self.assertGreater(os.path.getsize(video_file_name), 0)

    def test_convert_mp3(self):
        # テスト動画をmp3
        if not os.path.exists(video_file_name):
            self.test_download_video()
        video_info = {
            "thumbnail_url": "http://tn.smilevideo.jp/smile?i=32093759",
            "title": "test_title",
            "user_nickname": "test_user"
        }
        DownloadVideo.convert_mp3(video_info, video_file_name, 192, leave_flv=True)
        self.assertTrue(os.path.exists(mp3_file_name))
        self.assertGreater(os.path.getsize(mp3_file_name), 0)

    def tearDown(self):
        os.remove(video_file_name)
        if os.path.exists(mp3_file_name):
            os.remove(mp3_file_name)

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from kivy.app import App
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from os import path, sep
from threading import Thread
from nicovideo_dl import DownloadVideo
from tools.nicowalker import LoginFailedException

# フォント設定
font_dir = "{0}{1}font".format(path.dirname(path.abspath(__file__)), sep)
resource_add_path(font_dir)
LabelBase.register(DEFAULT_FONT, 'ipag.ttf')


class ChooseDirectoryDialog(FloatLayout):
    set_path = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    download_dir = StringProperty()
    progress = NumericProperty()
    status_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = None
        self.download_dir = path.dirname(path.abspath(__file__))
        self.progress = 0
        self.video_title = ""

        class Args:
            pass
        args = Args()
        args.mail = None
        args.passwd = None
        try:
            self.download_video = DownloadVideo(args)
            status_text = "ログインに成功しました。ユーザー名とパスワードは入力不要です。"
        except LoginFailedException:
            self.download_video = None
            status_text = "ユーザー名とパスワードを入力してください"
        self.status_text = status_text

    def set_path(self, dir_path):
        self.download_dir = dir_path
        self.dismiss_popup()

    def show_choose_dir(self):
        content = ChooseDirectoryDialog(set_path=self.set_path, cancel=self.dismiss_popup)
        self.popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def dismiss_popup(self):
        self.popup.dismiss()

    def start(self):
        self.progress = 0

    def finish(self):
        self.progress = 0

    def update(self, value):
        self.status_text = "ダウンロード中: {0} / {1}%".format(self.video_title, value)
        self.progress = value

    def start_download(self):
        self.status_text = "ダウンロードを開始しています"
        Thread(target=self.download).start()

    def download(self):
        watch_id = self.ids.input_watch_id.text
        if watch_id == "":
            self.status_text = "URLか動画IDを指定してください"
            return
        if watch_id.startswith("http"):
            watch_id = watch_id.split("/")[-1]
        if "?" in watch_id:
            watch_id = watch_id.split["?"][0]
        if self.ids.input_user_id.text != "":
            user_id = self.ids.input_user_id.text
        else:
            user_id = None
        if self.ids.input_password.text != "":
            password = self.ids.input_password.text
        else:
            password = None

        class Args:
            pass
        args = Args()
        args.vid = watch_id
        args.location = self.download_dir
        args.mail = user_id
        args.passwd = password
        if self.download_video is None:
            try:
                self.download_video = DownloadVideo(args)
            except LoginFailedException:
                self.status_text = "ログインに失敗しました"
                return

        session = self.download_video.session
        video_info = DownloadVideo.get_video_metadata(session, watch_id)
        self.video_title = video_info["title"]
        flv_url = DownloadVideo.get_download_url(session, video_info, watch_id)
        flv_path = DownloadVideo.gen_video_path(args.location, video_info)
        # ファイルが存在したら終了
        if path.exists(flv_path):
            self.status_text = "ファイルが存在します"
            return
        # ダウンロード実行
        if not DownloadVideo.exec_download(session, flv_url, flv_path, self):
            self.status_text = "ダウンロードが失敗しました"
        else:
            self.status_text = "ダウンロード完了"


class NicoVideoDLApp(App):
    pass

if __name__ == '__main__':
    Config.set('graphics', 'width', '700')
    Config.set('graphics', 'height', '350')
    Factory.register('Root', cls=Root)
    Factory.register('ChooseDirectoryDialog', cls=ChooseDirectoryDialog)
    NicoVideoDLApp().run()

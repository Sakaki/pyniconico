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


class LoginDialog(FloatLayout):
    start_login = ObjectProperty(None)
    label_login_status = StringProperty()

    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.label_login_status = message


class LoginProgressDialog(FloatLayout):
    pass


class Root(FloatLayout):
    download_dir = StringProperty()
    progress = NumericProperty()
    status_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = None
        self.login_dialog = None
        self.download_dir = path.dirname(path.abspath(__file__))
        self.progress = 0
        self.video_title = ""
        self.download_video = None

        class Args:
            pass
        self.configs = Args()

    def open_settings(self):
        App.open_settings()

    def start_login(self, mail, passwd, init=False):
        if not init:
            self.login_dialog.label_login_status = "ログインしています・・・"
        Thread(target=self.login, args=(mail, passwd, init, )).start()

    def login(self, mail, passwd, init=False):
        if self.login_dialog is not None and isinstance(self.login_dialog, Popup):
            self.login_dialog.dismiss()
        content = LoginProgressDialog()
        progress_dialog = Popup(title="ログイン", content=content, size_hint=(0.3, 0.3))
        progress_dialog.open()
        if mail == "":
            mail = None
        if passwd == "":
            passwd = None
        self.configs.mail = mail
        self.configs.passwd = passwd
        try:
            self.download_video = DownloadVideo(self.configs)
            self.status_text = "ログインに成功しました"
        except LoginFailedException:
            if init:
                message = "ユーザー名とパスワードを入力してください"
            else:
                message = "ログインに失敗しました"
            login_dialog = LoginDialog(message, start_login=self.start_login)
            self.login_dialog = Popup(title="ログイン", content=login_dialog, size_hint=(0.8, 0.9))
            self.login_dialog.open()
        finally:
            progress_dialog.dismiss()

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

        class Args:
            pass
        args = Args()
        args.vid = watch_id
        args.location = self.download_dir

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
    def on_start(self):
        self.root.start_login(None, None, init=True)
        self.root.ids.button_settings.bind(on_release=self.open_settings)
        for key in ["mp3conv", "bitrate", "overwrite"]:
            setattr(self.root.configs, key, self.config.get("general", key))

    def build_config(self, config):
        config.read("nicovideo_dl.ini")

    def build_settings(self, settings):
        settings.add_json_panel('Download Settings', self.config, filename='settings.json')

    def on_config_change(self, config, section, key, value):
        setattr(self.root.download_video.args, key, value)


if __name__ == '__main__':
    Config.set('graphics', 'width', '700')
    Config.set('graphics', 'height', '350')
    Factory.register('Root', cls=Root)
    Factory.register('ChooseDirectoryDialog', cls=ChooseDirectoryDialog)
    Factory.register("LoginDialog", cls=LoginDialog)
    NicoVideoDLApp().run()

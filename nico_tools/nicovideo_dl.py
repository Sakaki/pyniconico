#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from urllib import parse
import os
from nico_tools import nico_xml_parser
from nico_tools.nicowalker import NicoWalker
from nico_tools.mylist_items import GetMyListItems
from nico_tools.mylist import MyList
from progressbar import ProgressBar, Percentage, Bar, ETA
import subprocess
from nico_tools import mp3_tag
import re

character_replace = {
    "\\": "＼",
    "/": "／",
    ":": "：",
    "?": "？",
    "\"": "”",
    "<": "＜",
    ">": "＞",
    "|": "｜",
    " ": "_",
    "*": "＊"
}


class DownloadVideo(NicoWalker):
    command_name = 'download nicovideo flv'

    def __init__(self, args):
        super(DownloadVideo, self).__init__()
        self.parser.add_argument('vid',
                                 metavar='VID',
                                 help='watch ID or mylist name')
        self.parser.add_argument('-l', '--location',
                                 dest='location',
                                 default='./'.replace("/", os.sep),
                                 help='video output folder')
        self.parser.add_argument('-f', '--force',
                                 dest='overwrite',
                                 action='store_true',
                                 help='allow overwrite')
        self.parser.add_argument('--mp3',
                                 dest='mp3conv',
                                 action='store_true',
                                 help='convert to mp3')
        self.parser.add_argument('-b', '--bitrate',
                                 dest='bitrate',
                                 default=192,
                                 help='mp3 bitrate')
        self.parser.add_argument('-m', '--mylist',
                                 dest='mylist',
                                 action='store_true',
                                 help='download mylist items')
        self.set_parser(args)

    def invoke(self):
        if self.args.mylist:
            mylist_array = MyList.get_mylist_names(self.session)
            mylist_items = GetMyListItems.get_mylist_items(self.args.vid, self.session, mylist_array)
            watch_ids = list(map(lambda mylist_item: mylist_item["item_data"]["watch_id"], mylist_items))
        else:
            watch_ids = [self.args.vid]
        for watch_id in watch_ids:
            # Watch IDがURLで指定された場合、動画IDを抜き出す
            if watch_id.startswith("http"):
                searched = re.search("nicovideo.jp/watch/([a-z0-9]*)", watch_id)
                assert searched is not None, "URL中に動画IDが見つかりませんでした"
                watch_id = searched.groups()[0]
            # 3回失敗するまで繰り返す
            for _ in range(3):
                success = self.download(self.session, watch_id, self.args.location, self.args.overwrite,
                                        self.args.mp3conv, self.args.bitrate)
                if success:
                    # 成功したら終了
                    break
                else:
                    # 失敗したらログインしなおす
                    print("Dispose old session and retry.")
                    self.login(force=True)

    @staticmethod
    def get_video_metadata(session, watch_id):
        # 動画の情報をAPIから取得して、視聴ページを訪問
        # （これをやらないとFLVのURLが取れない）
        api_url = "http://ext.nicovideo.jp/api/getthumbinfo/{0}".format(watch_id)
        api_response_text = session.get(api_url).text
        video_info = nico_xml_parser.parse_video_info(api_response_text)
        session.get(video_info["watch_url"])
        return video_info

    @staticmethod
    def get_download_url(session, video_info, watch_id):
        # ダウンロードURLを取得
        print(video_info["title"], video_info["user_nickname"])
        url = 'http://flapi.nicovideo.jp/api/getflv?v={0}'.format(watch_id)
        text = session.get(url).text
        flv_url = text.split('&')[2].replace('url=', '')
        flv_url = parse.unquote(flv_url)
        return flv_url

    @staticmethod
    def gen_video_path(save_directory, video_info):
        # FLV保存のためのファイル名を決定
        if not save_directory.endswith('/') and not save_directory.endswith(os.sep):
            save_directory += '/'
        # ファイル名に使用不可能の文字列は大文字に置き換える
        video_title = video_info["title"]
        for key, value in character_replace.items():
            if key in video_title:
                video_title = video_title.replace(key, value)
        flv_path = "{0}{1}.{2}".format(save_directory, video_title, video_info["movie_type"])
        flv_path = flv_path.replace("/", os.sep)
        return flv_path

    @staticmethod
    def exec_download(session, flv_url, flv_path, progressbar):
        # ダウンロード＆保存処理開始
        with open(flv_path, 'wb') as f:
            # FLVのURLに対してセッションを開く
            res = session.get(flv_url, stream=True)
            if res.status_code != 200:
                print("Download failed. Status code is {0}.".format(res.status_code))
                return False
            # ファイルサイズ取得
            content_length = res.headers.get("content-length")
            content_length = int(content_length)
            # プログレスバー準備
            division_size = int(content_length / 100)
            downloaded_size = 0
            progressbar.start()
            # ストリーミングで4096bytesずつデータ取得
            for data in res.iter_content(chunk_size=4096):
                downloaded_size += len(data)
                f.write(data)
                # プログレスバーを更新
                try:
                    progressbar.update(int(downloaded_size / division_size))
                except OSError:
                    pass
            progressbar.finish()
            print('Saved as {0}'.format(flv_path))
        return True

    @staticmethod
    def convert_mp3(video_info, flv_path, mp3_bitrate, leave_flv=False):
        mp3_path = flv_path[:flv_path.rfind(".")] + ".mp3"
        print(mp3_path)
        command = 'ffmpeg -y -i "{0}" -ab {1}k "{2}"'.format(flv_path, mp3_bitrate, mp3_path)
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("ffmpegの実行に失敗しました。")
            exit(-1)
        mp3_tag.add_tag(
            mp3_path,
            video_info["thumbnail_url"],
            video_info["title"],
            video_info["user_nickname"],
            "ニコニコ動画"
        )
        # mp3ファイルが存在したら元のファイルを削除
        if leave_flv is False and os.path.exists(mp3_path):
            os.remove(flv_path)

    @staticmethod
    def download(session, watch_id, save_directory, overwrite=False, convert_mp3=False, mp3_bitrate="192"):
        if convert_mp3:
            try:
                subprocess.run("ffmpeg -version", shell=True, check=True, stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print("ffmpegが実行できません。ffmpegがインストールされ、PATHに含まれているか確認してください。\n"
                      "インストールする場合、 https://www.ffmpeg.org/download.html を参照してください。")
                exit(-1)
        video_info = DownloadVideo.get_video_metadata(session, watch_id)
        flv_url = DownloadVideo.get_download_url(session, video_info, watch_id)
        flv_path = DownloadVideo.gen_video_path(save_directory, video_info)
        # ファイルが存在したら終了
        if not overwrite and os.path.exists(flv_path):
            print("ファイルが存在します。上書きする場合は --overwrite オプションを指定してください。")
            return True
        # ダウンロード実行
        widgets = ["Downloading: ", Percentage(), Bar(), ETA()]
        progressbar = ProgressBar(maxval=100, widgets=widgets)
        if not DownloadVideo.exec_download(session, flv_url, flv_path, progressbar):
            return False
        # mp3へ変換
        if convert_mp3:
            DownloadVideo.convert_mp3(video_info, flv_path, mp3_bitrate)
        return True


if __name__ == '__main__':
    DownloadVideo(None).invoke()

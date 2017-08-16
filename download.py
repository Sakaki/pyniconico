#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from urllib import parse
import os
from tools import nico_xml_parser
from tools.nicowalker import NicoWalker
from mylist_items import GetMyListItems
from mylist import MyList
from progressbar import ProgressBar, Percentage, Bar, ETA
from subprocess import run
from tools import mp3_tag

character_replace = {
    "\\": "＼",
    "/": "／",
    ":": "：",
    "?": "？",
    "\"": "”",
    "<": "＜",
    ">": "＞",
    "|": "｜",
    " ": "_"
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
    def download(session, watch_id, save_directory, overwrite=False, convert_mp3=False, mp3_bitrate="192"):
        # 動画の情報をAPIから取得して、視聴ページを訪問
        # （これをやらないとFLVのURLが取れない）
        api_url = "http://ext.nicovideo.jp/api/getthumbinfo/{0}".format(watch_id)
        api_response_text = session.get(api_url).text
        video_info = nico_xml_parser.parse_video_info(api_response_text)
        session.get(video_info["watch_url"])
        url = 'http://www.nicovideo.jp/watch/{0}'.format(watch_id)
        session.get(url)

        # ダウンロードURLを取得
        print(video_info["title"], video_info["user_nickname"])
        url = 'http://flapi.nicovideo.jp/api/getflv?v={0}'.format(watch_id)
        text = session.get(url).text
        flv_url = text.split('&')[2].replace('url=', '')
        flv_url = parse.unquote(flv_url)

        # FLV保存のためのファイル名を決定
        if not save_directory.endswith('/'):
            save_directory += '/'
        # ファイル名に使用不可能の文字列は大文字に置き換える
        video_title = video_info["title"]
        for key, value in character_replace.items():
            if key in video_title:
                video_title = video_title.replace(key, value)
        flv_path = "{0}{1}.{2}".format(save_directory, video_title, video_info["movie_type"])
        flv_path = flv_path.replace("/", os.sep)
        if not overwrite and os.path.exists(flv_path):
            print("File exists. Skipping...")
            return True

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
            widgets = ["Downloading: ", Percentage(), Bar(), ETA()]
            progressbar = ProgressBar(maxval=100, widgets=widgets).start()
            # ストリーミングで4096bytesずつデータ取得
            for data in res.iter_content(chunk_size=4096):
                downloaded_size += len(data)
                f.write(data)
                # プログレスバーを更新
                progressbar.update(int(downloaded_size / division_size))
            progressbar.finish()
            print('Saved as {0}'.format(flv_path))
        # mp3へ変換
        if convert_mp3:
            mp3_path = "{0}{1}.{2}".format(save_directory, video_title, "mp3")
            mp3_path = mp3_path.replace("/", os.sep)
            command = 'ffmpeg -y -i "{0}" -ab {1}k "{2}"'.format(flv_path, mp3_bitrate, mp3_path)
            run(command, shell=True)
            mp3_tag.add_tag(mp3_path,
                            video_info["thumbnail_url"] + ".L",
                            video_info["title"],
                            video_info["user_nickname"],
                            "ニコニコ動画")
        return True


if __name__ == '__main__':
    DownloadVideo(None).invoke()

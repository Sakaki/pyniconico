# pyniconico

ニコニコ動画をpythonから扱うツールです。

## 機能

pyniconicoの実行スクリプト一覧です。

 * download.py : 動画をダウンロードする
 * mylist.py : マイリスト一覧を取得する
 * mylist_items.py : マイリストの動画ID一覧を抜き出す

## インストール

pipでprogressbar2, requests, eyed3, argparseを入れてください。

## 使い方

各コマンドの使い方は--helpを参照してください。

```
$ ./download.py --help
usage: downloadflv.py [-h] [-u MAIL] [-p PASSWD] [-l LOCATION] [-f] [--mp3]
                      [-b BITRATE]
                      VID

download niconico flv

positional arguments:
  VID                   video id

optional arguments:
  -h, --help            show this help message and exit
  -u MAIL, --username MAIL
                        username
  -p PASSWD, --password PASSWD
                        password
  -l LOCATION, --location LOCATION
                        video output folder
  -f, --force           allow overwrite
  --mp3                 convert to mp3
  -b BITRATE, --bitrate BITRATE
                        mp3 bitratesage: downloadflv.py [-h] [-u MAIL] [-p PASSWD] [-o LOCATION] [-f] VID
```

## サンプル

例えばtestというマイリストにある動画を全てダウンロードしたい場合は、

```
$ for id in `python getmylistsongs.py --raw -n test`
> do python downloadflv.py $id
> done
```

のような方法で実現できます。

## ログイン

ホームディレクトリに.netrcファイル(~/.netrc)を用意することでユーザー名及びパスワード入力を省略することができます。

```
machine   nicovideo
login     someone@example.com
password  testpasswd
```

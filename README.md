# pyniconico

ニコニコ動画をpythonから扱うツールです。

## 機能

pyniconicoの実行スクリプト一覧です。

 * getmylist.py : マイリスト一覧を取得する 
 * getmylistsongs.py : マイリストの動画ID一覧を抜き出す 
 * downloadflv.py : 動画をダウンロードする 

## インストール

progressbarとeyed3が必要です。ない場合はpipなどでインストールしてください。

## 使い方

各コマンドの使い方は--helpを参照してください。

```
$ ./downloadflv.py --help
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
> do ./downloadflv.py $id
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


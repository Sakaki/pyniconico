#pyniconico#

ニコニコ動画をpythonから扱うツールです。

##機能##

pyniconicoの主な機能です。

 * マイリスト一覧を取得する (getmylist.py)
 * マイリストの動画ID一覧を抜き出す機能 (getmylistsongs.py)
 * 動画をダウンロードする機能 (downloadflv.py)

##インストール##

pycurlとargparseが必要です。ない場合はeasy_installやpipでインストールしてください。

##使い方##

各コマンドの使い方は--helpで参照してください。

```
$ python downloadflv.py --help
usage: downloadflv.py [-h] [-u MAIL] [-p PASSWD] [-o LOCATION] [-f] VID

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
                        video output
  -f, --force           allow overwrite
  ```

##サンプル##

例えばtestというマイリストにある動画を全てダウンロードしたい場合は、

```
$ for id in `python getmylistsongs.py --raw -n test`
> do python downloadflv.py $id
> done
```

のような方法で実現できます。

##ログイン##

ホームディレクトリに.netrcファイル(~/.netrc)を用意することでユーザー名及びパスワード入力を省略することができます。

```
machine   nicovideo
login     someone@example.com
password  testpasswd
```

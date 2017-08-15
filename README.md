# pyniconico

ニコニコ動画をpythonから扱うツールです。

サーバーに負荷をかけない常識の範囲内でお使いください。

## 機能

 * download.py : 動画をダウンロードする
 * mylist.py : マイリスト一覧を取得する
 * mylist_items.py : マイリストの動画ID一覧を抜き出す

## インストール

Python 3で動作します（Python 3.5.2で動作を確認）。

pipでprogressbar2, requests, eyed3, argparseを入れてください。

## 使い方

```
$ python download.py -u someone@mail.com -p password sm31606995
ハチ MV「砂の惑星 feat.初音ミク」 ハチ
Downloading: 100%|#######################################################################################|Time: 0:00:09
Saved as ./ハチ_MV「砂の惑星_feat.初音ミク」.mp4
```

## ログイン

ホームディレクトリに以下のような.netrcファイル(~/.netrc)を用意することで、ユーザー名及びパスワード入力を省略することができます。

```
machine   nicovideo
login     someone@mail.com
password  testpasswd
```

## まとめてダウンロード

download.pyにはマイリストからまとめて動画をダウンロードする機能が付いています。

```
$ python download.py -u someone@mail.com -p password -m ボカロ
【波音リツキレ音源】心做し 【UTAUカバー】 cillia
Downloading: 100%|#######################################################################################|Time: 0:00:03
Saved as ./ボカロ5/【波音リツキレ音源】心做し_【UTAUカバー】.mp4
【初音ミク】 声 【オリジナルPV】 はりー
Downloading: 100%|#######################################################################################|Time: 0:00:16
Saved as ./ボカロ5/【初音ミク】_声_【オリジナルPV】.mp4
【初音ミク】 Initial Song 【オリジナルMV】 40mP
Downloading: 100%|#######################################################################################|Time: 0:00:14
Saved as ./ボカロ5/【初音ミク】_Initial_Song_【オリジナルMV】.mp4
```

そのほかの機能は各ファイルの--helpを参照してください。

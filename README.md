# pyniconico

ニコニコ動画をpythonから扱うツールです。

サーバーに負荷をかけない範囲でお使いください。

## 機能

 * download.py : 動画をダウンロードする
 * mylist.py : マイリスト一覧を取得する
 * mylist_items.py : マイリストの動画ID一覧を抜き出す
 * gui.py : 簡易的なGUIインターフェースです

## 動作環境

OS: Linux, MacOS, Windows (Windowsではnetrcが動きません)

アーキテクチャ: モジュールが入ればどれでも

## インストール

Python 3で動作します（Python 3.4.4で動作を確認）。

モジュールのインストールはrequirements.txtを使ってください。

```
$ pip install -r requirements.txt
```

## 使い方

### CLI (nicovideo_dl.py)

```
$ python nicovideo_dl.py -u someone@mail.com -p password sm31606995
ハチ MV「砂の惑星 feat.初音ミク」 ハチ
Downloading: 100%|#######################################################################################|Time: 0:00:09
Saved as ./ハチ_MV「砂の惑星_feat.初音ミク」.mp4
```

### GUI (gui.py)

![nicovideo_dl](https://user-images.githubusercontent.com/980141/29416522-5452b716-83a1-11e7-9372-379a0f72bb9e.png)

```
$ python gui.py
```

で起動します。初回はユーザー名、パスワード、URLまたは動画IDをすべて入力する必要があります。

2回目以降はクッキーを用いてログインを試み、成功した場合はユーザー名やパスワードの入力なしでもダウンロードができます。

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
$ python nicovideo_dl.py -u someone@mail.com -p password -m ボカロ
【波音リツキレ音源】心做し 【UTAUカバー】 cillia
Downloading: 100%|#######################################################################################|Time: 0:00:03
Saved as ./【波音リツキレ音源】心做し_【UTAUカバー】.mp4
【初音ミク】 声 【オリジナルPV】 はりー
Downloading: 100%|#######################################################################################|Time: 0:00:16
Saved as ./【初音ミク】_声_【オリジナルPV】.mp4
【初音ミク】 Initial Song 【オリジナルMV】 40mP
Downloading: 100%|#######################################################################################|Time: 0:00:14
Saved as ./【初音ミク】_Initial_Song_【オリジナルMV】.mp4
```

そのほかの機能は各ファイルの--helpを参照してください。

## mp3への変換

ffmpegが入っていればその場でmp3に変換することもできます。

その際、タグやカバーアートは自動で入ります。

```
$ python nicovideo_dl.py -u someone@mail.com -p password --mp3 sm31606995
ハチ MV「砂の惑星 feat.初音ミク」 ハチ
...
$ eyeD3 ハチ_MV「砂の惑星_feat.初音ミク」.mp3
/path/to/dir/ハチ_MV「砂の惑星_feat.初音ミク」.mp3       [ 5.49 MB ]
-------------------------------------------------------------------------------
Time: 03:59     MPEG1, Layer III        [ 192 kb/s @ 44100 Hz - Stereo ]
-------------------------------------------------------------------------------
ID3 v2.3:
title: ハチ MV「砂の惑星 feat.初音ミク」
artist: ハチ
album: ニコニコ動画
album artist: None
track:
UserTextFrame: [Description: minor_version]
1
UserTextFrame: [Description: major_brand]
isom
UserTextFrame: [Description: compatible_brands]
isom
FRONT_COVER Image: [Size: 9143 bytes] [Type: image/jpeg]
Description: Cover

-------------------------------------------------------------------------------
```

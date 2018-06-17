# pyniconico

ニコニコ動画のダウンロードやマイリスト取得が行えるPython製のツールです。

サーバーに過度の負荷をかけない範囲でお使いください。

## 使い方

python >= 3.5

Google ChromeかFirefoxのいずれかをインストールしてください（デフォルトではChromeが使用されます）。

```bash
$ pip install pyniconico
$ nicopy -u username -p password download sm32831006
sm32831006
ゆるキャン△にハマるマン しめさば
Downloading: 100%|#######################################################################|Time: 0:00:24
Saved as .\ゆるキャン△にハマるマン.mp4
```

もしくは、

```bash
git clone https://github.com/Sakaki/pyniconico.git
cd pyniconico
pip install -r requirements.txt
python niconico.py -u username -p password download sm32831006
```

動画IDの部分はURLを指定することも可能です（URLはダブルクォートなりで囲って指定してください）。

ホームディレクトリに.netrcファイル(~/.netrc)を用意することで、ユーザー名及びパスワード入力を省略することができます。

```bash
$ cat ~/.netrc
machine   nicovideo
login     （ログインID）
password  （パスワード）
$ chmod 600 ~/.netrc
$ nicopy download sm32831006
```

FirefoxをWebDriverとして使用する場合、

```bash
nicopy -d firefox download sm32831006
```

PhantomJSをWebDriverとして使用する場合、

```bash
nicopy -d phantomjs download sm32831006
```

※現在、PhantomJSを使用することは非推奨となっています。

### Dockerで実行

.env ファイルを作成してdocker-composeコマンドを実行してください。

```env
$ cat .env
driver=firefox
username=（ログインID）
password=（パスワード）

$ docker-compose run download sm32831006
$ docker-compose run mylist
$ docker-compose run mylist_items
```

### mp3に変換

ffmpegをインストールし、実行可能となっている（PATHに登録されている）必要があります。

```bash
$ nicopy download --mp3 sm31606995
sm31606995
ハチ MV「砂の惑星 feat.初音ミク」 ハチ
Downloading: 100%|#######################################################################|Time: 0:00:22
Saved as .\ハチ_MV「砂の惑星_feat.初音ミク」.mp4
.\ハチ_MV「砂の惑星_feat.初音ミク」.mp3
...
```

### マイリスト一覧

```bash
$ nicopy mylist
マジミラ2017 59835789
けものフレンズ 58720332
みんなの愛したゆゆ式 58076939
...
```

### マイリスト動画一覧

```bash
$ nicopy mylist_items マジミラ2017
マジミラ2017:
  sm1587618
  sm26470008
  sm28974414
  sm31401854
...
```

### マイリストからダウンロード

```bash
$ nicopy download --mylist ボカロ
ボカロ
【波音リツキレ音源】心做し 【UTAUカバー】 cillia
Downloading: 100%|#######################################################################|Time: 0:00:03
Saved as ./【波音リツキレ音源】心做し_【UTAUカバー】.mp4
【初音ミク】 声 【オリジナルPV】 はりー
Downloading: 100%|#######################################################################|Time: 0:00:16
Saved as ./【初音ミク】_声_【オリジナルPV】.mp4
【初音ミク】 Initial Song 【オリジナルMV】 40mP
Downloading: 100%|#######################################################################|Time: 0:00:14
Saved as ./【初音ミク】_Initial_Song_【オリジナルMV】.mp4
...
```

## 動作環境

|OS / ブラウザ|Chrome|Firefox|PhantomJS|
|---|---|---|---|
|Windows|64bit / 32bit|64bit / 32bit|64bit / 32bit|
|Linux|64bit|64bit / 32bit|64bit / 32bit|
|macOS|64bit|||

※Windowsではnetrcが動きません

## GUI (gui.py)

ニコニコ動画のログインシステムが刷新され、gui.pyのメンテナンスが追い付いていません。

恐らく動かないと思いますので、改善されるまでしばらくお待ちください・・・

---

```bash
$ pip install requirements_gui.txt
$ python gui.py
```

で起動します。初回はユーザー名、パスワード、URLまたは動画IDをすべて入力する必要があります。

![nicovideo_dl](https://user-images.githubusercontent.com/980141/29494124-72a2b4d4-85de-11e7-894d-9112dbac6e03.png)

2回目以降はクッキーを用いてログインを試み、成功した場合はユーザー名やパスワードの入力なしでもダウンロードができます。

### まとめてダウンロード

マイリスト一括ダウンロードの「選択」ボタンを押してください。

![nicovideo_dl_mylist](https://user-images.githubusercontent.com/980141/29494138-a967c586-85de-11e7-91f5-d125775ae09e.png)

### mp3変換

設定ボタンからmp3変換を有効にし、ビットレートを調整してください。

![nicovideo_dl_settings](https://user-images.githubusercontent.com/980141/29494148-d805f75a-85de-11e7-8cfd-02e5635f4025.png)

## ライセンス

pyniconicoのソースコードのライセンスについては、LICENSEファイルを参照してください。

また、selenimuのWebDriverとしてChromeDriver・geckodriver・PhantomJSを自動的にダウンロードします。

ライセンスについては、それぞれ以下のようになっています。

|WebDriver|Webサイト|ライセンス|
|---|---|---|
|ChdomeDriver|http://chromedriver.chromium.org/|明記無し|
|geckodriver|https://github.com/mozilla/geckodriver|Mozilla Public License Version 2.0|
|PhantomJS|http://phantomjs.org/download.html|BSD license|

WebDriverは nico_tools/download 以下にダウンロードされます。

各ディレクトリにライセンスファイルを配置していますので、そちらもご参照ください。

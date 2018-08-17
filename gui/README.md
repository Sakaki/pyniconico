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

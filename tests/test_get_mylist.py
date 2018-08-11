from unittest import TestCase
import netrc
from niconico import NicoVideoArgs
from nico_tools.mylist import MyList


class TestGetMyList(TestCase):

    def setUp(self):
        # ログイン情報はnetrcから取る
        auth = netrc.netrc()
        # TODO: web_driverをPhantomJSから変更する
        self.username, _, self.password = auth.authenticators("nicovideo")

    def test_get_mylist(self):
        # マイリスト取れて、とりあえずマイリストがあればテスト通過とする
        arguments_dict = {
            "mail": self.username,
            "password": self.password,
            "web_driver": "phantomjs"
        }
        arguments = NicoVideoArgs(arguments_dict)
        mylist = MyList(arguments)
        mylist_names = mylist.get_mylist_names(mylist.session)
        print(mylist_names)
        self.assertEqual(type(mylist_names), list)
        self.assertTrue(len(mylist_names) > 0)
        self.assertTrue("とりあえずマイリスト" in [item["name"] for item in mylist_names])

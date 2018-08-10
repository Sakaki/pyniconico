from unittest import TestCase
import netrc
from niconico import NicoVideoArgs
from nico_tools.mylist_items import GetMyListItems

test_mylist_name = "とりあえずマイリスト"


class TestGetMyListItem(TestCase):

    def setUp(self):
        # ログイン情報はnetrcから来る
        auth = netrc.netrc()
        # TODO: web_driverをPhantomJSから変更する
        self.username, _, self.password = auth.authenticators("nicovideo")

    def test_get_mylist(self):
        # とりあえずマイリストの動画IDが何か取れればOK
        arguments_dict = {
            "mail": self.username,
            "password": self.password,
            "web_driver": "phantomjs"
        }
        arguments = NicoVideoArgs(arguments_dict)
        mylist_object = GetMyListItems(arguments)
        mylist_items = mylist_object.get_mylist_items(
            test_mylist_name,
            mylist_object.session,
            mylist_object.mylist_array
        )
        self.assertTrue(len(mylist_items) > 0)
        self.assertTrue(len(mylist_items[0]["item_data"]["watch_id"]) > 0)

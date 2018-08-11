from unittest import TestCase
import netrc
from nico_tools.nicowalker import NicoWalker


class TestLogin(TestCase):

    def setUp(self):
        # ログイン情報はnetrcから取る
        auth = netrc.netrc()
        # TODO: web_driverをPhantomJSから変更する
        self.username, _, self.password = auth.authenticators("nicovideo")

    def test_login(self):
        nicowalker = NicoWalker()
        nicowalker.mail = self.username
        nicowalker.password = self.password
        nicowalker.login(force=True)
        self.assertTrue(nicowalker.is_logged_in())

    def test_load_session(self):
        nicowalker = NicoWalker()
        nicowalker.load_cookies()
        self.assertTrue(nicowalker.is_logged_in())

from unittest import TestCase
import netrc
from nico_tools.nicowalker import NicoWalker
import tests


class TestLogin(TestCase):

    def setUp(self):
        # ログイン情報はnetrcから取る
        auth = netrc.netrc()
        self.username, _, self.password = auth.authenticators("nicovideo")

    def test_login(self):
        nicowalker = NicoWalker()
        nicowalker.mail = self.username
        nicowalker.password = self.password
        nicowalker.web_driver = tests.test_driver
        nicowalker.login(force=True)
        self.assertTrue(nicowalker.is_logged_in())

    def test_load_session(self):
        nicowalker = NicoWalker()
        nicowalker.load_cookies()
        self.assertTrue(nicowalker.is_logged_in())

# -*- coding:utf-8 -*-

import argparse
import json
from os import path
import requests
import pickle
import netrc
import os
from nico_tools import web_drivers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

working_dir = path.dirname(path.abspath(__file__))
cookie_path = "{0}/{1}".format(working_dir, "cookie.bin")
cookie_path = cookie_path.replace("/", os.sep)


class NicoWalker(object):
    command_name = "Default Command"
    available_drivers = {
        "phantomjs": web_drivers.PhantomJSDriver,
        "chrome": web_drivers.ChromeDriver,
        "firefox": web_drivers.GeckoDriver
    }

    def __init__(self):
        self.parser = argparse.ArgumentParser(description=self.command_name)
        self.parser.add_argument('-u', '--username',
                                 dest='mail',
                                 default=None,
                                 help='username')
        self.parser.add_argument('-p', '--password',
                                 dest='passwd',
                                 default=None,
                                 help='password')
        self.parser.add_argument('-d', '--driver',
                                 dest='web_driver',
                                 default='phantomjs',
                                 help='password')
        self.mail = None
        self.password = None
        self.args = None
        self.web_driver = None
        self.session = requests.Session()

    def set_parser(self, args=None):
        if args is None:
            args = self.parser.parse_args()
        self.args = args
        # セッションが保存されていた場合、それを使う
        if path.exists(cookie_path):
            self.load_cookies()
            # ログインできていたらリターン
            if self.is_logged_in():
                return
        mail = args.mail
        password = args.passwd

        # ユーザー名とパスワードをnetrcから取得
        if mail is None or password is None:
            try:
                auth = netrc.netrc()
                mail, _, password = auth.authenticators("nicovideo")
            except OSError as e:
                print(e)
                raise LoginFailedException("ログインに失敗しました")
        # ログインしてセッションを取得
        self.mail = mail
        self.password = password
        self.web_driver = args.web_driver
        self.login()

    def login(self, force=False):
        # セッションが保存されていた場合、それを使う
        if path.exists(cookie_path) and not force:
            self.load_cookies()
            # ログインできていたらリターン
            if self.is_logged_in():
                return
        web_driver_object = NicoWalker.available_drivers.get(self.web_driver, None)
        if web_driver_object is None:
            print("指定されたWebDriverが見つかりませんでした。\n"
                  "phantomjs, chrome, firefoxのいずれかを指定してください。")
            exit(-1)
        driver = web_driver_object().get_driver()
        login_page_url = "https://account.nicovideo.jp/login"
        driver.get(login_page_url)
        WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.ID, "login__submit")))
        mail = driver.find_element_by_id('input__mailtel')
        password = driver.find_element_by_id('input__password')
        submit = driver.find_element_by_id("login__submit")
        mail.send_keys(self.mail)
        password.send_keys(self.password)
        submit.submit()
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
            (By.ID, "siteHeaderUserNickNameContainer")))
        mylist_url = "http://www.nicovideo.jp/api/deflist/list"
        driver.get(mylist_url)
        # cookieを保存
        for cookie in driver.get_cookies():
            self.session.cookies.set(cookie['name'], cookie['value'])
        if self.is_logged_in():
            # クッキーを保存
            self.save_cookies()
        else:
            raise LoginFailedException("ログインに失敗しました")

    def load_cookies(self):
        with open(cookie_path, "rb") as f:
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            self.session.cookies = cookies

    def save_cookies(self):
        with open(cookie_path, "wb") as f:
            pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

    # とりあえずマイリストにアクセスしてログイン状態を確認
    # TODO もうちょっとカジュアルな確認方法を探す
    def is_logged_in(self):
        url = 'http://www.nicovideo.jp/api/deflist/list'
        res = self.session.get(url)
        res_json = json.loads(res.text)
        if res_json["status"] == "ok":
            return True
        else:
            return False


class LoginFailedException(Exception):
    pass

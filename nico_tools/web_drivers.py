# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import platform
import requests
import os
import zipfile
import tarfile
import json
import stat

with open("{}/web_drivers.json".format(os.path.dirname(os.path.abspath(__file__)))) as f:
    driver_json = json.loads(f.read())


# WebDriverのスーパークラス
class WebDriver:
    # OS・アーキテクチャごとのDL情報
    driver_info = {}
    # DLや解凍するWebDriverのファイルの保存ディレクトリ
    working_directory = "/download"

    # パス中の/は全てos.sepで置換
    def __init__(self):
        current_abs_directory = os.path.dirname(os.path.abspath(__file__))
        # 絶対パスに変換
        self.working_directory = (current_abs_directory + self.working_directory).replace("/", os.sep)
        # OSやアーキテクチャの情報を取得
        self.system = platform.system()
        self.machine = platform.architecture()[0]
        platform_driver = self.driver_info.get(self.system).get(self.machine)
        # WebDriverのダウンロードURLを取得
        self.driver_url = platform_driver.get("download_url")
        # 実行ファイルのパスを絶対パスに変換
        self.execute_path = (current_abs_directory + platform_driver.get("path")).replace("/", os.sep)
        # DL対象ファイル名
        self.archive_path = "{0}/{1}".format(self.working_directory, "archive").replace("/", os.sep)
        # DL実行
        self.download()
        # DLしたらファイルを解凍
        if not os.path.exists(self.execute_path):
            self.extract()

    # WebDriverのアーカイブをダウンロード
    def download(self):
        # もしファイルが存在したらスキップ
        if os.path.exists(self.archive_path):
            return
        print("WebDriverを取得しています。")
        raw = requests.get(self.driver_url, stream=True)
        with open(self.archive_path, "wb") as f:
            for chunk in raw.iter_content(chunk_size=128):
                f.write(chunk)
        print("WebDriverの取得が完了しました。")

    # DLしたファイルを解凍
    def extract(self):
        pass

    # zipファイルの解凍
    def extract_zip(self):
        with zipfile.ZipFile(self.archive_path) as archive_zip:
            archive_zip.extractall(self.working_directory)

    # tarファイルの解凍
    def extract_tar(self):
        with tarfile.open(self.archive_path) as archive_tar:
            archive_tar.extractall(self.working_directory)

    # ドライバを生成
    def generate_driver(self):
        return None

    # エラーに気を付けながらドライバを取得
    def get_driver(self):
        driver = None
        try:
            driver = self.generate_driver()
        except WebDriverException as e:
            print("WebDriver(PhantomJS)を作成することができませんでした。 {}".format(e))
            exit(-1)
        return driver


class PhantomJSDriver(WebDriver):
    driver_info = driver_json.get("PhantomJS")
    driver_info["Windows"]["32bit"] = driver_info["Windows"]["64bit"]
    working_directory = "/download/PhantomJS"

    def extract(self):
        if self.system == "Windows":
            self.extract_zip()
        elif self.system == "Linux":
            self.extract_tar()

    def generate_driver(self):
        return webdriver.PhantomJS(self.execute_path)


class GeckoDriver(WebDriver):
    driver_info = driver_json.get("GeckoDriver")
    working_directory = "/download/geckodriver"

    def extract(self):
        if self.system == "Windows":
            self.extract_zip()
        elif self.system == "Linux":
            self.extract_tar()

    def generate_driver(self):
        options = FirefoxOptions()
        options.add_argument("-headless")
        return webdriver.Firefox(executable_path=self.execute_path, options=options)


class ChromeDriver(WebDriver):
    driver_info = driver_json.get("ChromeDriver")
    working_directory = "/download/ChromeDriver"

    def extract(self):
        self.extract_zip()
        if self.system in {"Linux", "Darwin"}:
            os.chmod(self.execute_path, stat.S_IRWXU)

    def generate_driver(self):
        options = ChromeOptions()
        options.add_argument("--headless")
        return webdriver.Chrome(self.execute_path, options=options)


if __name__ == "__main__":
    phantom_js = PhantomJSDriver()

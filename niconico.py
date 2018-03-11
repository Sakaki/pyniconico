# -*- coding:utf-8 -*-

import click
from nicovideo_dl import DownloadVideo


class NicoVideoArgs:
    def __init__(self, argument_dict):
        self.vid = argument_dict.get("video_id")
        self.location = argument_dict.get("location")
        self.overwrite = argument_dict.get("overwrite")
        self.mp3conv = argument_dict.get("convert_mp3")
        self.bitrate = argument_dict.get("bit_rate")
        self.mylist = argument_dict.get("my_list")
        self.mail = argument_dict.get("mail")
        self.passwd = argument_dict.get("password")


@click.group()
@click.option("--username", prompt="Please input your username/email", help="username/email")
@click.option("--password", prompt="Please input your password", hide_input=True, help="password")
@click.pass_context
def niconico(context, username, password):
    context.obj["username"] = username
    context.obj["password"] = password


@niconico.command()
@click.argument('video_id')
@click.pass_context
def download(context, video_id):
    print(video_id)
    arguments_dict = {
        "video_id": video_id,
        "location": "./",
        "overwrite": False,
        "convert_mp3": False,
        "bit_rate": 192,
        "my_list": False,
        "mail": context.obj.get("username"),
        "password": context.obj.get("password")
    }
    arguments = NicoVideoArgs(arguments_dict)
    DownloadVideo(arguments).invoke()


if __name__ == '__main__':
    niconico(obj={})

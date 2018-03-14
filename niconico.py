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
@click.option("--username", "-u", prompt="Please input your username/email", help="username/email")
@click.option("--password", "-p", prompt="Please input your password", hide_input=True, help="password")
@click.pass_context
def niconico(context, username, password):
    context.obj["username"] = username
    context.obj["password"] = password


@niconico.command()
@click.argument('video_id')
@click.option("--location", "-l", default="./", help="Download directory", type=click.Path(
    exists=True, file_okay=False, dir_okay=True, writable=True))
@click.option("--overwrite", help="Overwrite", is_flag=True)
@click.option("--mp3", help="Convert video to mp3 (requires ffmpeg in PATH)", is_flag=True)
@click.option("--bit_rate", "-b", default=192, help="mp3 bit rate (kbps, default: 192)", type=int)
@click.pass_context
def download(context, video_id, location, overwrite, mp3, bit_rate):
    print(video_id)
    arguments_dict = {
        "video_id": video_id,
        "location": location,
        "overwrite": overwrite,
        "convert_mp3": mp3,
        "bit_rate": bit_rate,
        "my_list": False,
        "mail": context.obj.get("username"),
        "password": context.obj.get("password")
    }
    arguments = NicoVideoArgs(arguments_dict)
    DownloadVideo(arguments).invoke()


if __name__ == '__main__':
    niconico(obj={})

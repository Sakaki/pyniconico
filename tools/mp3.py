# -*- coding:utf-8 -*-

import os, eyed3, re
from commands import getoutput

def convert(infile, bitrate, author, title, album='niconico'):
    outfile = infile.replace(infile[-4:], '.mp3')
    coverart = infile.replace(infile[-4:], '.jpg')

    os.system('ffmpeg -y -i "{0}" -ab {1}k "{2}"'.format(infile, bitrate, outfile))

    w, h = getSize(infile)
    startpos = (w-h)/2
    ffstr = 'ffmpeg -ss 50 -y -i "{3}" -vframes 1 -vf crop={0}:{0}:{1}:{2} -f image2 "{4}"'
    os.system(ffstr.format(h, startpos, 0, infile, coverart))

    audiotag = eyed3.load(outfile.decode('utf-8'))
    audiotag.tag.version = (2, 3, 0)
    audiotag.tag.artist = author.decode('utf-8')
    audiotag.tag.album = album.decode('utf-8')
    audiotag.tag.title = title.decode('utf-8')
    with open(coverart, 'rb') as f:
        image = f.read()
    audiotag.tag.images.set(3, image, 'image/jpeg',u'made by ffmpeg')
    audiotag.tag.save()

    os.remove(coverart)

def getSize(filename):
    videoinf = getoutput('ffmpeg -y -i "{0}"'.format(filename))
    cropline = re.search('[1-9][0-9]*x[1-9][0-9]*', videoinf)
    pos = cropline.group(0).split('x')
    width = int(pos[0])
    height = int(pos[1])

    return width, height

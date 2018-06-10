import requests
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from mutagen.id3 import ID3NoHeaderError
from PIL import Image
from io import BytesIO


def add_tag(file_path, thumbnail_url, title, artist, album):
    try:
        tags = ID3(file_path)
    except ID3NoHeaderError:
        print("Adding ID3 header.")
        tags = ID3()
    retry = 3
    while retry >= 0:
        try:
            thumbnail_url_large = thumbnail_url + ".L"
            coverart_page = requests.get(thumbnail_url_large)
            if coverart_page.status_code == 404:
                coverart_page = requests.get(thumbnail_url)
            if coverart_page.status_code != 404:
                jpeg_file = BytesIO(coverart_page.content)
                image_processor = Image.open(jpeg_file)
                size = image_processor.size
                smaller, larger = size if size[0] < size[1] else size[::-1]
                box = ((larger-smaller)/2, 0, (larger-smaller)/2+smaller, smaller)
                cropped = image_processor.crop(box)
                temp = BytesIO()
                cropped.save(temp, format="JPEG")
                temp.seek(0)
                coverart = temp.read()
                tags["APIC:"] = APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3,
                    desc='Cover',
                    data=coverart
                )
            if title is not None:
                tags["TIT2"] = TIT2(encoding=3, text=title)
            if artist is not None:
                tags["TPE1"] = TPE1(encoding=3, text=artist)
            if album is not None:
                tags["TALB"] = TALB(encoding=3, text=album)
            break
        except requests.ConnectionError as e:
            print(e)
            retry -= 1
    tags.save(file_path, v1=0, v2_version=3)

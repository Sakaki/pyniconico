#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='pyniconico',
    version='1.3',
    description='Python NicoNico Douga downloader',
    long_description='Please read ./README.md',
    author='Sakaki Mirai',
    author_email='sakaki333@gmail.com',
    url='https://github.com/Sakaki/pyniconico',
    license='Written in ./LICENSE for this project. But please be careful this project download external programs.',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'progressbar2',
        'requests',
        'mutagen',
        'pillow',
        'argparse',
        'selenium',
        'beautifulsoup4',
        'click'
    ],
    py_modules=['niconico'],
    entry_points='''
        [console_scripts]
        nicopy=niconico:main
    ''',
    package_data={
        'nico_tools': [
            'web_drivers.json',
            'download/ChromeDriver/README.md',
            'download/geckodriver/mpl-v2.0.md',
            'download/PhantomJS/LICENSE.BSD'
        ]
    },
)

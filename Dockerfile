FROM python:3-alpine

WORKDIR /usr/src/app

RUN apk update && \
    apk add python firefox-esr fontconfig ttf-freefont dbus-x11
RUN apk add zlib-dev jpeg-dev gcc make libc-dev linux-headers

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir /download

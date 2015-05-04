#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import wget
from bs4 import BeautifulSoup

def get_name(tag):
    divs = tag.find_all("div")
    for dv in divs:
        if "class" in dv.attrs and "Name" in dv["class"]:
            return dv.strings.next().encode('utf-8')

    print >> sys.stderr,"Name Not Found:", tag
    exit(1)

def get_image_url(tag):
    imgs = tag.find_all("img")
    for img in imgs:
        if "src" in img.attrs and img["src"][-3:]=="jpg":
            return img["src"]

    print >> sys.stderr, "Image Not Found:", tag
    exit(1)

URL="http://sp.senkyo.mainichi.jp/giin/list.html?p="
memnum = 0

def get_image_from_page(page, f):
    global memnum
    url=URL+str(page)
    response = urllib2.urlopen(url)
    html = response.read()

    soup = BeautifulSoup(html)

    tags = soup.find_all('a')
    for tag in tags:
        if "class" in tag.attrs and "ContentsDataLink" in tag["class"]:
            memnum += 1
            m_id = str(memnum).zfill(3)
            name    = get_name(tag)
            img_url = get_image_url(tag)
            img = wget.download(img_url, out="./img/"+m_id+".jpg")
            print m_id,": ",name
            print >>f, m_id,": ",name


def main():
    with open("list.txt", "w") as f:
        for p in range(36):
            get_image_from_page(p+1, f)

if __name__ == '__main__':
    main()

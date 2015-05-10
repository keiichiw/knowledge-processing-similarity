#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import os.path
import sys
import wget
from bs4 import BeautifulSoup
import cv2

def get_name(tag):
    li = tag.find_all("li")
    for l in li:
        if "class" in l.attrs and "Name" in l["class"]:
            return l.div.strings.next().encode('utf-8')

    print >> sys.stderr,"Name Not Found:", tag

def get_image_url(tag):
    imgs = tag.find_all("img")
    for img in imgs:
        if "src" in img.attrs and img["src"][-3:]=="jpg":
            return img["src"]

    print >> sys.stderr, "Image Not Found:", tag

HOME_URL = "http://senkyo.mainichi.jp"
URL      = HOME_URL+"/giin/list.html?p="
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
            img_url = HOME_URL + get_image_url(tag)
            img_path="./img/"+m_id+".jpg"
            if not os.path.exists(img_path):
                wget.download(img_url, out=img_path)
            get_face(m_id)
            print "%s %s" % (m_id, name)
            print >>f, "%s %s" % (m_id, name)


def get_face(m_id):
    img_path="./img/"+m_id+".jpg"
    cascade_path = "./haarcascade_frontalface_alt.xml"

    image = cv2.imread(img_path)
    image_gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)

    cascade = cv2.CascadeClassifier(cascade_path)

    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

    if len(facerect) == 1:
        rect = facerect[0]

        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]

        face = cv2.resize(image_gray[y: y + h, x: x + w], (64, 64))
        face_path="./img/"+m_id+"_face.jpg"
        cv2.imwrite(face_path, face)
        return True
    else:
        print "fail to detect the face"


def main():
    with open("list.txt", "w") as f:
        for p in range(36):
            get_image_from_page(p+1, f)

if __name__ == '__main__':
    main()

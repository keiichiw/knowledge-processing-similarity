#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy
import cv2

MEMBER_NUM = 717
img_vecs = {}


def load_img(img_id):
    global img_vecs
    img_path = "./img/"+str(img_id).zfill(3)+"_face.jpg"
    try:
        image = cv2.imread(img_path, 0).flatten()
        n_image = image / numpy.linalg.norm(image)
        img_vecs[img_id] = n_image
    except:
        # 顔が認識されなかった
        pass

def calc_sim(v1, v2):
    x = numpy.dot(v1, v2)
    y = numpy.linalg.norm(v1) * numpy.linalg.norm(v2)
    return x / y

def main():
    global img_vecs

    for i in range(MEMBER_NUM):
        load_img(i+1)

    mx_v = 0
    mx_pair = (-1, -1)
    print " id| nearest| similarity"
    for k1, v1 in img_vecs.items():
        c_max = 0
        p = 0
        for k2, v2 in img_vecs.items():
            if k1 == k2:
                continue
            c = calc_sim(v1, v2)
            if c > c_max:
                c_max = c
                p = k2
        print str(k1).zfill(3), str(p).zfill(3), c_max
        if c_max > mx_v:
            mx_v = c_max
            mx_pair = (k1, p)
    print mx_v, mx_pair

if __name__ == '__main__':
    main()

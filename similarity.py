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
        n_image = image / numpy.linalg.norm(image) # 正規化
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

    print "calculation.."
    lst = []
    for k1, v1 in img_vecs.items():
        for k2, v2 in img_vecs.items():
            if k1 >= k2:
                continue
            c = calc_sim(v1, v2)
            lst.append((c, (k1, k2)))

    lst.sort()
    lst.reverse()

    f = open('list.txt')
    names = f.readlines()
    f.close()

    for i in range(3):
        p, (id1, id2) = lst[i]
        name1 = names[id1-1].split()[1]
        name2 = names[id2-1].split()[1]
        print "%03d%s, %03d%s : %f" % (id1, name1, id2, name2, p)

if __name__ == '__main__':
    main()

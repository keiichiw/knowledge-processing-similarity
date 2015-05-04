#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy

MEMBER_NUM = 717
img_vecs = []


def read_img(img_id):
    global img_vecs
    img = "./img/"+str(img_id).zfill(3)+".pgm"
    with open(img) as f:
        data = f.read().split()
        max_v = int(data[3])+0.0
        data = data[4:] # remove header
        vec = [int(v)/max_v for v in data]
        assert(len(vec)==4096)
        arr = numpy.array(vec)
        return arr / numpy.linalg.norm(arr)

def calc_sim(a, b):
    v1 = img_vecs[a]
    v2 = img_vecs[b]
    x = numpy.dot(v1, v2)
    y = numpy.linalg.norm(v1) * numpy.linalg.norm(v2)
    return x / y

def main():
    global img_vecs
    img_vecs = [read_img(i+1) for i in range(MEMBER_NUM)]

    cvec = []

    for i in range(MEMBER_NUM):
        c_max = 0
        p = -1
        for j in range(MEMBER_NUM):
            if i==j:
                continue
            c = calc_sim(i, j)
            if c > c_max:
                c_max = c
                p = j
        print i+1, p+1, c_max
    cvec.sort()
    print cvec[:5]
    print "-------------"
    print cvec[-5:]

if __name__ == '__main__':
    main()

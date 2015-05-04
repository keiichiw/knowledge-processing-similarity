#!/bin/bash

for file in ./img/*.jpg
do
    f=${file%.*}
    echo $f;
    convert -resize '128x' \
        -resize 'x128<' \
        -resize '50%' \
        -gravity 'center' \
        -crop '64x64+0+0' \
        ${f}.jpg ${f}_square.jpg;
    convert ${f}_square.jpg -compress none ${f}.pgm;
    rm ${f}_square.jpg
done

#!/bin/bash
experiment=$1
trial=$2

python2 create_frames.py $experiment $trial
bash combine_frames.sh $experiment $trial
rm figures/frames/*.png 
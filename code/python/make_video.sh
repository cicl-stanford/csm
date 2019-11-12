#!/bin/bash
experiment=$1 # '2ball', 'teleport', or '3ball'
trial=$2 # trial index (remember 0 indexing)

python2 create_frames.py $experiment $trial
bash combine_frames.sh $experiment $trial
rm figures/frames/*.png 
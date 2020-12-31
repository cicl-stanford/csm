#!/bin/bash
experiment=$1 # 'teleport' or '3ball'
trial=$2 # trial index (remember 0 indexing)

python3 create_frames.py $experiment $trial
bash combine_frames.sh $experiment $trial
rm figures/frames/*.png 
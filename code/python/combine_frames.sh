#!/bin/bash
experiment=$1
trial=$2
let trial+=1
ffmpeg -framerate 50 -i figures/frames/animation%3d.png  -c:v libx264 -profile:v high -crf 10 -pix_fmt yuv420p video/${experiment}_clip_${trial}.mp4


# A Counterfactual simulation model of causal judgment 

This repository contains all materials for the paper "A counterfactual simulation model of causal judgment" by Tobias Gerstenberg, Noah Goodman, David Lagnado & Joshua Tenenbaum. If you have any questions about this repository, please feel to email me at [gerstenberg@stanford.edu](mailto:gerstenberg@stanford.edu).

# Repository structure 

```
.
├── code
│   ├── R
│   │   ├── cache
│   │   └── data
│   ├── flash
│   │   ├── experiment1
│   │   ├── experiment2
│   │   └── experiment3
│   └── python
│       ├── figures
│       ├── results
│       ├── trialinfo
│       └── video
├── data
├── docs
├── figures
│   ├── clips
│   │   ├── experiment1
│   │   ├── experiment2
│   │   └── experiment3
│   ├── diagrams
│   └── plots
└── videos
    ├── experiment1
    ├── experiment2
    └── experiment3
```

## code 

### R 

Analysis and plotting script. You can view a rendered html file of the analysis [here](https://cicl-stanford.github.io/csm/). 

### flash 

Flash experiment code files. 

### python 

The counterfactual simulation model is implemented in python 3.7 using the physics engine [pymunk](http://www.pymunk.org/en/latest/). The  `model.py` file contains the model code. 

- to run the counterfactual simulation model, cd into `code/python/` 
- you can then run `python simulation_2ball.py 1` where the last number indicates the degree of noise that should be applied in the counterfactual simulation 
- `simulation_teleport.py` and `simulation_3ball.py` are used for generating model predictions for the Experiments 2 and 3 in the paper 
- in each simulation file, you can set the following parameters: 
	+ `n_simulations`: number of counterfactual simulations to run
	+ `trials`: which trials to run (specified as a list)
	+ `noise`: noise applied to the ball's motion in the counterfactual situation 
	+ `record_data`: logical value whether or not to record the outcome of the simulations 
	+ `experiment`: experiment indicator 
	+ `animate`: logical value whether or not to show animations of the simulations 

- to create videos of the different clips, you can run the `make_videos.sh` script like so `bash make_videos.sh '2balls' 0` (this would make a video of the first clip in Experiment 1)

## data 

Raw data files of the three experiments reported in the paper (two conditions each). 

## figures

### clips 

Illustrations of the different clips in each experiment. 

### diagrams 

Diagrams used in the paper. 

### plots 

Results plots. 

## videos 

Videos of the clips presented in the three different experiments. 
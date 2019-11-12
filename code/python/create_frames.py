from model import World
import sys

"""
Takes in experiment and trial to generate a png of each video frame 
experiment = '2ball', 'teleport', or '3ball'
trial = trial index (remember 0 indexing)
"""

experiment = sys.argv[1]
trial = int(sys.argv[2])

w = World()
w.simulate(experiment = experiment, trial = trial, animate = True, save = True)	

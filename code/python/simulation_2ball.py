from model import World
import sys
import pandas as pd
import numpy as np

##############################
# parameters
##############################

n_simulations = 1000
trials = range(0,18) # note that clips 11 and 12 are swapped
noise = float(sys.argv[1]) #noise 
record_data = True
experiment = '2ball'
animate = False

##############################
# set up data structure 
##############################

column_names = ['trial','noise','A_whether']

df = pd.DataFrame(0.0, index=np.arange(len(trials)), columns=column_names)

df['trial'] = trials
df['noise'] = noise

##############################
# run simulations 
##############################

w = World()

for idx, trial in enumerate(trials):
	df.loc[idx, 'A_whether'] = w.whether_cause(experiment = experiment, noise = noise, w = w, trial = trial, cause = 'A', df = df, n_simulations = n_simulations, animate = animate)

df['trial'] = df['trial'] + 1
df = df*1 #logical to integer

if record_data:
	df.to_csv('results/' + experiment + '_results_noise_' + str(noise).replace(".", "_") + '_nsamples_' + str(n_simulations) + '.csv', index = False)

from model import World
import sys
import pandas as pd
import numpy as np

##############################
# parameters
##############################

# n_simulations = 100
n_simulations = 1000
# n_simulations = 1
# trials = range(0,18)
trials = range(0,32)
# trials = [2]
# trials = [22]
noise = float(sys.argv[1]) #noise 
# noise = 0.9
perturb_robust = 10
# record_data = False
record_data = True
experiment = '3ball'
# animate = True
animate = False

##############################
# set up data structure 
##############################

column_names = ['trial','A_difference','A_how','A_whether','A_sufficient','A_robust','B_difference','B_how','B_whether','B_sufficient','B_robust']

df = pd.DataFrame(0.0, index=np.arange(len(trials)), columns=column_names)

df['trial'] = trials
df['noise'] = noise
df['perturb'] = perturb_robust
df['n_simulations'] = n_simulations
df['trial'] = df['trial']+1

##############################
# run simulations 
##############################

w = World()

for idx, trial in enumerate(trials):
	df.loc[idx, 'A_difference'] = w.difference_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'A', alternatives = ['B'], df = df, n_simulations = n_simulations, animate = animate)
	df.loc[idx, 'A_how'] = w.how_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'A', df = df, animate = animate)
	df.loc[idx, 'A_whether'] = w.whether_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'A', df = df, n_simulations = n_simulations, animate = animate)
	df.loc[idx, 'A_sufficient'] = w.sufficient_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'A', alternatives = ['B'], target = 'E', df = df, n_simulations = n_simulations, animate = animate)	
	df.loc[idx, 'A_robust'] = w.robust_cause(w = w, experiment = experiment, noise = noise, perturb = perturb_robust, trial = trial, cause = 'A', alternatives = ['B'], target = 'E', df = df, n_simulations = n_simulations, animate = animate)	

	df.loc[idx, 'B_difference'] = w.difference_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'B', alternatives = ['A'], df = df, n_simulations = n_simulations, animate = animate)
	df.loc[idx, 'B_how'] = w.how_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'B', df = df, animate = animate)
	df.loc[idx, 'B_whether'] = w.whether_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'B', df = df, n_simulations = n_simulations, animate = animate)
	df.loc[idx, 'B_sufficient'] = w.sufficient_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'B', alternatives = ['A'], target = 'E', df = df, n_simulations = n_simulations, animate = animate)
	df.loc[idx, 'B_robust'] = w.robust_cause(w = w, experiment = experiment, noise = noise, perturb = perturb_robust, trial = trial, cause = 'B', alternatives = ['A'], target = 'E', df = df, n_simulations = n_simulations, animate = animate)

	df = df*1 #logical to integer
	
	print("noise", noise)
	print("trial", trial+1)

	if record_data:
		df.to_csv('results/3ball_results_noise_' + str(noise).replace(".", "_") + "_perturb_" + str(perturb_robust) + "_nsamples_" + str(n_simulations) + '.csv',index=False)

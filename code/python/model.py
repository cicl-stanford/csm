import sys
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import itertools
import json
import numpy as np
import math
from pymunk import Vec2d
import collections #for keeping the order in which dictionaries were created

class World():
	"""
	Sets up world and simulates a particular trial
	- note: y-coordinates are flipped compared to javascript or flash implementation
	- run python window in low resolution mode: /usr/local/Cellar/python/3.7.2_2/Frameworks/Python.framework/Versions/3.7/Resources/Python.app
	- counterfactual tests could be made more efficient by only running the actual situation once
	"""

	def __init__(self):
		pass 

	def pymunk_setup(self,experiment):
		# Initialize space and set gravity for space to do simulation over
		self.width = 800
		self.height = 600
		self.ball_size = 60 
		self.speed = 200 # scales how fast balls are moving 
		self.step_size = 1/50.0
		self.step_max = 300 # step at which to stop the animation
		self.step = 0 # used to record when events happen 
		self.space = pymunk.Space()
		self.events = {'collisions': [],
						'outcome': None,
						'outcome_fine': None} # used to record events 
		# containers for bodies and shapes
		self.bodies = collections.OrderedDict()
		self.shapes = collections.OrderedDict()	
		self.sprites = collections.OrderedDict()
		
		self.collision_types = {
			'static': 0,
			'dynamic': 1,
			'teleport': 2
		}		
		self.experiment = experiment

		if self.experiment == '3ball':
			self.target_ball = 'E'
		else:
			self.target_ball = 'B'
	
		# add walls 
		self.add_wall(position = (400, 590), length = 800, height = 20, name = 'top_wall', space = self.space)
		self.add_wall(position = (400, 10), length = 800, height = 20, name = 'bottom_wall', space = self.space)
		self.add_wall(position = (10, 100), length = 20, height = 200, name = 'top_left_wall', space = self.space)
		self.add_wall(position = (10, 500), length = 20, height = 200, name = 'bottom_left_wall', space = self.space)

		# read in trial info 
		self.read_trials()
		self.balls = self.trials[self.trial]['balls']

		# add objects 
		if self.experiment == 'teleport':
			self.objects = self.trials[self.trial]['objects']
			for object in self.objects: 
				if object['name'] == 'brick':
					body, shape = self.add_brick(position = object['position'], name = object['name'], rotation = object['rotation'], space = self.space)
				if object['name'] == 'teleport_entrance':
					body, shape = self.add_teleport_entrance(position = object['position'], name = object['name'], rotation = object['rotation'], status = object['status'], space = self.space)
				if object['name'] == 'teleport_exit':
					body, shape = self.add_teleport_exit(position = object['position'], name = object['name'], status = object['status'], space = self.space)
				self.bodies[object['name']] = body
				self.shapes[object['name']] = shape		

		# add balls 
		for ball in self.balls:
			body, shape = self.add_ball(position = ball['position'], name = ball['name'], velocity = ball['velocity'], size = self.ball_size, space = self.space) 
			self.bodies[ball['name']] = body
			self.shapes[ball['name']] = shape

	# read in trial information 
	def read_trials(self):
		self.trials = json.load(open('trialinfo/' + self.experiment + '_trials.json', 'r'))

	# setup collision handlers 
	def collision_setup(self):	
		handler_dynamic = self.space.add_collision_handler(self.collision_types['dynamic'], self.collision_types['dynamic'])
		handler_dynamic.begin = self.collisions
		
		if self.experiment == 'teleport':		
			handler_teleport = self.space.add_collision_handler(self.collision_types['teleport'], self.collision_types['dynamic'])
			if self.bodies['teleport_entrance'].status == 'on':
				handler_teleport.begin = self.teleport

	# handle dynamic events
	def collisions(self,arbiter,space,data):
		# print arbiter.is_first_contact #checks whether it was the first contact between the shapes 
		event = {
			'balls': {arbiter.shapes[0].body.name,arbiter.shapes[1].body.name},
			'step': self.step
		}
		self.events['collisions'].append(event)
		return True

	# handle teleport
	def teleport(self,arbiter,space,data):
		objects = [arbiter.shapes[0].body,arbiter.shapes[1].body]
		for object in objects: 
			if object.name == 'B':
				object.position = self.bodies['teleport_exit'].position 
		return False	

	def add_wall(self, position, length, height, name, space):
		body = pymunk.Body(body_type = pymunk.Body.STATIC)
		body.position = position
		wall = pymunk.Poly.create_box(body, size = (length, height))
		wall.elasticity = 1
		wall.name = name 
		wall.collision_type = self.collision_types['static']
		space.add(wall)
		return wall	

	def add_ball(self, position, velocity, size, name, space):
		mass = 1
		radius = size/2
		moment = pymunk.moment_for_circle(mass, 0, radius)
		body = pymunk.Body(mass, moment)
		body.position = position
		body.size = (size,size)
		body.angle = 0
		velocity = [x*self.speed for x in velocity] 
		body.apply_impulse_at_local_point(velocity) #set velocity
		body.name = name 
		shape = pymunk.Circle(body, radius)
		shape.elasticity = 1.0
		shape.friction = 0
		shape.collision_type = self.collision_types['dynamic']
		space.add(body, shape)
		return body, shape

	def add_brick(self, position, rotation, name, space):
		body = pymunk.Body(body_type = pymunk.Body.STATIC)
		body.position = position
		body.name = name 
		body.size = (35, 100)
		body.angle = math.radians(rotation)
		shape = pymunk.Poly.create_box(body, size = body.size)
		shape.elasticity = 1
		shape.collision_type = self.collision_types['static']
		space.add(body, shape)
		return body, shape

	def add_teleport_entrance(self, position, rotation, name, status, space):
		body = pymunk.Body(body_type = pymunk.Body.STATIC)
		body.position = position
		body.name = name 
		body.size = (35, 100)
		body.angle = math.radians(rotation)
		body.status = status
		shape = pymunk.Poly.create_box(body, size = body.size)
		shape.sensor = True
		shape.collision_type = self.collision_types['teleport']
		space.add(body, shape)
		return body, shape

	def add_teleport_exit(self, position, name, status, space):
		# take out of physics later ... 
		body = pymunk.Body(body_type = pymunk.Body.STATIC)
		body.position = position
		body.name = name 
		# body.size = (40,40)
		body.angle = 0
		body.status = status
		shape = pymunk.Circle(body, 20)
		shape.sensor = True
		# space.add(body, shape)
		return body, shape

	def remove(self,ball,step,animate):
		if self.step == step:
			self.space.remove(self.shapes[ball]) #remove body from space 
			self.space.remove(self.bodies[ball]) #remove body from space 
			del self.bodies[ball] #remove body 
			del self.shapes[ball] #remove shape
			if animate: 		
				del self.sprites[ball] #remove sprite 

	def perturb(self,ball,step,magnitude = 0):
		if self.step == step:
			b = self.bodies[ball]
			b.position = (b.position.x+self.gaussian_noise()*magnitude,
				b.position.y+self.gaussian_noise()*magnitude)

	def apply_noise(self,ball,step,noise):
		if not noise == 0:
			b = self.bodies[ball]
			if self.step > step:
				x_vel = b.velocity[0]
				y_vel = b.velocity[1]
				perturb = self.gaussian_noise()*noise
				cos_noise = np.cos(perturb*np.pi/180)
				sin_noise = np.sin(perturb*np.pi/180)
				x_vel_noise = x_vel * cos_noise - y_vel * sin_noise
				y_vel_noise = x_vel * sin_noise + y_vel * cos_noise
				b.velocity = x_vel_noise,y_vel_noise

	def end_clip(self,animate):
		if self.step > self.step_max:
			b = self.bodies[self.target_ball]
			if b.position[0] > -self.ball_size/2:
				self.events['outcome'] = 0
			else:
				self.events['outcome'] = 1
			self.events['outcome_fine'] = b.position
			pygame.display.quit()
			return True

	def simulate(self, experiment = '3ball', animate=True, trial=0, noise = 0, save=False, info=[]):
		# Initialization 
		self.trial = trial
		self.pymunk_setup(experiment)
		self.collision_setup()
		pic_count = 0 # used for saving images 
		done = False # pointer to say when animation is done 
		self.info = info
		self.noise = noise
		
		# If animating, initialize pygame animation
		if animate:
			pygame.init()
			clock = pygame.time.Clock()

			# Set size/title of display
			screen = pygame.display.set_mode((self.width, self.height))
			pygame.display.set_caption("Animation")

			# Load sprites
			for body in self.bodies:
				b = self.bodies.get(body)
				if  b.name == 'teleport_entrance' or b.name == 'teleport_exit':
					name = b.name + "_" + b.status
				else: 
					name = b.name
				sprite = pygame.image.load('figures/' + name + '.png')
				self.sprites[body] = sprite

		# Run the simulation forever, until exit
		while not done:
			if animate:
				# Lets you exit the animation loop by clicking escape on animation
				for event in pygame.event.get():
					if event.type == QUIT:
							sys.exit(0)
					elif event.type == KEYDOWN and event.key == K_ESCAPE:
							sys.exit(0)

				# Draw static elements 
				screen.fill((255,255,255)) #background 
				pygame.draw.rect(screen, pygame.color.THECOLORS['red'], [0,200,20,200]) #goal
				pygame.draw.rect(screen, pygame.color.THECOLORS['black'], [0,0,800,20]) #top wall
				pygame.draw.rect(screen, pygame.color.THECOLORS['black'], [0,580,800,20]) #bottom wall
				pygame.draw.rect(screen, pygame.color.THECOLORS['black'], [0,0,20,200]) #top left
				pygame.draw.rect(screen, pygame.color.THECOLORS['black'], [0,400,20,200]) #bottom left
				
				# update object positions over time 
				for body in self.bodies:
					self.update_sprite(body = self.bodies.get(body), sprite = self.sprites.get(body),screen = screen)

				# Draw the space
				pygame.display.flip()
				pygame.display.update()
				clock.tick(100)
				
				if save:
					pygame.image.save(screen, 'figures/frames/animation'+'{:03}'.format(pic_count)+'.png')
					pic_count += 1

			# manipulations 
			if self.info:
				for action in self.info:
					if action['action'] == 'remove':
						self.remove(ball = action['ball'], step = action['step'], animate = animate)
					if action['action'] == 'perturb':
						self.perturb(ball = action['ball'], step = action['step'], magnitude = action['magnitude'])
					if action['action'] == 'noise':
						self.apply_noise(ball = action['ball'], step = action['step'], noise = self.noise)

			# Take a step in the simulation, update clock/ticks
			done = self.end_clip(animate = animate)

			self.space.step(self.step_size) 
			self.step += 1

		return self.events

	def flipy(self, y):
	    """Small hack to convert chipmunk physics to pygame coordinates"""
	    return -y+600

	def update_sprite(self,body,sprite,screen):
		p = body.position
		p = Vec2d(p.x, self.flipy(p.y))
		angle_degrees = math.degrees(body.angle)
		rotated_shape = pygame.transform.rotate(sprite, angle_degrees)
		offset = Vec2d(rotated_shape.get_size()) / 2.
		p = p - offset
		screen.blit(rotated_shape, p)

	def gaussian_noise(self):
		u = 1 - np.random.random()
		v = 1 - np.random.random()
		return np.sqrt(-2*np.log(u)) * np.cos(2 * np.pi * v)

	##############################
	# define counterfactual operations (local noise)
	##############################
	# A procedure to determine which balls need added noise at what time
	def noise_addition(self, collisions, in_chain, start_time):
		# Base case. When the list is empty return the empty list
		if collisions == []:
			return []
		else:
			# Otherwise grab the first collision. Diff is all balls in the collision
			# that are not currently in the causal chain
			hd = collisions[0]
			diff = hd['balls'] - in_chain

			# If both balls are not in the causal chain, then the collision is not connected
			# to the causal chain. Because the collisions are sorted by time, we know it can be ignored

			# If both balls are already in the causal chain, then they already should have noise applied
			# (or have been removed). We don't need to add noise.

			# If only one ball is not in the causal chain, then this collision makes that ball a part
			# of the causal chain. Check to make sure it did not occur simultaneously with the previous
			# collision (a counterexample). If it did not then we add that ball and the timestep of the
			# collision to the output. We also add the ball to the set of in_chain balls and update the
			# timestep
			if len(diff) == 1 and hd['step'] > start_time:
				b2 = diff.pop()
				new_set = in_chain | {b2}
				return [(b2, hd['step'])] + self.noise_addition(collisions[1:], new_set, hd['step'])
			else:
				return self.noise_addition(collisions[1:], in_chain, start_time)

	# A procedure to test whether the candidate cause was a difference maker
	def difference_cause(self, w, experiment, noise, trial, cause, alternatives, df, n_simulations, animate, test_noise=False):
		# run actual world 
		events = w.simulate(experiment = experiment, trial = trial, animate=animate)	

		# Determine all the objects that need noise addition. Filter out the target
		# because adding noise to the target will automatically change its fine outcome
		# in the cf. This is okay, because if the target was a part of the direct causal
		# chain, it will still be affected by the removal and thus labeled a dm
		noise_adds = self.noise_addition(events['collisions'], {cause}, -1)
		noise_adds = [x for x in noise_adds if x[0] != self.target_ball]

		# save the fine outcome
		outcome_actual = events['outcome_fine']

		# remove candidate cause 
		info = [{
			'action': 'remove',
			'ball': cause,
			'step': 0
		}]

		# add noise + transitive noise if appropriate
		for item in noise_adds:
			info.append({
					'action': 'noise',
					'ball': item[0],
					'step': item[1]
				})

		# Simulate n outcomes, saving the sim outcomes each time. 
		outcomes = []
		for x in range(0, n_simulations):
			events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info)
			outcome_counterfactual = events['outcome_fine']
			outcomes.append(outcome_actual != outcome_counterfactual)
		
		if not test_noise:
			return sum(outcomes)/float(n_simulations)
		else:
			return sum(outcomes)/float(n_simulations), {'info': info}

	# A procedure to measure the degree to which a candidate cause is a whether cause
	def whether_cause(self, experiment, noise, w, trial, cause, df, n_simulations, animate, test_noise = False):
		# run actual world 
		# events = w.simulate(experiment = experiment, trial = trial, animate=animate)	
		events = w.simulate(experiment = experiment, trial = trial, animate=False)	
		# get the outcome and determine which objects need noise added post removal
		outcome_actual = events['outcome']
		noise_add = self.noise_addition(events['collisions'], {cause}, -1)

		# remove candidate cause (maybe remove right at the beginning)
		info = [{
			'action': 'remove',
			'ball': cause,
			'step': 0
		}]

		# add noise
		for item in noise_add:
			info.append({
					'action': 'noise',
					'ball': item[0],
					'step': item[1]
				})
		
		# simulate n times and return the proportion of outcomes that differ from the actual
		outcomes = []
		for x in range(0, n_simulations):
			events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info)
			outcomes.append(events['outcome'] != outcome_actual)
		
		if not test_noise:
			return sum(outcomes)/float(n_simulations)
		else:
			return sum(outcomes)/float(n_simulations), {'info': info}
	
	# A procedure to determine whether the candidate cause is a how cause
	def how_cause(self, w, experiment, noise, trial, cause, df, animate):
		# same as the global version
		# run actual world 
		events = w.simulate(experiment = experiment, trial = trial, animate=animate)	
		outcome_actual = events['outcome_fine']

		# perturb candidate cause 
		info = [{
			'action': 'perturb',
			'ball': cause,
			'step': 0,
			'magnitude': 0.0001
		}]

		# simulate the conterfactual. If the outcome is different at a fine level, the candidate
		# is a how cause
		events = w.simulate(experiment = experiment, trial = trial, animate = animate, info = info)
		outcome_counterfactual = events['outcome_fine']
		
		return (outcome_counterfactual != outcome_actual)

	# A procedure to measure the degree to which the candidate is a sufficient cause
	def sufficient_cause(self, w, experiment, noise, trial, cause, alternatives, target, df, n_simulations, animate, test_noise=False):
		# run actual world 
		events = w.simulate(experiment = experiment, trial = trial, animate = animate)
		outcome_actual = events['outcome']
		# For this version of the model there will be exactly one alternative
		# Could be better generalized for other cases
		alternative = alternatives[0]
		noise_add = self.noise_addition(events['collisions'], {alternative}, -1)

		# manipulations
		# For first cf, remove alternative cause and add noise to anything it collided with
		info = [{
			'action': 'remove',
			'ball': alternative,
			'step': 0
		}]

		for item in noise_add:
			info.append({
					'action': 'noise',
					'ball': item[0],
					'step': item[1]
				})

		# For the contingency manipulations, remove the alternative and the cause. 
		info_cont = [
			{
				'action': 'remove',
				'ball': cause,
				'step': 0
			},
			{
				'action': 'remove',
				'ball': alternative,
				'step': 0
			}
		]

		# See how both the candidate cause and alternative propogate noise. Combine the noise additions
		# and sort by timestep. Remove any that aren't related to the target (since the target) is
		# the only body left. If there are still noise additions, take the first, the only one we need
		noise_add_cont = sorted(self.noise_addition(events['collisions'], {cause}, -1) + noise_add, key=lambda x: x[1])
		noise_add_cont = [x for x in noise_add_cont if x[0] == target]
		if len(noise_add_cont) > 0:
			tar_noise = noise_add_cont[0]
			info_cont.append({'action': 'noise', 'ball': tar_noise[0], 'step': tar_noise[1]})

		
		outcomes = []
		for x in range(0, n_simulations):

			# Simulate the cf with just the alternative removed
			events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info)
			outcome_counterfactual = events['outcome']		

			# Simulate the cf with the alternative and the cause removed
			events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info_cont)
			outcome_counterfactual_contingency = events['outcome']
			 
			# The candidate gets a point in favor of sufficiency whenever it is a whether cause with all
			# alternatives removed (the second conjunct) and the event that it causes is the same as what
			# took place in the actual world (the first conjunct)
			outcomes.append((outcome_actual == outcome_counterfactual) and (outcome_counterfactual != outcome_counterfactual_contingency))
		
		# return the sum of sufficiency points over total simulations
		if not test_noise:
			return sum(outcomes)/float(n_simulations)
		else:
			return sum(outcomes)/float(n_simulations), {'info': info, 'info_cont': info_cont}

	# A procedure to measure the extent to which the candidate is a robust cause
	def robust_cause(self, w, experiment, noise, perturb, trial, cause, alternatives, target, df, n_simulations, animate, test_noise=False):
			# run actual world 
			events = w.simulate(experiment = experiment, trial = trial, animate=animate)
			outcome_actual = events['outcome']
			noise_add = self.noise_addition(events['collisions'], {cause}, -1)	

			# perturb alternatives
			info = []
			for alternative in alternatives: 
				info.append({
					'action': 'perturb',
					'ball': alternative,
					'step': 0,
					'magnitude': perturb
				})

			# Keep the perturbations and remove the cause. Add noise to anything downstream
			# of the cause in the collision chain
			info_cont = info + [{'action': 'remove', 'ball': cause, 'step': 0}]
			for item in noise_add:
				info_cont.append({
						'action': 'noise',
						'ball': item[0],
						'step': item[1]
					})

			# Simulate the world with and without the candidate cause
			# Every situation where the outcome with the candidate matches the actual world and the outcome
			# without the candidate differs from the actual is a point in favor of the candidates robustness
			outcomes = []
			for x in range(0, n_simulations):
				events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info)
				outcome_counterfactual = events['outcome']
				
				events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info_cont)
				outcome_counterfactual_contingency = events['outcome']
				 
				outcomes.append((outcome_actual == outcome_counterfactual) and (outcome_counterfactual != outcome_counterfactual_contingency))
			
			if not test_noise:
				return sum(outcomes)/float(n_simulations)
			else:
				return sum(outcomes)/float(n_simulations), {'info_cont': info_cont}

